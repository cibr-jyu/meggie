# coding: utf-8

# Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and
# Atte Rautio>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 16, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen, Atte Rautio
Contains the MainWindow-class that holds the main window of the application.
"""

import os
import sys
import traceback
import shutil
import sip
import gc
import json

import matplotlib
import mne

from PyQt4 import QtCore
from PyQt4 import QtGui
from PyQt4.QtGui import QWhatsThis
from PyQt4.QtGui import QAbstractItemView
from PyQt4.Qt import QApplication

from mne.evoked import write_evokeds

matplotlib.use('Qt4Agg')

from meggie.ui.general.mainWindowUi import Ui_MainWindow
from meggie.ui.general.createExperimentDialogMain import CreateExperimentDialog
from meggie.ui.general.addSubjectDialogMain import AddSubjectDialog
from meggie.ui.general.infoDialogMain import InfoDialog
from meggie.ui.general.channelSelectionDialogMain import ChannelSelectionDialog
from meggie.ui.epoching.eventSelectionDialogMain import EventSelectionDialog
from meggie.ui.visualization import visualizeEpochChannelDialogMain
from meggie.ui.preprocessing.maxFilterDialogMain import MaxFilterDialog
from meggie.ui.preprocessing.eogParametersDialogMain import EogParametersDialog
from meggie.ui.preprocessing.ecgParametersDialogMain import EcgParametersDialog
from meggie.ui.general.preferencesDialogMain import PreferencesDialog
from meggie.ui.general.evokedStatsDialogMain import EvokedStatsDialog
from meggie.ui.preprocessing.addECGProjectionsMain import AddECGProjections
from meggie.ui.preprocessing.addEOGProjectionsMain import AddEOGProjections
from meggie.ui.visualization.TFRDialogMain import TFRDialog
from meggie.ui.visualization.TFRTopologyDialogMain import TFRTopologyDialog
from meggie.ui.visualization.powerSpectrumDialogMain import PowerSpectrumDialog
from meggie.ui.widgets.epochWidgetMain import EpochWidget
from meggie.ui.general.aboutDialogMain import AboutDialog
from meggie.ui.filtering.filterDialogMain import FilterDialog
from meggie.ui.sourceModeling.forwardModelDialogMain import ForwardModelDialog
from meggie.ui.sourceModeling.sourceEstimateDialogMain import SourceEstimateDialog
from meggie.ui.general.experimentInfoDialogMain import experimentInfoDialog
from meggie.ui.sourceModeling.forwardSolutionDialogMain import ForwardSolutionDialog
from meggie.ui.sourceModeling.covarianceRawDialogMain import CovarianceRawDialog
from meggie.ui.sourceModeling.plotStcDialogMain import PlotStcDialog
from meggie.ui.widgets.covarianceWidgetNoneMain import CovarianceWidgetNone
from meggie.ui.widgets.covarianceWidgetRawMain import CovarianceWidgetRaw
from meggie.ui.general.logDialogMain import LogDialog
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

from meggie.code_meggie.general import experiment
from meggie.code_meggie.general.experiment import Experiment
from meggie.code_meggie.general.preferences import PreferencesHandler
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.general.mvcModels import ForwardModelModel
from meggie.code_meggie.general.mvcModels import SubjectListModel
from meggie.code_meggie.general.mvcModels import _initializeForwardSolutionList
from meggie.code_meggie.general.mvcModels import _initializeInverseOperatorList
from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general.wrapper import wrap_mne_call
from meggie.code_meggie.epoching.evoked import Evoked


class MainWindow(QtGui.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """

    caller = Caller.Instance()

    def __init__(self, application):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.spectrumDialog = None
        self.filterDialog = None
        self.epochParameterDialog = None
        self.tfr_dialog = None
        self.tfrTop_dialog = None
        self.log_dialog = None
        
        # List of subprocesses, used for terminating MNE-C processes on Meggie
        # quit.
        self.processes = []

#         # Direct output to console
#         if 'debug' not in sys.argv:
#             self.directOutput()
#             self.ui.actionDirectToConsole.triggered.connect(self.directOutput)
#             sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
#             sys.stderr = EmittingStream(textWritten=self.errorOutputWritten)

        # One main window (and one _experiment) only needs one caller to do its
        # bidding.
        self.caller.setParent(self)

        # For storing and handling program wide prefences.
        self.preferencesHandler = PreferencesHandler()
        self.preferencesHandler.set_env_variables()

        # For handling initialization and switching of experiments.
        self.experimentHandler = experiment.ExperimentHandler(self)

        # No tabs in the tabWidget initially
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

        # Creates a label on status bar to show current working file message.
        self.statusLabel = QtGui.QLabel()
        self.ui.statusbar.addWidget(self.statusLabel)

        # Creates a listwidget for epoch analysis.
        self.epochList = EpochWidget(self)
        self.epochList.hide()

        #self.ui.listWidgetEvoked.setHorizontalScrollBarPolicy(300)
        self.ui.listWidgetEvoked.setMinimumWidth(346)
        self.ui.listWidgetEvoked.setMaximumWidth(346)
        
        self.evokeds_batching_widget = BatchingWidget(
            self, self.ui.widget,
            self.ui.pushButtonCreateEvoked,
            self.ui.pushButtonCreateEvokedBatch,
            self.evoked_selection_changed,
            self.collect_evoked_parameter_values,
            lambda: self.initialize_ui()
        )
        
        # Populate the combobox for selecting lobes for channel averages.
        self.populate_comboBoxLobes()

        # Connect signals and slots.
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)

        # Models for several views in the UI, e.g. in the forward model setup
        # tab.
        self.forwardModelModel = ForwardModelModel(self)
        self.subjectListModel = SubjectListModel(self)


        # Proxymodels for tuning what is actually shown in the views below.
        self.proxyModelTableViewForwardSolutionSource = QtGui.\
            QSortFilterProxyModel(self)
        self.proxyModelTableViewForwardSolutionSource.setFilterKeyColumn(15)
        rx = QtCore.QRegExp('yes')
        self.proxyModelTableViewForwardSolutionSource.setFilterRegExp(rx)
        self.proxyModelTableViewForwardSolutionSource.\
            setSourceModel(self.forwardModelModel)

        self.proxyModelTableViewForwardSolutions = QtGui.\
            QSortFilterProxyModel(self)
        self.proxyModelTableViewForwardSolutions.setFilterKeyColumn(16)
        rx2 = QtCore.QRegExp('yes')
        self.proxyModelTableViewForwardSolutions.setFilterRegExp(rx2)
        self.proxyModelTableViewForwardSolutions.\
            setSourceModel(self.forwardModelModel)

        # Linking corresponding views to models above and tuning them

        self.ui.listViewSubjects.setModel(self.subjectListModel)

        self.ui.tableViewForwardModels.setModel(self.forwardModelModel)
        for colnum in range(17, 21):
            self.ui.tableViewForwardModels.setColumnHidden(colnum, True)

        self.ui.tableViewFModelsForCoregistration.setModel(self.forwardModelModel)
        for colnum in range(16, 21):
            self.ui.tableViewFModelsForCoregistration.setColumnHidden(colnum,
                                                                      True)

        tvfs = self.ui.tableViewFModelsForSolution
        tvfs.setModel(self.proxyModelTableViewForwardSolutionSource)
        for colnum in range(1, 16):
            tvfs.setColumnHidden(colnum, True)

        # If the user has chosen to open the previous experiment automatically.
        if self.preferencesHandler.auto_load_last_open_experiment is True:
            exp = None
            
            try:
                exp = self.experimentHandler.open_existing_experiment(self.preferencesHandler)
            except Exception as e:
                exc_messagebox(self, e)
            
            if exp:
                self.caller.experiment = exp
                self.add_tabs()
                self.initialize_ui()
                self.reinitialize_models()
            else:
                self.preferencesHandler.previous_experiment_name = ''
                self.preferencesHandler.write_preferences_to_disk()

        # Populate layouts combobox.
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)
        if self.epochList.ui.listWidgetEpochs.count() > 1:
            self.epochList.ui.listWidgetEpochs.setCurrentRow(0)
        self.ui.listWidgetBads.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.listWidgetProjs.setSelectionMode(QAbstractItemView.NoSelection)
        
    def update_ui(self):
        """
        Method for repainting the ui.
        Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()

# Code for catching signals and reacting to them:
    def on_actionQuit_triggered(self, checked=None):
        """Closes the program, possibly after a confirmation by the user."""
        if checked is None:
            return

        if self.preferencesHandler.confirm_quit:
            reply = QtGui.QMessageBox.question(self, 'Close Meggie',
                                               'Are you sure you want to quit '
                                               'Meggie?', QtGui.QMessageBox.Yes
                                               | QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                self.close()
        else:
            self.close()

    def on_actionCreate_experiment_triggered(self, checked=None):
        """Create a new CreateExperimentDialog and show it"""
        if checked is None:
            return

        if self.preferencesHandler.working_directory != '':
            self.dialog = CreateExperimentDialog(self)
            self.dialog.experimentCreated.connect(self.setExperiment)
            self.dialog.show()
        else:
            self.check_workspace()
            if self.preferencesHandler.working_directory != '':
                self.dialog = CreateExperimentDialog(self)
                self.dialog.experimentCreated.connect(self.setExperiment)
                self.dialog.show()

    @QtCore.pyqtSlot(Experiment)
    def setExperiment(self, newExperiment):
        """Temporary setter for experiment."""
        self.caller.experiment = newExperiment
        gc.collect()
        
        self.add_tabs()
        self.initialize_ui()
        self.reinitialize_models()

    def on_actionOpen_experiment_triggered(self, checked=None):
        """
        Open an existing _experiment.

        TODO actual experiment opening code should be in ExperimentHandler
        """
        # Standard workaround for file dialog opening twice
        if checked is None:
            return
        if self.caller.experiment is not None:
            directory = self.caller.experiment.workspace
        else:
            directory = ''
        path = str(QtGui.QFileDialog.getExistingDirectory
                   (self, "Select _experiment directory", directory))
        if path == '':
            return
        
        print 'Opening experiment ' + path

        try:
            exp = self.experimentHandler.open_existing_experiment(
                self.preferencesHandler, path=path)
            self.caller.experiment = exp
            self.add_tabs()
            self.initialize_ui()
            self.reinitialize_models()
        except Exception as e:
            exc_messagebox(self, e)
        except ValueError as e:
            messagebox(self, e)
        self.preferencesHandler.write_preferences_to_disk()

    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """Open subject dialog."""
        if checked is None:
            return

        # Check that we have an experiment that we can add a subject to
        if self.caller.experiment is None:
            msg = ('No active experiment to add a subject to. Load an '
                   'experiment or make a new one, then try again.')
            messagebox(self, msg)
            return

        self.subject_dialog = AddSubjectDialog(self)
        self.subject_dialog.exec_()

    def on_pushButtonRemoveSubject_clicked(self, checked=None):
        """Delete the selected subject item and the files related to it."""
        if checked is None:
            return

        selIndexes = self.ui.listViewSubjects.selectedIndexes()

        if selIndexes == []:
            message = 'No subject selected for removal.'
            messagebox(self, message)
            return

        message = 'Permanently remove the selected subects and the related files?'
        reply = QtGui.QMessageBox.question(self, 'delete selected subjects',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            rows_to_remove = []
            for index in selIndexes:
                subject_name = index.data()
        
                try:
                    self.caller.experiment.remove_subject(subject_name, self)
                    rows_to_remove.append(index.row())
                except Exception:
                    msg = 'Could not remove the contents of the subject folder.'
                    messagebox(self, msg)
    
            self.subjectListModel.removeRows(rows_to_remove)

        self.initialize_ui()

    def show_epoch_collection_parameters(self, epochs):
        """
        Shows parameters from the currently chosen epochs.

        Keyword arguments:
        epochs -- Epochs object
        """
        # Set default/empty values for epoch parameters.
        self.clear_epoch_collection_parameters()
        params = epochs.params
        if params is None:
            print 'Epochs parameters not found!'
            return
            # TODO: Fill source file field if no parameters for epochs
            # collection. 'filename' is the current location of the collection,
            # so add some other information here?
        #events = params['events']
        
        events = epochs.raw.event_id
        
        for event_name, event_id in events.items():
            events_str = event_name + ' [' + str(len(epochs.raw[event_name])) + ' events found]'
            item = QtGui.QListWidgetItem()
            item.setText(events_str)
            self.epochList.ui.listWidgetEvents.addItem(item)
        
        
        
       # TODO: create category items to add on the listWidgetEvents widget.
        self.ui.textBrowserTmin.setText(str(params['tmin']) + ' s')
        self.ui.textBrowserTmax.setText(str(params['tmax']) + ' s')
        # Creates dictionary of strings instead of qstrings for rejections.
        params_rejections_str = dict((str(key), value) for key, value in
                                     params['reject'].iteritems())
        if 'mag' in params_rejections_str:
            self.ui.textBrowserMag.setText(str(params_rejections_str['mag']) + ' fT')
        else:
            self.ui.textBrowserMag.setText('-1')
        if 'grad' in params_rejections_str:
            self.ui.textBrowserGrad.setText(str(params_rejections_str['grad']) + ' fT/cm')
        else:
            self.ui.textBrowserGrad.setText('-1')
        if 'eeg' in params_rejections_str:
            self.ui.textBrowserEEG.setText(str(params_rejections_str['eeg']) + 'uV')
        else:
            self.ui.textBrowserEEG.setText('-1')
        if 'stim' in params_rejections_str:
            self.ui.textBrowserStim.setText('Yes')
        else:
            self.ui.textBrowserStim.setText('-1')
        if 'eog' in params_rejections_str:
            self.ui.textBrowserEOG.setText(str(params_rejections_str['eog'] / 
                                               1e-6) + 'uV')
        else:
            self.ui.textBrowserEOG.setText('-1')
        self.ui.textBrowserWorkingFile.setText(os.path.basename(epochs.raw.info['filename']))

    def clear_epoch_collection_parameters(self):
        """
        Clears epoch collection parameters on mainWindow Epoching tab.
        """
        while self.epochList.ui.listWidgetEvents.count() > 0:
            self.epochList.ui.listWidgetEvents.takeItem(0)
        self.ui.textBrowserTmin.clear()
        self.ui.textBrowserTmax.clear()
        self.ui.textBrowserGrad.clear()
        self.ui.textBrowserMag.clear()
        self.ui.textBrowserEEG.clear()
        self.ui.textBrowserStim.clear()
        self.ui.textBrowserEOG.clear()
        self.ui.textBrowserWorkingFile.clear()

    def on_actionSet_workspace_triggered(self, checked=None):
        """
        Open the preferences dialog the for specific purpose of initial setting
        of workspace.
        """
        if checked is None:
            return
        self.check_workspace()

    def on_actionShow_log_triggered(self, checked=None):
        if checked is None:
            return
        if self.caller.experiment is None:
            message = 'Please open an experiment first.'
            messagebox(self, message)
            return
        self.log_dialog = LogDialog(self)
        self.log_dialog.show()

    def on_actionPreferences_triggered(self, checked=None):
        """Open the preferences-dialog."""
        if checked is None:
            return
        self.dialogPreferences = PreferencesDialog(self)
        self.dialogPreferences.show()

    def on_pushButtonCreateEpochs_clicked(self, checked=None):
        """Open the epoch dialog."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.epochParameterDialog = EventSelectionDialog(self)
        self.epochParameterDialog.finished.connect(self.on_close)
        self.epochParameterDialog.show()

    def closeEvent(self, event):
        """Redefine window close event to allow confirming on quit."""

        if self.preferencesHandler.confirm_quit:
            reply = QtGui.QMessageBox.question(self, 'Close Meggie',
                                               'Are you sure you want to '
                                               'quit?', QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def update_epochs(self):
        """Populates the epochs list.
        """
        self.epochList.clearItems()
        epochs = self.caller.experiment.active_subject.epochs
        if epochs is not None:
            for epoch in epochs.values():
                print epoch.collection_name
                item = QtGui.QListWidgetItem(epoch.collection_name)
                self.epochList.addItem(item)

    def on_actionAbout_triggered(self, checked=None):
        """Open the About-dialog."""
        if checked is None:
            return
        self.dialogAbout = AboutDialog()
        self.dialogAbout.show()

    def on_actionShowExperimentInfo_triggered(self, checked=None):
        """Open the experiment info dialog """
        if checked is None:
            return
        if self.caller.experiment is None:
            messagebox(self, 'You do not currently have an experiment activated.')  # noqa
            return
        self.expInfoDialog = experimentInfoDialog()
        self.expInfoDialog.show()

    def on_actionHide_Show_subject_list_and_info_triggered(self, checked=None):
        if checked is None:
            return
        if self.ui.dockWidgetSubjects.isVisible():
            self.ui.dockWidgetSubjects.hide()
        else:
            self.ui.dockWidgetSubjects.show()

    def on_actionToggle_whatsthis_mode_triggered(self, checked=None):
        if checked is None:
            return
        if QWhatsThis.inWhatsThisMode():
            QWhatsThis.leaveWhatsThisMode()
        else:
            QWhatsThis.enterWhatsThisMode()

    def collect_evoked_parameter_values(self):
        collection_names = [str(item.text()) for item 
                in self.epochList.ui.listWidgetEpochs.selectedItems()]
        return collection_names        

    def evoked_selection_changed(self, subject_name, data_dict):
        epoch_widget = self.epochList.ui.listWidgetEpochs
        
        epoch_widget.clear()
        for name in self.caller.experiment.subjects[subject_name].epochs:
            item = QtGui.QListWidgetItem()
            item.setText(name)
            epoch_widget.addItem(item)
            if name in data_dict:
                epoch_widget.setItemSelected(item, True)

    def _calculate_evokeds(self, subject, collection_names):
        
        evokeds = {}
        for name in collection_names:
            collection = subject.epochs[name]

            try:
                collection = subject.epochs[name]
            except KeyError:
                raise KeyError('No epoch collection called ' + str(name))

            epoch = collection.raw
            evoked = epoch.average()
            evoked.comment = name
            evokeds[name] = evoked

        evoked_name = (
            '-'.join(collection_names) +
            '_evoked.fif'
        )
    
        self._save_evoked(subject, evokeds, evoked_name)
#         # Save evoked into evoked (average) directory with name evoked_name
#         saveFolder = subject.evokeds_directory
#         if not os.path.exists(saveFolder):
#             try:
#                 os.mkdir(saveFolder)
#             except IOError:
#                 message = ('Writing to selected folder is not allowed. You can'
#                            ' still process the evoked file (visualize etc.).')
#                 raise IOError(message)
# 
#         try:
#             print 'Writing evoked data as ' + evoked_name + ' ...'
#             write_evokeds(os.path.join(saveFolder, evoked_name), evokeds.values())
#         except IOError:
#             message = ('Writing to selected folder is not allowed. You can '
#                        'still process the evoked file (visualize etc.).')
#             raise IOError(message)
#         
#         new_evoked = Evoked(evoked_name, subject, evokeds)
#         subject.add_evoked(new_evoked)        

    def _save_evoked(self, subject, evokeds, evoked_name):
        # Save evoked into evoked (average) directory with name evoked_name
        saveFolder = subject.evokeds_directory
        if not os.path.exists(saveFolder):
            try:
                os.mkdir(saveFolder)
            except IOError:
                message = ('Writing to selected folder is not allowed. You can'
                           ' still process the evoked file (visualize etc.).')
                raise IOError(message)

        try:
            print 'Writing evoked data as ' + evoked_name + ' ...'
            write_evokeds(os.path.join(saveFolder, evoked_name), evokeds.values())
        except IOError:
            message = ('Writing to selected folder is not allowed. You can '
                       'still process the evoked file (visualize etc.).')
            raise IOError(message)
        
        new_evoked = Evoked(evoked_name, subject, evokeds)
        subject.add_evoked(new_evoked)                
        
    def on_pushButtonCreateEvoked_clicked(self, checked=None):
        """
        Create averaged epoch collection (evoked dataset).
        Plot the evoked data as a topology.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        selected_items = self.epochList.ui.listWidgetEpochs.selectedItems()
        collection_names = [str(item.text()) for item in selected_items]

        # If no collections are selected, show a message to to the user and return.
        if len(collection_names) == 0:
            messagebox(self, 'Please select an epoch collection to average.')
            return

        subject = self.caller.experiment.active_subject
        
        try:
            self._calculate_evokeds(subject, collection_names)
        except Exception as e:
            exc_messagebox(self, e)

        self.caller.experiment.save_experiment_settings()
        self.evokeds_batching_widget.cleanup(self)
        self.initialize_ui()

    def on_pushButtonCreateEvokedBatch_clicked(self, checked=None):
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        subject_names = self.evokeds_batching_widget.selected_subjects
        
        recently_active_subject_name = self.caller.experiment.active_subject.subject_name
         
        for subject_name, collection_names in self.evokeds_batching_widget.data.items():
            if subject_name in subject_names:
                subject = self.caller.experiment.activate_subject(subject_name)
                try:
                    self._calculate_evokeds(subject, collection_names)
                except Exception as e:
                    failed_subjects = self.evokeds_batching_widget.failed_subjects
                    failed_subjects.append((subject, str(e)))
                    traceback.print_exc()
                     
        self.caller.experiment.activate_subject(recently_active_subject_name)
        self.caller.experiment.save_experiment_settings()
        self.evokeds_batching_widget.cleanup(self)
        self.initialize_ui()

    def on_pushButtonOpenEvokedStatsDialog_clicked(self, checked=None):
        """Open the evokedStatsDialog for viewing statistical data."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return
        evoked_name = str(item.text())
        self.evokedStatsDialog = EvokedStatsDialog(self, evoked_name)
        self.evokedStatsDialog.show()

    def on_pushButtonVisualizeEpochChannels_clicked(self, checked=None):
        """Plot image over epochs channel"""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.epochList.ui.listWidgetEpochs.count() == 0:
            messagebox(self, 'Create epochs before visualizing.')
            return
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'Please select an epoch collection on the list.'
            messagebox(self, message)
            return
        name = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
        epochs = self.caller.experiment.active_subject.epochs.get(name)
        self.visualizeEpochs = (visualizeEpochChannelDialogMain.
                                VisualizeEpochChannelDialog(epochs))
        self.visualizeEpochs.show()

    def on_pushButtonEpochsPlot_clicked(self, checked=None):
        """Call ``epochs.plot``."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        item = self.epochList.ui.listWidgetEpochs.currentItem()
        if item is None:
            message = 'No epochs collection selected.'
            messagebox(self, message)
            return

        epochs_name = str(item.text())
        epochs = self.caller.experiment.active_subject.epochs.get(epochs_name)

        def handle_close(event):
            fileManager.save_epoch(epochs, overwrite=True)
            self.epochList.selection_changed()
        fig = epochs.raw.plot(block=True, show=True)
        fig.canvas.mpl_connect('close_event', handle_close)

    def on_pushButtonVisualizeEvokedDataset_clicked(self, checked=None):
        """Plot the evoked data as a topology."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return
        layout = ''
        if self.ui.radioButtonSelectLayout.isChecked():
            layout = str(self.ui.comboBoxLayout.currentText())
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
        if layout == '':
            messagebox(self, 'No layout selected!')
            return

        self.ui.pushButtonVisualizeEvokedDataset.setText('      Visualizing...'
                                                         '      ')
        self.ui.pushButtonVisualizeEvokedDataset.setEnabled(False)

        evoked_name = str(item.text())
        evoked = self.caller.experiment.active_subject.evokeds[evoked_name]
        mne_evokeds = evoked.mne_evokeds

        print 'Meggie: Visualizing evoked collection %s...\n' % evoked_name
        try:
	    QtGui.QApplication.setOverrideCursor(
                QtGui.QCursor(QtCore.Qt.WaitCursor))
            self.caller.draw_evoked_potentials(mne_evokeds.values(), layout)
            print 'Meggie: Evoked collection %s visualized!\n' % evoked_name
        except Exception as e:
            exc_messagebox(self, e)
        finally:
            oldText = 'Visualize selected dataset'
            self.ui.pushButtonVisualizeEvokedDataset.setText(oldText)
            self.ui.pushButtonVisualizeEvokedDataset.setEnabled(True)
            QtGui.QApplication.restoreOverrideCursor()

    def on_pushButtonGroupAverage_clicked(self, checked=None):
        """
        Plots topology view of evoked response group averages. Saves the
        results as ascii to ``output`` folder. Uses event names for determining
        which responses to average across subjects.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())

        if self.ui.radioButtonSelectLayout.isChecked():
            layout = self.ui.comboBoxLayout.currentText()
        else:
            layout = str(self.ui.labelLayout.text())

        try:
            evokeds = self.caller.group_average(evoked_name, layout)
        except Exception as e:
            exc_messagebox(self, e)
            return

        self._save_evoked(self.caller.experiment.active_subject, evokeds, 'group_' + evoked_name)

        self.initialize_ui()

    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """Opens a dialog for selecting a layout file."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        fName = str(QtGui.QFileDialog.
                    getOpenFileName(self, "Select a layout file", '/home/',
                                    "Layout-files (*.lout *.lay);;All files "
                                    "(*.*)"))
        self.ui.labelLayout.setText(fName)

    def on_pushButtonDeleteEpochs_clicked(self, checked=None):
        """Delete the selected epoch item and the files related to it."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.epochList.isEmpty():
            return

        elif self.epochList.currentItem() is None:
            messagebox(self, 'No epochs selected')

        item_str = self.epochList.currentItem().text()

        message = 'Permanently remove epochs and the related files?'
        reply = QtGui.QMessageBox.question(self, 'delete epochs',
                                           message, QtGui.QMessageBox.Yes | 
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            try:
                self.caller.experiment.active_subject.remove_epochs(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)
            self.epochList.remove_item(self.epochList.currentItem())
        if self.epochList.ui.listWidgetEpochs.count() == 0:
            self.clear_epoch_collection_parameters()
        self.caller.experiment.save_experiment_settings()

    def on_pushButtonDeleteEvoked_clicked(self, checked=None):
        """Delete the selected evoked item and the files related to it."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.listWidgetEvoked.count() == 0:
            return

        elif self.ui.listWidgetEvoked.currentItem() is None:
            messagebox(self, 'No evokeds selected.')

        item_str = self.ui.listWidgetEvoked.currentItem().text()

        message = 'Permanently remove evokeds and the related files?'
        reply = QtGui.QMessageBox.question(self, 'delete evokeds',
                                           message, QtGui.QMessageBox.Yes | 
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            item = self.ui.listWidgetEvoked.currentItem()
            row = self.ui.listWidgetEvoked.row(item)
            self.ui.listWidgetEvoked.takeItem(row)
            self.ui.listWidgetInverseEvoked.takeItem(row)
            try:
                self.caller.experiment.active_subject.remove_evoked(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)
            self.caller.experiment.save_experiment_settings()


    def on_pushButtonDeletePower_clicked(self, checked=None):
        """Delete the selected power item and the files related to it."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.listWidgetPowerItems.count() == 0:
            return

        elif self.ui.listWidgetPowerItems.currentItem() is None:
            messagebox(self, 'No power selected.')
            return

        item_str = self.ui.listWidgetPowerItems.currentItem().text()
        message = 'Delete power item?'
        reply = QtGui.QMessageBox.question(self, 'delete power',
                                           message, QtGui.QMessageBox.Yes | 
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            item = self.ui.listWidgetPowerItems.currentItem()
            row = self.ui.listWidgetPowerItems.row(item)
            self.ui.listWidgetPowerItems.takeItem(row)
            try:
                self.caller.experiment.active_subject.remove_power(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)
        else:
            return

    def on_pushButtonRawPlot_clicked(self, checked=None):
        """Call ``raw.plot``."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        def handle_close(event):
            raw = self.caller.experiment.active_subject.get_working_file()
            fname = self.caller.experiment.active_subject.get_working_file().info['filename']
            fileManager.save_raw(self.caller.experiment, raw, fname, overwrite=True)
            
            self.initialize_ui()
            bads = self.caller.experiment.active_subject.get_working_file().info['bads']
            self.caller.experiment.action_logger.log_message('Raw plot bad channels selected for file: ' + fname + '\n' + str(bads))
        if self.ui.checkBoxShowEvents.isChecked():
            events = self.caller.experiment.active_subject.get_events()
        else:
            events = None
        try:
            raw = self.caller.experiment.active_subject.get_working_file()
            fig = raw.plot(block=True, show=True, events=events)
            fig.canvas.mpl_connect('close_event', handle_close)
        except Exception, err:
            exc_messagebox(self, err)
            return

    def on_pushButtonMNE_Browse_Raw_clicked(self, checked=None):
        """Call mne_browse_raw."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return
        
        info = self.caller.experiment.active_subject.get_working_file().info
        try:
            self.caller.call_mne_browse_raw(info['filename'])
        except Exception, err:
            exc_messagebox(self, err)
            return

    def on_pushButtonMNE_Browse_Raw_2_clicked(self, checked=None):
        """Call mne_browse_raw."""
        if self.caller.experiment.active_subject is None:
            return

        self.on_pushButtonMNE_Browse_Raw_clicked(checked)

    def on_pushButtonPlotProjections_clicked(self, checked=None):
        """Plots added projections as topomaps."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        raw = self.caller.experiment.active_subject.get_working_file()

        try:
            self.caller.plot_projs_topomap(raw)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonMaxFilter_clicked(self, checked=None):
        """
        Call Elekta's MaxFilter.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        try:
            self.maxFilterDialog = MaxFilterDialog(self)
        except Exception, err:
            exc_messagebox(self, err)
            return
        self.maxFilterDialog.show()

    def on_pushButtonSpectrum_clicked(self, checked=None):
        """Open the power spectrum visualization dialog."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.spectrumDialog = PowerSpectrumDialog(self)
        self.spectrumDialog.finished.connect(self.on_close)
        self.spectrumDialog.show()

    def on_pushButtonEOG_clicked(self, checked=None):
        """Open the dialog for calculating the EOG PCA."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        
        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.computed.connect(self.ui.checkBoxEOGComputed.setChecked)
        self.eogDialog.show()

    def on_pushButtonECG_clicked(self, checked=None):
        """Open the dialog for calculating the ECG PCA."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.ecgDialog = EcgParametersDialog(self)
        self.ecgDialog.show()

    def on_pushButtonApplyEOG_clicked(self, checked=None):
        """Open the dialog for applying the EOG-projections to the data."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        info = self.caller.experiment.active_subject.get_working_file().info
        self.addEogProjs = AddEOGProjections(self, info['projs'])
        self.addEogProjs.exec_()

    def on_pushButtonApplyECG_clicked(self, checked=None):
        """Open the dialog for applying the ECG-projections to the data."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return
        
        info = self.caller.experiment.active_subject.get_working_file().info
        self.addEcgProjs = AddECGProjections(self, info['projs'])
        self.addEcgProjs.exec_()

    def on_pushButtonTFR_clicked(self, checked=None):
        """Open the dialog for plotting TFR from a single channel."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return
        
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must create epochs before TFR.'
            messagebox(self, message)
            return
        name = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
        epochs = self.caller.experiment.active_subject.epochs.get(name)

        self.tfr_dialog = TFRDialog(self, epochs)
        self.tfr_dialog.finished.connect(self.on_close)
        self.tfr_dialog.show()

    def on_pushButtonTFRTopology_clicked(self, checked=None):
        """Opens the dialog for plotting TFR topology."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must select the epochs for TFR.'
            messagebox(self, message)
            return
        name = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
        self.tfrTop_dialog = TFRTopologyDialog(self, name)
        self.tfrTop_dialog.finished.connect(self.on_close)
        self.tfrTop_dialog.show()

    def on_pushButtonTFRTopology_2_clicked(self, checked=None):
        """Visualize existing AVGPower as topology."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        item = self.ui.listWidgetPowerItems.currentItem()
        if item is None:
            return
        power_name = item.text()
        subject = self.caller.experiment.active_subject
        path = os.path.join(subject.subject_path, 'TFR')
        fname = os.path.join(path, power_name)
        tfr = fileManager.load_tfr(fname)
        self.tfrTop_dialog = TFRTopologyDialog(self, None, tfr)
        self.tfrTop_dialog.finished.connect(self.on_close)
        self.tfrTop_dialog.show()

    def on_pushButtonChannelAverages_clicked(self, checked=None):
        """Shows the channels average graph."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return
        
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'Please select an epoch collection to channel average.'
            messagebox(self, message)
            return
        name = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
        
        if self.ui.radioButtonLobe.isChecked():
            try:
                self.caller.average_channels(name,
                                             self.ui.comboBoxLobes.currentText(),
                                             None)
            except Exception as e:
                exc_messagebox(self, e)
            #TODO: visualizing actions logged or not?
            #TODO: this actually works, but user must know this is only a visualization call and a non-MNE method
            #TODO: weird error occurred, not sure if it was this code or something else, couldnt replicate
            #wrap_mne_call(self.caller.experiment, self.caller.average_channels, name, self.ui.comboBoxLobes.currentText(), None)
        else:
            channels = []
            for i in xrange(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                channels.append(str(item.text()))
            try:
                self.caller.average_channels(name, None, set(channels))
            except Exception as e:
                exc_messagebox(self, e)
            #TODO: visualizing actions logged or not?
            #TODO: this actually works, but user must know this is only a visualization call and a non-MNE method
            #TODO: weird error occurred, not sure if it was this code or something else, couldnt replicate
            #wrap_mne_call(self.caller.experiment, self.caller.average_channels, name, None, set(channels))

    def on_pushButtonModifyChannels_clicked(self, checked=None):
        """
        Slot for adding channels to the list for averaging epochs.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        channels = list()
        for i in xrange(self.ui.listWidgetChannels.count()):
            item = self.ui.listWidgetChannels.item(i)
            channels.append(str(item.text()))

        channelDialog = ChannelSelectionDialog(channels, 'Select channels')
        channelDialog.channelsChanged.connect(self.channels_modified)
        channelDialog.exec_()

    @QtCore.pyqtSlot(list)
    def channels_modified(self, channels):
        """
        Slot for signal from channelSelectionDialog.
        Adds selected channels to the list for averaging.
        Keyword arguments:
        channels -- Channels to add to the list.
        """
        self.ui.listWidgetChannels.clear()
        self.ui.listWidgetChannels.addItems(channels)

    def on_pushButtonFilter_clicked(self, checked=None):
        """
        Show the dialog for filtering.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.filterDialog = FilterDialog(self)
        self.filterDialog.finished.connect(self.on_close)
        self.filterDialog.show()

    def on_pushButtonActivateSubject_clicked(self, checked=None):
        """
        Activates a subject.
        """
        if checked is None:
            return
        if self.ui.listViewSubjects.selectedIndexes() == []:
            return

        selIndexes = self.ui.listViewSubjects.selectedIndexes()
        
        if len(selIndexes) > 1:
            return
        
        subject_name = selIndexes[0].data()

        # Not much point trying to activate an already active subject.
        if self.caller.experiment.active_subject:
            if subject_name == self.caller.experiment.active_subject.subject_name:
                return
        # This prevents taking the epoch list currentItem from the previously
        # open subject when activating another subject.
        self.clear_epoch_collection_parameters()
        try:
            self.caller.activate_subject(subject_name)
        except Exception as e:
            exc_messagebox(self, e)
        self.initialize_ui()

        # To tell the MVC models that the active subject has changed.
        self.reinitialize_models()

    def on_pushButtonBrowseRecon_clicked(self, checked=None):
        """
        Copies reconstructed mri files from the directory supplied by the user
        to the corresponding directory under the active subject directory
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        activeSubject = self.caller.experiment.active_subject

        if activeSubject.check_reconFiles_copied():
            reply = QtGui.QMessageBox.question(self, 'Please confirm',
                                               "Do you really want to change "
                                               "the reconstructed files? This "
                                               "will invalidate all later "
                                               "source analysis work and "
                                               "clear the results of the "
                                               "later phases",
                                               QtGui.QMessageBox.Yes | 
                                               QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.No:
                return

        path = str(QtGui.QFileDialog.getExistingDirectory(self,
                                                          "Select directory "
                                                          "of the "
                                                          "reconstructed "
                                                          "MRI image"))
        if path == '':
            return

        mriDir = os.path.join(path, 'mri')
        surfDir = os.path.join(path, 'surf')
        if not (os.path.isdir(mriDir) and os.path.isdir(surfDir)):
            msg = ("Reconstructed image directory should have both 'surf' "
                   "and 'mri' directories in it.")
            messagebox(self, msg)
            return

        try:
            fileManager.copy_recon_files(activeSubject, path)
            self.ui.lineEditRecon.setText(path)
        except Exception:
            msg = ('Could not copy files. Either the disk is full , you have '
                   'no rights to read the directory or something weird '
                   'happened.')
            messagebox(self, msg)

        self.initialize_ui()

    def on_pushButtonConvertToMNE_clicked(self, checked=None):
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        try:
            self.caller.convert_mri_to_mne()
        except Exception as e:
            exc_messagebox(self, e)

        self.initialize_ui()

    def on_pushButtonCreateNewForwardModel_clicked(self, checked=None):
        """
        Open up a dialog for creating a new forward model.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.fmodelDialog = ForwardModelDialog(self)
        self.fmodelDialog.show()

    def on_pushButtonRemoveSelectedForwardModel_clicked(self, checked=None):
        """
        Removes selected forward model from the forward model list and
        from the disk.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.tableViewForwardModels.selectedIndexes() == []:
            message = 'Please select a forward model to remove.'
            messagebox(self, message)
            return

        reply = QtGui.QMessageBox.question(self, 'Removing forward model',
                                           'Do you really want to remove the '
                                           'selected forward model, including '
                                           'the coregistration and forward '
                                           'solution files related to it?',
                                           QtGui.QMessageBox.Yes | 
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.No:
            return

        tableView = self.ui.tableViewForwardModels

        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedRowNumber = selectedRowIndexes[0].row()
        fmname = selectedRowIndexes[0].data()
        subject = self.caller.experiment.active_subject

        try:
            fileManager.remove_fModel_directory(fmname, subject)
            self.forwardModelModel.removeRows(selectedRowNumber)
        except Exception:
            msg = ('There was a problem removing forward model. Nothing was '
                   'removed.')
            messagebox(self, msg)

    def on_pushButtonBrowseCoregistration_clicked(self, checked=None):
        """
        Open a file browser dialog for the user to choose
        a translated coordinate file to use with the currently selected forward
        model.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        activeSubject = self._experiment._active_subject
        tableView = self.ui.tableViewFModelsForCoregistration

        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedFmodelName = selectedRowIndexes[0].data()

        subjectPath = activeSubject._subject_path
        targetName = os.path.join(subjectPath, 'sourceAnalysis',
                                  'forwardModels', selectedFmodelName,
                                  'reconFiles', 'reconFiles-trans.fif')

        path = QtGui.QFileDialog.getOpenFileName(self, 'Select the existing '
                                                 'coordinate file (the file '
                                                 'should end with '
                                                 '"-trans.fif")')
        if path == '':
            return
        else:
            try:
                shutil.copyfile(path, targetName)
            except IOError:
                msg = 'There was a problem while copying the coordinate file.'
                messagebox(self, msg)

        self.forwardModelModel.initialize_model()

    def on_pushButtonMNECoregistration_clicked(self, checked=None):
        """
        Open a dialog for coregistering the currently selected
        forward model in tableViewFModelsForCoregistration.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.tableViewFModelsForCoregistration.selectedIndexes() == []:
            msg = 'Please select a forward model to (re-)coregister.'
            messagebox(self, msg)
            return

        self.caller.coregister_with_mne_gui_coregistration()

    def on_pushButtonCreateForwardSolution_clicked(self, checked=None):
        """
        Open a dialog for creating a forward solution for the currently
        selected forward model in tableViewFModelsForSolution.
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        if self.ui.tableViewFModelsForSolution.selectedIndexes() == []:
            message = ('Please select a forward model to (re)create a forward '
                       'solution for.')
            messagebox(self, message)
            return

        self.fSolutionDialog = ForwardSolutionDialog(self)
        self.fSolutionDialog.show()

    def on_pushButtonMNE_AnalyzeCoregistration_clicked(self, checked=None):
        if checked is None:
            return
        # TODO: Implement this last if needed.
        return

    def on_pushButtonComputeCovarianceRaw_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on raw file
        (measurement file with a subject but without epochs, or an empty room
        measurement).
        """
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        self.covarianceRawDialog = CovarianceRawDialog(self)
        self.covarianceRawDialog.show()

    def on_pushButtonComputeCovarianceEpochs_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on data
        before epochs.
        """
        # TODO:
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return


    def on_pushButtonComputeInverse_clicked(self, checked=None):
        """Compute inverse operator clicked."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        fwd_name = str(self.ui.listWidgetForwardSolution.currentItem().text())
        inv = self.caller.compute_inverse(fwd_name)
        _initializeInverseOperatorList(self.ui.listWidgetInverseOperator,
                                       self.caller.experiment.active_subject)

    def on_pushButtonMakeSourceEstimate_clicked(self, checked=None):
        """Make source estimate clicked."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        ui = self.ui
        if ui.radioButtonRaw.isChecked():
            inst_name = self.caller.experiment.active_subject.subject_name
            type = 'raw'
        elif ui.radioButtonEpoch.isChecked():
            inst_name = str(self.epochList.currentItem().text())
            type = 'epochs'
        elif ui.radioButtonEvoked.isChecked():
            inst_name = str(ui.listWidgetInverseEvoked.currentItem().text())
            type = 'evoked'
        dir = self.caller.experiment.active_subject._source_analysis_directory
        self.sourceEstimateDialog = SourceEstimateDialog(self, inst_name, type)
        self.sourceEstimateDialog.stc_computed.connect(self.
            _update_source_estimates)
        self.sourceEstimateDialog.show()


    def _update_source_estimates(self):
        """Helper for updating source estimates to list."""
        self.ui.listWidgetSourceEstimate.clear()
        subject = self.caller.experiment.active_subject
        dir = subject._stc_directory
        stcs = [f for f in os.listdir(dir) if
                os.path.isfile(os.path.join(dir, f)) and f.endswith('lh.stc')]
        for stc in stcs:
            if os.path.isfile(os.path.join(dir, stc[:-6] + 'rh.stc')):
                self.ui.listWidgetSourceEstimate.addItem(stc[:-7])


    def on_pushButtonVisStc_clicked(self, checked=None):
        """Visualize source estimates."""
        if checked is None:
            return
        if self.caller.experiment.active_subject is None:
            return

        stc = str(self.ui.listWidgetSourceEstimate.currentItem().text())
        self.plotStcDialog = PlotStcDialog(self, stc)
        self.plotStcDialog.show()

# Code for UI initialization (when starting the program) and
# updating when something changes

    def initialize_ui(self):
        """
        Method for setting up the GUI. Called whenever a subject is activated,
        either via creation of a new subject or change of an active subject.
        Also called when anything that can affect UI state has been run.
        Checks the existence of a ton of files and sets the GUI fields to
        reflect the state of the experiment and subject according to them.
        """

        # Clear the lists.
        self.clear_epoch_collection_parameters()
        self.epochList.clearItems()
        self.ui.listWidgetEvoked.clear()
        self.ui.listWidgetInverseEvoked.clear()

        # Clears and sets labels, checkboxes etc. on mainwindow.
        self.ui.textBrowserEvents.clear()
        self.ui.labelDateValue.clear()
        self.ui.labelLengthValue.clear()
        self.ui.labelEEGValue.clear()
        self.ui.labelGradMEGValue.clear()
        self.ui.labelHighValue.clear()
        self.ui.labelLowValue.clear()
        self.ui.labelMagMEGValue.clear()
        self.ui.labelSamplesValue.clear()
        self.ui.labelSubjectValue.clear()
        self.ui.listWidgetProjs.clear()
        self.ui.listWidgetBads.clear()
        self.ui.checkBoxMaxFilterComputed.setChecked(False)
        self.ui.checkBoxMaxFilterApplied.setChecked(False)
        self.ui.checkBoxECGComputed.setChecked(False)
        self.ui.checkBoxECGApplied.setChecked(False)
        self.ui.checkBoxEOGComputed.setChecked(False)
        self.ui.checkBoxEOGApplied.setChecked(False)
        self.ui.checkBoxConvertedToMNE.setChecked(False)
        self.ui.lineEditRecon.setText('')

        # Deactivate various buttons. They will be
        # activated later if prerequisites are met.
        self.ui.pushButtonApplyECG.setEnabled(False)
        self.ui.pushButtonApplyEOG.setEnabled(False)
        self.ui.pushButtonConvertToMNE.setEnabled(False)
        self.ui.pushButtonCheckTalairach.setEnabled(False)
        self.ui.pushButtonSkullStrip.setEnabled(False)
        self.ui.pushButtonCheckSurfaces.setEnabled(False)
        self.ui.pushButtonCheckSegmentations.setEnabled(False)
        #self.ui.pushButtonCreateNewForwardModel.setEnabled(False)
                
        self.setWindowTitle('Meggie - ' + self.caller.experiment.experiment_name)

        if self.caller.experiment.active_subject is None:
            self.statusLabel.setText('Add or activate subjects before '
                                     'continuing.')
            return
        
        self.update_power_list()

        name = self.caller.experiment.active_subject.working_file_name
        status = "Current working file: " + name
        
        self.statusLabel.setText(status)
        #self.ui.

        # Check whether ECG projections are calculated
        if self.caller.experiment.active_subject.check_ecg_projs():
            self.ui.pushButtonApplyECG.setEnabled(True)
            self.ui.checkBoxECGComputed.setChecked(True)
        # Check whether EOG projections are calculated
        if self.caller.experiment.active_subject.check_eog_projs():
            self.ui.pushButtonApplyEOG.setEnabled(True)
            self.ui.checkBoxEOGComputed.setChecked(True)
        # Check whether ECG projections are applied
        if self.caller.experiment.active_subject.check_ecg_applied():
            self.ui.checkBoxECGApplied.setChecked(True)
        # Check whether EOG projections are applied
        if self.caller.experiment.active_subject.check_eog_applied():
            self.ui.checkBoxEOGApplied.setChecked(True)
        # Check whether sss/tsss method is applied.
        if self.caller.experiment.active_subject.check_sss_applied():
            self.ui.checkBoxMaxFilterComputed.setChecked(True)
            self.ui.checkBoxMaxFilterApplied.setChecked(True)

        # Populate subject list
        # Subject list is populated by calling reinitialize_models()
        # in mainwindow
        
        # Populate epoch and evoked lists        
        raw = self.caller.experiment.active_subject.get_working_file()
        active_sub = self.caller.experiment.active_subject

        epochs_items = self.caller.experiment.active_subject.epochs
        evokeds_items = self.caller.experiment.active_subject.evokeds
        if epochs_items is not None:
            for epoch in epochs_items.values():
                self.epochList.ui.listWidgetEpochs.addItem(epoch.collection_name)

        if evokeds_items is not None:
            for evoked in evokeds_items.values():
                self.ui.listWidgetEvoked.addItem(evoked.name)
                self.ui.listWidgetInverseEvoked.addItem(evoked.name)

        # This updates the 'Subject info' section below the subject list.
        try:
            InfoDialog(raw, self.ui, False)
            self.populate_raw_tab_event_list()
        except Exception as err:
            exc_messagebox(self, err)
            return

        # Check whether reconstructed mri files have been copied to the recon
        # files directory under the subject and set up the UI accordingly.
        if self.caller.experiment.active_subject.check_reconFiles_copied():
            self.ui.lineEditRecon.setText('Reconstructed mri image already '
                                          'copied.')
            self.ui.pushButtonConvertToMNE.setEnabled(True)
            self.ui.pushButtonCheckTalairach.setEnabled(True)
            self.ui.pushButtonSkullStrip.setEnabled(True)
            self.ui.pushButtonCheckSurfaces.setEnabled(True)
            self.ui.pushButtonCheckSegmentations.setEnabled(True)

        # Check if MRI image has been setup with mne_setup_forward solution
        if self.caller.experiment.active_subject.check_mne_setup_mri_run():
            self.ui.checkBoxConvertedToMNE.setChecked(True)
            self.ui.pushButtonCreateNewForwardModel.setEnabled(True)

        projs = raw.info['projs']
        for proj in projs:
            self.ui.listWidgetProjs.addItem(str(proj))

        bads = raw.info['bads']
        for bad in bads:
            self.ui.listWidgetBads.addItem(bad)

        _initializeInverseOperatorList(self.ui.listWidgetInverseOperator,
                                       self.caller.experiment.active_subject)
        self.update_covariance_info_box()
        self._update_source_estimates()

    def update_power_list(self):
        """Updates the TFR list."""
        self.ui.listWidgetPowerItems.clear()
        active_sub = self.caller.experiment.active_subject
        power_items = fileManager.load_powers(active_sub)
        if len(power_items) > 0:
            for item in power_items:
                self.ui.listWidgetPowerItems.addItem(item)

    def update_covariance_info_box(self):
        """
        Fills the info box in the covariance tab with info about the
        current covariance matrix info for the active subject, if said info
        exists.
        """
        path = self.caller.experiment.active_subject._source_analysis_directory
        cvParamFilePath = os.path.join(path, 'covariance.param')

        cvdict = None
        if os.path.isfile(cvParamFilePath):
            try:
                cvdict = fileManager.unpickle(cvParamFilePath)
            except Exception:
                pass

        if self.ui.frameCovarianceInfoWidget.layout() is not None:
            sip.delete(self.ui.frameCovarianceInfoWidget.layout())

        for child in self.ui.frameCovarianceInfoWidget.children():
            child.setParent(None)

        covLayout = QtGui.QGridLayout()
        self.ui.frameCovarianceInfoWidget.setLayout(covLayout)

        if cvdict is None:
            covarianceWidgetNone = CovarianceWidgetNone()
            covLayout.addWidget(covarianceWidgetNone)
            return

        if cvdict['covarianceSource'] == 'raw':
            covarianceWidgetRaw = CovarianceWidgetRaw()
            cvwui = covarianceWidgetRaw.ui
            if cvdict['rawsubjectname'] is not None:
                cvwui.textBrowserBasedOn.setText(cvdict['rawsubjectname'])
            else:
                cvwui.textBrowserBasedOn.setText(cvdict['rawfilepath'])
            cvwui.textBrowserTmin.setText(str(cvdict['starttime']))
            cvwui.textBrowserTmax.setText(str(cvdict['endtime']))
            cvwui.textBrowserTstep.setText(str(cvdict['tstep']))
            if cvdict['reject'] is not None:
                txt = str(cvdict.get('reject').get('grad', ''))
                cvwui.textBrowserGradPeakCovariance.setText(txt)
                txt = str(cvdict.get('reject').get('mag', ''))
                cvwui.textBrowserMagPeakCovariance.setText(txt)
                txt = str(cvdict.get('reject').get('eeg', ''))
                cvwui.textBrowserEEGPeakCovariance.setText(txt)
                txt = str(cvdict.get('reject').get('eog', ''))
                cvwui.textBrowserEOGPeakCovariance.setText(txt)
            if cvdict['flat'] is not None:
                txt = str(cvdict.get('flat').get('grad', ''))
                cvwui.textBrowserFlatGrad.setText(txt)
                txt = str(cvdict.get('flat').get('mag', ''))
                cvwui.textBrowserFlatMag.setText(txt)
                txt = str(cvdict.get('flat').get('eeg', ''))
                cvwui.textBrowserFlatEEG.setText(txt)
                txt = str(cvdict.get('flat').get('eog', ''))
                cvwui.textBrowserFlatEOG.setText(txt)
                txt = str(cvdict.get('flat').get('ecg', 'Not used'))
                cvwui.textBrowserFlatECG.setText(txt)
            covLayout.addWidget(covarianceWidgetRaw)

        if cvdict['covarianceSource'] == 'epochs':
            # TODO: implement this functionality, then use existing
            # CovarianceWidgetEpochs
            pass

    def populate_raw_tab_event_list(self):
        """
        Fill the raw tab event list with info about event IDs and
        amount of events with those IDs.
        """
        # TODO: trigger ---> event, also in the UI
        events = self.caller.experiment.active_subject.create_event_set()
        if events is None:
            return
        events_string = ''
        for key, value in events.iteritems():
            events_string += 'Trigger %s, %s events\n' % (str(key), str(value))
        self.ui.textBrowserEvents.setText(events_string)

    def populate_comboBoxLobes(self):
        """
        Populate the combo box listing available lobes for to use for
        channel averaging.
        """
        self.ui.comboBoxLobes.clear()
        self.ui.comboBoxLobes.addItem('Vertex')
        self.ui.comboBoxLobes.addItem('Left-temporal')
        self.ui.comboBoxLobes.addItem('Right-temporal')
        self.ui.comboBoxLobes.addItem('Left-parietal')
        self.ui.comboBoxLobes.addItem('Right-parietal')
        self.ui.comboBoxLobes.addItem('Left-occipital')
        self.ui.comboBoxLobes.addItem('Right-occipital')
        self.ui.comboBoxLobes.addItem('Left-frontal')
        self.ui.comboBoxLobes.addItem('Right-frontal')

    def add_tabs(self):
        """Method for initializing the tabs."""
        self.ui.tabWidget.insertTab(1, self.ui.tabPreprocessing,
                                    "Preprocessing")
        self.ui.tabWidget.insertTab(2, self.ui.tabEpoching, "Epoching")
        self.ui.tabWidget.insertTab(3, self.ui.tabAveraging, "Averaging")
        self.ui.tabWidget.insertTab(4, self.ui.tabTFR, "TFR")
        self.ui.tabWidget.insertTab(5, self.ui.tabSourcePreparation,
                                    "Source modelling preparation")
        self.ui.tabWidget.insertTab(6, self.ui.tabForwardModel,
                                    "Forward model creation")
        self.ui.tabWidget.insertTab(7, self.ui.tabCoregistration,
                                    "Coregistration")
        self.ui.tabWidget.insertTab(8, self.ui.tabForwardSolution,
                                    "Forward solution creation")
        self.ui.tabWidget.insertTab(9, self.ui.tabNoiseCovariance,
                                    "Noise covariance")
        self.ui.tabWidget.insertTab(10, self.ui.tabInverseOperator,
                                    "Inverse operator")
        self.ui.tabWidget.insertTab(11, self.ui.tabSourceEstimate,
                                    "Source estimate")
        self.ui.tabWidget.insertTab(12, self.ui.tabSourceAnalysis,
                                    "Source analysis")

    def on_currentChanged(self):
        """
        TODO: should use a proper mcv system to avoid this crap.
        Keep track of the active tab.
        Show the epoch collection list epochList when in appropriate tabs.
        """
        index = self.ui.tabWidget.currentIndex()
        if index == 1:
            mode = QtGui.QAbstractItemView.SingleSelection
            self.epochList.ui.groupBoxEvents.setVisible(True)
            self.epochList.setParent(self.ui.groupBoxEpochsEpoching)
        elif index == 2:
            mode = QtGui.QAbstractItemView.MultiSelection
            self.epochList.ui.groupBoxEvents.setVisible(True)
            self.epochList.setParent(self.ui.groupBoxEpochsAveraging)
        elif index == 3:
            mode = QtGui.QAbstractItemView.SingleSelection
            self.epochList.ui.groupBoxEvents.setVisible(True)
            self.epochList.setParent(self.ui.groupBoxEpochsTFR)
        elif index == 10:
            mode = QtGui.QAbstractItemView.SingleSelection
            self.epochList.ui.groupBoxEvents.setVisible(False)
            self.epochList.setParent(self.ui.frameInverseEpochs)
        else:
            self.epochList.hide()
            return
        self.epochList.ui.listWidgetEpochs.setSelectionMode(mode)
        self.epochList.show()

        if index == 10:
            self.ui.listWidgetSourceEstimate.setParent(self.ui.groupBox_23)
        elif index == 11:
            self.ui.listWidgetSourceEstimate.setParent(self.ui.groupBox_24)


    def reinitialize_models(self):
        """
        Tell all the MVC models of the views in Meggie that they should
        (re)initialize themselves. Should only be needed when active subject
        changes, updating the models when items are added to them is based
        on events.
        """
        self.forwardModelModel.initialize_model()
        self.subjectListModel.initialize_model()
        if self.caller.experiment.active_subject:
            _initializeForwardSolutionList(self.ui.listWidgetForwardSolution,
                self.caller.experiment.active_subject)

    def collect_parameter_values(self):
        #TODO: clear batchingWidget data after group average
        collection_names = [str(item.text()) for item 
                in self.epochList.ui.listWidgetEpochs.selectedItems()]
        return collection_names        

# Miscellaneous code:

    def directOutput(self):
        """
        Method for directing stdout to the console and back.
        """
        if self.ui.actionDirectToConsole.isChecked():
            sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
            sys.stderr = EmittingStream(textWritten=self.errorOutputWritten)
        else:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def check_workspace(self):
        """
        Open the preferences dialog, in this case for choosing the workspace.
        """
        preferencesDialog = PreferencesDialog(self)
        preferencesDialog.exec_()

    def hide_workspace_option(self):
        self.ui.actionSet_workspace.setVisible(False)

    def __del__(self):
        """
        Restores stdout at the end.
        """
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
 
    def normalOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stdout.
        Parameters:
        text - Text to write to the console.
        """
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()
 
    def errorOutputWritten(self, text):
        """
        Appends text to 'console' at the bottom of the dialog.
        Used for redirecting stderr.
        Parameters:
        text - Text to write to the console.
        """
        cursor = self.ui.textEditConsole.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.ui.textEditConsole.setTextCursor(cursor)
        self.ui.textEditConsole.ensureCursorVisible()

    @QtCore.pyqtSlot(int)
    def on_close(self, result):
        """
        Slot to be called on close of dialogs. Frees the memory by setting the
        dialog as None.
        Parameters:
        result - Integer indicating the result from the dialog (accept,
                                                                reject).
        """
        sender = self.sender()
        if sender is self.spectrumDialog:
            self.spectrumDialog = None
        elif sender is self.filterDialog:
            self.filterDialog = None
        elif sender is self.epochParameterDialog:
            self.epochParameterDialog = None
        elif sender is self.tfr_dialog:
            self.tfr_dialog = None
        elif sender is self.tfrTop_dialog:
            self.tfrTop_dialog = None
        sender.deleteLater()


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass


def main():

    app = QtGui.QApplication(sys.argv)
    window = MainWindow(app)

    window.showMaximized()
    
    sys.exit(app.exec_())
