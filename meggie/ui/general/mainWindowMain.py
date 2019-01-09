# coding: utf-8

"""
"""

import os
import sys
import warnings
import gc
import logging

import matplotlib
matplotlib.use('Qt5Agg')

import numpy as np
import matplotlib.pyplot as plt

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.Qt import QApplication

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.ui.icons import mainWindowIcons_rc

from meggie.ui.general.mainWindowUi import Ui_MainWindow
from meggie.ui.general.createExperimentDialogMain import CreateExperimentDialog
from meggie.ui.general.addSubjectDialogMain import AddSubjectDialog
from meggie.ui.general.layoutDialogMain import LayoutDialog
from meggie.ui.general.infoDialogMain import InfoDialog
from meggie.ui.epoching.eventSelectionDialogMain import EventSelectionDialog
from meggie.ui.analysis import visualizeEpochChannelDialogMain
from meggie.ui.preprocessing.eogParametersDialogMain import EogParametersDialog
from meggie.ui.preprocessing.ecgParametersDialogMain import EcgParametersDialog
from meggie.ui.preprocessing.eegParametersDialogMain import EegParametersDialog
from meggie.ui.preprocessing.badChannelsDialogMain import BadChannelsDialog
from meggie.ui.general.preferencesDialogMain import PreferencesDialog
from meggie.ui.preprocessing.addECGProjectionsMain import AddECGProjections
from meggie.ui.preprocessing.addEOGProjectionsMain import AddEOGProjections
from meggie.ui.preprocessing.filterDialogMain import FilterDialog
from meggie.ui.preprocessing.icaDialogMain import ICADialog
from meggie.ui.widgets.epochWidgetMain import EpochWidget
from meggie.ui.general.aboutDialogMain import AboutDialog
from meggie.ui.general.experimentInfoDialogMain import ExperimentInfoDialog
from meggie.ui.general.logDialogMain import LogDialog
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget
from meggie.ui.utils.decorators import threaded

from meggie.ui.general.tabs.mainWindowTabSourceAnalysisMain import MainWindowTabSourceAnalysis
from meggie.ui.general.tabs.mainWindowTabSpectrumsMain import MainWindowTabSpectrums
from meggie.ui.general.tabs.mainWindowTabInducedMain import MainWindowTabInduced

from meggie.code_meggie.general import experiment
from meggie.code_meggie.general.experiment import Experiment
from meggie.code_meggie.general.preferences import PreferencesHandler
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.structures.evoked import Evoked
from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.analysis.epoching import draw_evoked_potentials
from meggie.code_meggie.analysis.epoching import group_average
from meggie.code_meggie.analysis.epoching import average_channels
from meggie.code_meggie.preprocessing.projections import plot_projs_topomap


class MainWindow(QtWidgets.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """

    def __init__(self, application):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.experiment = None

        self.setup_loggers()        

        # Direct output to console
        if 'debug' not in sys.argv:
            self.directOutput()
            self.ui.actionDirectToConsole.triggered.connect(self.directOutput)
        # For storing and handling program wide prefences.
        self.preferencesHandler = PreferencesHandler()
        self.preferencesHandler.set_env_variables()

        # For handling initialization and switching of experiments.
        self.experimentHandler = experiment.ExperimentHandler(self)

        # Create the tab contents
        self.mainWindowTabSpectrums = MainWindowTabSpectrums(self)
        self.mainWindowTabSourceAnalysis = MainWindowTabSourceAnalysis(self)
        self.mainWindowTabInduced = MainWindowTabInduced(self)

        # Creates a label on status bar to show current working file message.
        self.statusLabel = QtWidgets.QLabel()
        self.ui.statusbar.addWidget(self.statusLabel)

        # Creates a listwidget for epoch analysis.
        self.epochList = EpochWidget(self, epoch_getter=self.get_epochs,
            parameter_setter=self.show_epoch_collection_parameters)
        self.epochList.hide()

        self.ui.listWidgetEvoked.setMinimumWidth(346)
        self.ui.listWidgetEvoked.setMaximumWidth(346)

        self.evokeds_batching_widget = BatchingWidget(
            self.experiment,
            self, self.ui.widget,
            self.ui.pushButtonCreateEvoked,
            self.ui.pushButtonCreateEvokedBatch,
            self.evoked_selection_changed,
            self.collect_evoked_parameter_values,
        )
 
        # Populate the combobox for selecting lobes for channel averages.
        self.populate_comboBoxLobes()

        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)

        # If the user has chosen to open the previous experiment automatically.
        if self.preferencesHandler.auto_load_last_open_experiment:
            exp = None
            
            try:
                exp = self.experimentHandler.open_existing_experiment(
                    self.preferencesHandler)
            except Exception as e:
                exc_messagebox(self, e)
            
            if exp:
                self.experiment = exp
                self.initialize_ui()
            else:
                self.preferencesHandler.previous_experiment_name = ''
                self.preferencesHandler.write_preferences_to_disk()


        # Select the first item on epoch list
        if self.epochList.ui.listWidgetEpochs.count() > 1:
            self.epochList.ui.listWidgetEpochs.setCurrentRow(0)

        # Set bads not selectable
        self.ui.listWidgetBads.setSelectionMode(QAbstractItemView.NoSelection)


    def get_epochs(self, epoch_name):
        experiment = self.experiment
        if not experiment:
            return
        
        active_subject = experiment.active_subject
        if not active_subject:
            return

        return active_subject.epochs.get(epoch_name)


    def on_actionQuit_triggered(self, checked=None):
        """Closes the program, possibly after a confirmation by the user."""
        if checked is None:
            return

        if self.preferencesHandler.confirm_quit:
            reply = QtWidgets.QMessageBox.question(self, 'Close Meggie',
                'Are you sure you want to quit Meggie?', 
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
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

    def on_actionOpen_experiment_triggered(self, checked=None):
        """ Open an existing _experiment. """

        if checked is None:
            return

        if self.experiment is not None:
            directory = self.experiment.workspace
        else:
            directory = ''

        path = str(QtWidgets.QFileDialog.getExistingDirectory
                   (self, "Select _experiment directory", directory))

        if path == '':
            return
        
        logging.getLogger('ui_logger').info('Opening experiment ' + path)

        try:
            exp = self.experimentHandler.open_existing_experiment(
                self.preferencesHandler, path=path)
            self.experiment = exp
            self.initialize_ui()
        except Exception as e:
            exc_messagebox(self, e)

        # Saves at least the previous experiment name
        self.preferencesHandler.write_preferences_to_disk()

    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """Open subject dialog."""

        if checked is None:
            return

        # Check that we have an experiment that we can add a subject to
        if self.experiment is None:
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

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()

        if selIndexes == []:
            message = 'No subject selected for removal.'
            messagebox(self, message)
            return

        message = 'Permanently remove the selected subjects and the related files?'
        reply = QtWidgets.QMessageBox.question(self, 'Delete selected subjects',
                                           message, QtWidgets.QMessageBox.Yes |
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        failures = []
        if reply == QtWidgets.QMessageBox.Yes:
            for index in selIndexes:
                subject_name = index.data()
        
                try:
                    self.experiment.remove_subject(subject_name, self)
                except Exception:
                    failures.append(subject_name)

        if failures:
            msg = ''.join(['Could not remove the contents of the subject ',
                           'folder for following subjects: ',
                           '\n'.join(failures)])
            messagebox(self, msg)

        self.experiment.save_experiment_settings()
        self.initialize_ui()

    def closeEvent(self, event):
        """Redefine window close event to allow confirming on quit."""

        if self.preferencesHandler.confirm_quit:
            reply = QtWidgets.QMessageBox.question(self, 'Close Meggie',
                                               'Are you sure you want to '
                                               'quit?', QtWidgets.QMessageBox.Yes | 
                                               QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

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

        if self.experiment is None:
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

        if self.experiment.active_subject is None:
            return

        self.epochParameterDialog = EventSelectionDialog(self)
        self.epochParameterDialog.show()

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
        if self.experiment is None:
            messagebox(self, 'You do not currently have an experiment activated.')  # noqa
            return

        self.expInfoDialog = ExperimentInfoDialog(self)
        self.expInfoDialog.show()

    def on_actionHide_Show_subject_list_and_info_triggered(self, checked=None):
        if checked is None:
            return
        if self.ui.dockWidgetSubjects.isVisible():
            self.ui.dockWidgetSubjects.hide()
        else:
            self.ui.dockWidgetSubjects.show()

    def evoked_selection_changed(self, subject_name, data_dict):
        epoch_widget = self.epochList.ui.listWidgetEpochs
        
        epoch_widget.clear()
        epochs = self.experiment.subjects[subject_name].epochs
        for name in sorted(epochs.keys()):
            item = QtWidgets.QListWidgetItem()
            item.setText(name)
            epoch_widget.addItem(item)
            if name in data_dict:
                epoch_widget.setItemSelected(item, True)
       
    def on_listWidgetEvoked_currentItemChanged(self, item):
        if not item:
            self.ui.textBrowserEvokedInfo.clear()
            return
        
        evoked_name = str(item.text())
        evoked = self.experiment.active_subject.evokeds.get(evoked_name)
        info = 'Subjects:\n'
        
        if 'subjects' not in evoked.info:
            self.ui.textBrowserEvokedInfo.clear()
            return 
        
        for subject_name in evoked.info['subjects']:
            info += subject_name + '\n'
 
        info += '\nEpoch collection info:\n'
         
        for collection_name, events in evoked.info['epoch_collections'].items():
            info += collection_name
            for key, value in events.items():
                info += ' [' + key + ', ' + str(value) + '] '
            info += '\n\n'
 
        self.ui.textBrowserEvokedInfo.setText(info)
        
    def on_pushButtonCreateEvoked_clicked(self, checked=None):
        """
        Create averaged epoch collection (evoked dataset).
        Plot the evoked data as a topology.
        """
        if checked is None:
            return

        if self.experiment.active_subject is None:
            return

        selected_items = self.epochList.ui.listWidgetEpochs.selectedItems()
        collection_names = [str(item.text()) for item in selected_items]

        # If no collections are selected, show a message to to the user and return.
        if len(collection_names) == 0:
            messagebox(self, 'Please select an epoch collection to average.')
            return

        subject = self.experiment.active_subject
        
        try:
            self.calculate_evokeds(subject, collection_names)
        except Exception as e:
            exc_messagebox(self, e)

        self.evokeds_batching_widget.cleanup(self)
        self.initialize_ui()

    def on_pushButtonCreateEvokedBatch_clicked(self, checked=None):
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        subject_names = self.evokeds_batching_widget.selected_subjects
        
        recently_active_subject_name = self.experiment.active_subject.subject_name
         
        for subject_name, collection_names in self.evokeds_batching_widget.data.items():
            if subject_name in subject_names:
                try:
                    subject = self.experiment.activate_subject(subject_name)
                    self.calculate_evokeds(subject, collection_names)
                except Exception as e:
                    failed_subjects = self.evokeds_batching_widget.failed_subjects
                    failed_subjects.append((subject, str(e)))
                    logging.getLogger('ui_logger').exception(str(e))
                     
        self.experiment.activate_subject(recently_active_subject_name)
        self.experiment.save_experiment_settings()
        self.evokeds_batching_widget.cleanup(self)
        self.initialize_ui()

    def on_pushButtonGroupSaveEvoked_clicked(self, checked=None):
        if checked is None:
            return
        
        subjects = self.experiment.subjects
        self.save_evoked_data(subjects)

    def on_pushButtonSaveEvoked_clicked(self, checked=None):
        if checked is None:
            return
        
        subjects = dict([
            (self.experiment.active_subject.subject_name, 
             self.experiment.active_subject),
        ])
        
        self.save_evoked_data(subjects)


    def on_pushButtonEvokedTopomaps_clicked(self, checked=None):
        if checked is None:
            return

        if not self.experiment:
            return

        if not self.experiment.active_subject:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())
        evoked = self.experiment.active_subject.evokeds[evoked_name]
        mne_evokeds = evoked.mne_evokeds

        logging.getLogger('ui_logger').info("Plotting evoked topomaps.")

        try:
            number_of_timepoints = 20
            for idx in range(len(list(mne_evokeds.keys()))):
                evoked = list(mne_evokeds.values())[idx]
                evoked_name = list(mne_evokeds.keys())[idx]
                for ch_type in ['mag', 'grad', 'eeg']:
                    n_eeg_channels = len(list(mne.pick_types(evoked.info, eeg=True)))
                    n_mag_channels = len(list(mne.pick_types(evoked.info, meg='mag')))
                    n_grad_channels = len(list(mne.pick_types(evoked.info, meg='grad')))

                    # if mixed data, plot only mag and grad
                    if ch_type == 'eeg' and (n_eeg_channels == 0 or
                                             n_mag_channels > 0 or 
                                             n_grad_channels > 0):
                        continue
                    if ch_type == 'grad' and n_grad_channels == 0:
                        continue
                    if ch_type == 'mag' and n_mag_channels == 0:
                        continue

                    times = np.linspace(0, 
                                        evoked.times[-1], 
                                        number_of_timepoints+1)[:-1]

                    fig, axes = plt.subplots(2, int(number_of_timepoints/2))
                    axes = axes.reshape(-1)

                    title = evoked_name + ' (' + ch_type + ')'
                    fig.suptitle(title) 

                    layout = self.experiment.layout
                    layout = fileManager.read_layout(layout)

                    evoked.plot_topomap(
                        times=times, ch_type=ch_type,
                        axes=axes, show=False, colorbar=False,
                        layout=layout)
            plt.show()

        except Exception as e:
            exc_messagebox(self, e)


    def on_pushButtonVisualizeEpochChannels_clicked(self, checked=None):
        """Plot image over epochs channel"""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        if self.epochList.isEmpty():
            messagebox(self, 'Create epochs before visualizing.')
            return

        if self.epochList.currentItem() is None:
            message = 'Please select an epoch collection from the list.'
            messagebox(self, message)
            return

        name = str(self.epochList.currentItem().text())
        epochs = self.experiment.active_subject.epochs.get(name)
        self.visualizeEpochs = (visualizeEpochChannelDialogMain.
                                VisualizeEpochChannelDialog(epochs))
        self.visualizeEpochs.show()

    def on_pushButtonEpochsPlot_clicked(self, checked=None):
        """Call ``epochs.plot``."""

        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        item = self.epochList.currentItem()
        if item is None:
            message = 'No epochs collection selected.'
            messagebox(self, message)
            return

        epochs_name = str(item.text())
        epochs = self.experiment.active_subject.epochs.get(epochs_name)
        bads = epochs.raw.info['bads']
        
        def handle_close(event):
            epochs.raw.info['bads'] = bads
            fileManager.save_epoch(epochs, overwrite=True)
            self.epochList.selection_changed()
       
        fig = epochs.raw.plot(block=True, show=True)
        
        fig.canvas.mpl_connect('close_event', handle_close)

    def on_pushButtonVisualizeEvokedDataset_clicked(self, checked=None):
        """Plot the evoked data as a topology."""
        if checked is None:
            return

        if self.experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())
        evoked = self.experiment.active_subject.evokeds[evoked_name]
        mne_evokeds = evoked.mne_evokeds

        message = 'Meggie: Visualizing evoked collection %s...\n' % evoked_name
        logging.getLogger('ui_logger').info(message)

        try:
            draw_evoked_potentials(
                self.experiment,
                list(mne_evokeds.values()),
                title=evoked_name)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonGroupAverage_clicked(self, checked=None):
        """
        Plots topology view of evoked response group averages. Saves the
        results as ascii to ``output`` folder. Uses event names for determining
        which responses to average across subjects.
        """
        if checked is None:
            return

        if self.experiment.active_subject is None:
            return

        item = self.ui.listWidgetEvoked.currentItem()
        if item is None:
            return

        evoked_name = str(item.text())

        try:
            evokeds, group_epoch_info = group_average(
                self.experiment, evoked_name, update_ui=self.update_ui)

        except Exception as e:
            exc_messagebox(self, e)
            return

        self.save_evoked(self.experiment.active_subject, evokeds, 'group_' + evoked_name, group_epoch_info=group_epoch_info)

        self.initialize_ui()

    def on_pushButtonLayout_clicked(self, checked=None):
        if checked is None:
            return
        
        self.layoutDialog = LayoutDialog(self)
        self.layoutDialog.show()

    def on_pushButtonDeleteEpochs_clicked(self, checked=None):
        """Delete the selected epoch collection."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        if self.epochList.isEmpty():
            return

        elif self.epochList.currentItem() is None:
            messagebox(self, 'No epochs selected')

        item_str = self.epochList.currentItem().text()

        message = 'Permanently remove epochs?'
        reply = QtWidgets.QMessageBox.question(self, 'delete epochs',
                                           message, QtWidgets.QMessageBox.Yes | 
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.experiment.active_subject.remove_epochs(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)

            self.epochList.remove_item(self.epochList.currentItem())

        if self.epochList.ui.listWidgetEpochs.count() == 0:
            self.clear_epoch_collection_parameters()

        self.experiment.save_experiment_settings()
        self.initialize_ui()

    def on_pushButtonGroupDeleteEpochs_clicked(self, checked=None):
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return
        
        if self.epochList.currentItem() is None:
            messagebox(self, 'No epochs selected')

        collection_name = self.epochList.currentItem().text()
        
        message = 'Permanently remove epoch collection from all subjects?'
        reply = QtWidgets.QMessageBox.question(self, 'delete epochs',
                                           message, QtWidgets.QMessageBox.Yes | 
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for subject in self.experiment.subjects.values():
                if collection_name in subject.epochs:
                    subject.remove_epochs(
                        collection_name,
                    )
            
        if self.epochList.isEmpty():
            self.clear_epoch_collection_parameters()
        
        if collection_name not in self.experiment.active_subject.epochs:
            self.epochList.remove_item(self.epochList.currentItem())
        
        self.experiment.save_experiment_settings()
        self.initialize_ui()

    def on_pushButtonDeleteEvoked_clicked(self, checked=None):
        """Delete the selected evoked."""
        if checked is None:
            return

        if self.experiment.active_subject is None:
            return

        if self.ui.listWidgetEvoked.count() == 0:
            return

        elif self.ui.listWidgetEvoked.currentItem() is None:
            messagebox(self, 'No evokeds selected.')
            return

        item_str = self.ui.listWidgetEvoked.currentItem().text()

        message = 'Permanently remove evokeds?'
        reply = QtWidgets.QMessageBox.question(self, 'delete evokeds',
                                           message, QtWidgets.QMessageBox.Yes | 
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            try:
                self.experiment.active_subject.remove_evoked(
                    item_str,
                )
            except Exception as e:
                exc_messagebox(self, e)

            item = self.ui.listWidgetEvoked.currentItem()
            row = self.ui.listWidgetEvoked.row(item)
            self.ui.listWidgetEvoked.takeItem(row)
            self.experiment.save_experiment_settings()
            self.initialize_ui()


    def on_pushButtonGroupDeleteEvoked_clicked(self, checked=None):
        if checked is None:
            return

        if self.ui.listWidgetEvoked.currentItem() is None:
            messagebox(self, 'No evokeds selected')
            return

        collection_name = self.ui.listWidgetEvoked.currentItem().text()
        
        message = 'Permanently remove evokeds from all subjects?'
        reply = QtWidgets.QMessageBox.question(self, 'delete evokeds',
                                           message, QtWidgets.QMessageBox.Yes | 
                                           QtWidgets.QMessageBox.No,
                                           QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            for subject in self.experiment.subjects.values():
                if collection_name in subject.evokeds:
                    subject.remove_evoked(collection_name)
        
        if collection_name not in self.experiment.active_subject.evokeds:
            self.ui.listWidgetEvoked.takeItem(
                self.ui.listWidgetEvoked.currentRow())
        
        self.experiment.save_experiment_settings()
        self.initialize_ui()


    class RawBadsPlot(object):
        def __init__(self, parent):
            self.parent = parent
            
            if parent.ui.checkBoxShowEvents.isChecked():
                events = parent.experiment.active_subject.get_events()
            else:
                events = None
            try:
                raw = parent.experiment.active_subject.get_working_file()  # noqa
                self.raw = raw.copy()
                fig = self.raw.plot(events=events)
                fig.canvas.mpl_connect('close_event', self.handle_close)
            except Exception as err:
                exc_messagebox(parent, err)
                return
        
        def handle_close(self, event):
            self.raw = None

    def on_pushButtonRawPlot_clicked(self, checked=None):
        """Call ``raw.plot``."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        # Create a plot where bad channels are not set by clicking them
        self.plot = MainWindow.RawBadsPlot(self)
        
    def on_pushButtonCustomChannels_clicked(self, checked=None):
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return
        
        self.badChannelsDialog = BadChannelsDialog(self)
        self.badChannelsDialog.show()
        
    def on_pushButtonPlotProjections_clicked(self, checked=None):
        """Plots added projections as topomaps."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        raw = self.experiment.active_subject.get_working_file()
        if not raw.info['projs']:
            messagebox(self, "No added projections.")
            return
        
        try:
            plot_projs_topomap(self.experiment, raw)
        except Exception as e:
            exc_messagebox(self, e)
       
    def on_pushButtonEOG_clicked(self, checked=None):
        """Open the dialog for calculating the EOG PCA."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.show()

    def on_pushButtonECG_clicked(self, checked=None):
        """Open the dialog for calculating the ECG PCA."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        self.ecgDialog = EcgParametersDialog(self)
        self.ecgDialog.show()

    def on_pushButtonApplyEOG_clicked(self, checked=None):
        """Open the dialog for applying the EOG-projections to the data."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        info = self.experiment.active_subject.get_working_file().info
        self.addEogProjs = AddEOGProjections(self, info['projs'])
        self.addEogProjs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.addEogProjs.show()
        
    def on_pushButtonApplyECG_clicked(self, checked=None):
        """Open the dialog for applying the ECG-projections to the data."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return
        
        info = self.experiment.active_subject.get_working_file().info
        self.addEcgProjs = AddECGProjections(self, info['projs'])
        self.addEcgProjs.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.addEcgProjs.show()
        
    def on_pushButtonRemoveProj_clicked(self, checked=None):
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return
        
        if self.ui.listWidgetProjs.currentItem() is None:
            message = 'Select projection to remove.'
            messagebox(self, message)
            return
        
        selected_items = self.ui.listWidgetProjs.selectedItems()
        raw = self.experiment.active_subject.get_working_file()
        str_projs = [str(proj) for proj in raw.info['projs']]
        
        for item in selected_items:
            proj_name = item.text()
            if proj_name in str_projs:
                index = str_projs.index(proj_name)
                str_projs.pop(index)
                raw.info['projs'].pop(index)
                row = self.ui.listWidgetProjs.row(item)
                self.ui.listWidgetProjs.takeItem(row)

        directory = self.experiment.active_subject.subject_path
        subject_name = self.experiment.active_subject.working_file_name
        fname = os.path.join(directory, subject_name)        
        fileManager.save_raw(self.experiment, raw, fname)
        self.initialize_ui()


    def on_pushButtonChannelAverages_clicked(self, checked=None):
        """Shows the channels average graph."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return
        
        if self.epochList.currentItem() is None:
            message = 'Please select an epoch collection to channel average.'
            messagebox(self, message)
            return

        name = str(self.epochList.currentItem().text())
        
        try:
            lobe_name = self.ui.comboBoxLobes.currentText()
            channels = mne.read_selection(
                lobe_name)
            average_channels(self.experiment, name,
                             channels,
                             lobe_name, 
                             update_ui=self.update_ui)
        except Exception as e:
            exc_messagebox(self, e)

    def on_pushButtonICA_clicked(self, checked=None):
        """
        Show the dialog for ICA preprocessing.
        """
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        self.icaDialog = ICADialog(self)
        self.icaDialog.show()

    def on_pushButtonFilter_clicked(self, checked=None):
        """
        Show the dialog for filtering.
        """
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        self.filterDialog = FilterDialog(self)
        self.filterDialog.show()

    def on_pushButtonActivateSubject_clicked(self, checked=None):
        """
        Activates a subject.
        """
        if checked is None:
            return

        if self.ui.listWidgetSubjects.selectedIndexes() == []:
            return

        selIndexes = self.ui.listWidgetSubjects.selectedIndexes()
        
        if len(selIndexes) > 1:
            return
        
        subject_name = selIndexes[0].data()

        if self.experiment.active_subject:
            if subject_name == self.experiment.active_subject.subject_name:
                return

        # This prevents taking the epoch list currentItem from the previously
        # open subject when activating another subject.
        self.clear_epoch_collection_parameters()
        
        previous_subject = self.experiment.active_subject
        try:
            @threaded
            def activate(subject_name):
                self.experiment.activate_subject(subject_name)
            activate(subject_name, do_meanwhile=self.update_ui)

        except Exception as e:
            self.experiment.active_subject = None
            exc_messagebox(self, "Couldn't activate the subject.")
            if previous_subject:
                message = "Couldn't activate the subject, resuming to previous one."
                logging.getLogger('ui_logger').info(message)
                self.experiment.activate_subject(previous_subject.subject_name)

        self.initialize_ui()

    #####################

    def update_ui(self):
        """
        Method for repainting the ui.
        Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()

    @QtCore.pyqtSlot(Experiment)
    def setExperiment(self, newExperiment):
        """Temporary setter for experiment."""
        self.experiment = newExperiment
        gc.collect()
        
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
            
            logging.getLogger('ui_logger').warning(
                'Epochs parameters not found!')
            return
        
        self.ui.textBrowserTmin.setText(str(params['tmin']) + ' s')
        self.ui.textBrowserTmax.setText(str(params['tmax']) + ' s')

        # Creates dictionary of strings instead of qstrings for rejections.
        params_rejections_str = dict((str(key), value) for key, value in
                                     params['reject'].items())

        if 'mag' in params_rejections_str:
            factor = params_rejections_str['mag']
            self.ui.textBrowserMag.setText(
                str(factor) + ' ' + get_unit('mag'))
        else:
            self.ui.textBrowserMag.setText('-1')

        if 'grad' in params_rejections_str:
            factor = params_rejections_str['grad']
            self.ui.textBrowserGrad.setText(
                str(factor) + ' ' + get_unit('grad'))
        else:
            self.ui.textBrowserGrad.setText('-1')

        if 'eeg' in params_rejections_str:
            factor = params_rejections_str['eeg']
            self.ui.textBrowserEEG.setText(
                str(factor) + ' ' + get_unit('eeg'))
        else:
            self.ui.textBrowserEEG.setText('-1')

        if 'eog' in params_rejections_str:
            factor = params_rejections_str['eog']
            self.ui.textBrowserEOG.setText(
                str(factor) + ' ' + get_unit('eog'))
        else:
            self.ui.textBrowserEOG.setText('-1')

        if 'stim' in params_rejections_str:
            self.ui.textBrowserStim.setText('Yes')
        else:
            self.ui.textBrowserStim.setText('-1')

        self.ui.textBrowserWorkingFile.setText(
            epochs.path)

    def clear_epoch_collection_parameters(self):
        """
        Clears epoch collection parameters on mainWindow Epoching tab.
        """
        self.ui.textBrowserTmin.clear()
        self.ui.textBrowserTmax.clear()
        self.ui.textBrowserGrad.clear()
        self.ui.textBrowserMag.clear()
        self.ui.textBrowserEEG.clear()
        self.ui.textBrowserStim.clear()
        self.ui.textBrowserEOG.clear()
        self.ui.textBrowserWorkingFile.clear()

    def collect_evoked_parameter_values(self):
        collection_names = [str(item.text()) for item 
                in self.epochList.ui.listWidgetEpochs.selectedItems()]
        return collection_names        


    def calculate_evokeds(self, subject, collection_names):

        # check that lengths are same
        time_arrays = []
        for name in collection_names:
            collection = subject.epochs.get(name)
            if collection:
                time_arrays.append(collection.raw.times)

        for i, i_times in enumerate(time_arrays):
            for j, j_times in enumerate(time_arrays):
                if i != j:
                    try:
                        np.testing.assert_array_almost_equal(i_times, j_times)
                    except AssertionError:
                        raise Exception('Epochs collections of different time'
                                        'scales are not allowed')
        
        evokeds = {}
        for name in collection_names:

            try:
                collection = subject.epochs[name]
            except KeyError:
                raise KeyError('No epoch collection called ' + str(name))

            epoch = collection.raw
            
            @threaded
            def average():
                return epoch.average()

            evoked = average(do_meanwhile=self.update_ui)

            evoked.comment = name
            evokeds[name] = evoked

        evoked_name = (
            '-'.join(collection_names) +
            '_evoked.fif'
        )
    
        self.save_evoked(subject, evokeds, evoked_name)

    def save_evoked(self, subject, evokeds, evoked_name, group_epoch_info={}):
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
            message = 'Writing evoked data as ' + evoked_name + ' ...'
            logging.getLogger('ui_logger').info(message)

            mne.write_evokeds(os.path.join(saveFolder, evoked_name), list(evokeds.values()))
        except IOError:
            message = ('Writing to selected folder is not allowed. You can '
                       'still process the evoked file (visualize etc.).')
            raise IOError(message)
        
        new_evoked = Evoked(evoked_name, subject, evokeds)

        epoch_info = {}
        subject_names = []
        
        if not group_epoch_info:
            for key in evokeds:
                epoch = getattr(subject.epochs.get(key, object()), 'raw', None)
                events = epoch.event_id
                epoch_info[key] = dict([(name, str(len(epoch[name])) + ' events') 
                                        for name in events])
            subject_names = [subject.subject_name]
        else:
            for subject_name, info in group_epoch_info.items():               
                epoch_info[subject_name] = info['epoch_collections']
                subject_names = ['group evoked']
        
        new_evoked.info['subjects'] = subject_names
        new_evoked.info['epoch_collections'] = epoch_info
        subject.add_evoked(new_evoked)             
        self.experiment.save_experiment_settings()

    def save_evoked_data(self, subjects):
        try:    
            evoked_name = str(self.ui.listWidgetEvoked.currentItem().text())
        except AttributeError:
            messagebox(self, "Please select evoked data from the list")
            return

        path = fileManager.create_timestamped_folder(
            self.experiment)

        for sub_name, subject in subjects.items():
            names = []
            evokeds = []
            meggie_evoked = subject.evokeds.get(evoked_name)
            if meggie_evoked:
                for name, evoked in meggie_evoked.mne_evokeds.items():
                    if evoked:
                        evokeds.append(evoked)
                        names.append(name)
            if evokeds:
                cleaned_evoked_name = evoked_name.split('.')[0]
                filename = cleaned_evoked_name + '_' + sub_name + '.csv'  # noqa
                fileManager.group_save_evokeds(os.path.join(path, filename), 
                                               evokeds, names)
 

    def initialize_ui(self):
        """
        Method for setting up the GUI. Called whenever a subject is activated,
        either via creation of a new subject or change of an active subject.
        Also called when anything that can affect UI state has been run.
        Checks the existence of a ton of files and sets the GUI fields to
        reflect the state of the experiment and subject according to them.
        """

        self.update_tabs()

        self.setup_loggers()

        self.clear_epoch_collection_parameters()
        self.epochList.clearItems()
        self.ui.listWidgetSubjects.clear()
        self.ui.listWidgetEvoked.clear()
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
        self.ui.pushButtonApplyECG.setEnabled(False)
        self.ui.pushButtonApplyEOG.setEnabled(False)

        self.setWindowTitle('Meggie - ' + self.experiment.experiment_name)

        self.populate_subject_list()

        # Update the batching widget ui
        if self.experiment:
            self.evokeds_batching_widget.update(self.experiment, False)

        active_subject = self.experiment.active_subject
        
        if active_subject is None:
            self.statusLabel.setText('Add or activate subjects before '
                                     'continuing.')
            return        
        
        raw = active_subject.get_working_file()
        
        name = active_subject.working_file_name
        status = "Current working file: " + name
        
        self.statusLabel.setText(status)

        # Check whether ECG projections are calculated
        if active_subject.check_ecg_projs():
            self.ui.pushButtonApplyECG.setEnabled(True)
            self.ui.checkBoxECGComputed.setChecked(True)
        
        # Check whether EOG (and old EEG) projections are calculated
        if active_subject.check_eog_projs() or active_subject.check_eeg_projs():
            self.ui.pushButtonApplyEOG.setEnabled(True)
            self.ui.checkBoxEOGComputed.setChecked(True)
        
        # Check whether ECG projections are applied
        if active_subject.check_ecg_applied():
            self.ui.checkBoxECGApplied.setChecked(True)
        
        # Check whether EOG (and old EEG) projections are applied
        if active_subject.check_eog_applied() or active_subject.check_eeg_applied():
            self.ui.checkBoxEOGApplied.setChecked(True)

        # Check whether sss/tsss method is applied.
        if active_subject.check_sss_applied():
            self.ui.checkBoxMaxFilterComputed.setChecked(True)
            self.ui.checkBoxMaxFilterApplied.setChecked(True)

        epochs_items = active_subject.epochs
        evokeds_items = active_subject.evokeds
        if epochs_items is not None:
            for name in sorted(epochs_items.keys()):
                self.epochList.add_item(name)

        if evokeds_items is not None:
            for name in sorted(evokeds_items.keys()):
                self.ui.listWidgetEvoked.addItem(name)

        # This updates the 'Subject info' section below the subject list.
        try:
            InfoDialog(raw, self.ui, False)
            self.populate_raw_tab_event_list()
        except Exception as err:
            exc_messagebox(self, err)
            return

        projs = raw.info['projs']
        for proj in projs:
            self.ui.listWidgetProjs.addItem(str(proj))

        bads = raw.info['bads']
        for bad in bads:
            self.ui.listWidgetBads.addItem(bad)

    def populate_subject_list(self):
        """ """
        active_subject_name = None
        if self.experiment and self.experiment.active_subject:
            active_subject_name = self.experiment.active_subject.subject_name

        for subject_name in sorted(self.experiment.subjects.keys()):
            item = QtWidgets.QListWidgetItem()
            item.setText(subject_name)
            if subject_name == active_subject_name:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            self.ui.listWidgetSubjects.addItem(item)

        
    def populate_raw_tab_event_list(self):
        """
        Fill the raw tab event list with info about event IDs and
        amount of events with those IDs.
        """
        events = self.experiment.active_subject.create_event_set()

        if events is None:
            return

        events_string = ''
        for key, value in events.items():
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

    def update_tabs(self):
        """Method for initializing the tabs."""

        current_tab = self.ui.tabWidget.currentIndex()                                  
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)

        self.ui.tabWidget.insertTab(1, self.ui.tabPreprocessing, "Preprocessing")
        self.ui.tabWidget.insertTab(2, self.mainWindowTabSpectrums, "Spectrums")
        self.ui.tabWidget.insertTab(3, self.ui.tabEpoching, "Epoching")
        self.ui.tabWidget.insertTab(4, self.ui.tabEvoked, "Evoked responses")
        self.ui.tabWidget.insertTab(5, self.mainWindowTabInduced, "Induced responses")
        self.ui.tabWidget.insertTab(6, self.mainWindowTabSourceAnalysis, "Source Analysis")

        self.ui.tabWidget.setCurrentIndex(current_tab)

        self.mainWindowTabSourceAnalysis.update_tabs()
        self.mainWindowTabSourceAnalysis.initialize_ui()

        self.mainWindowTabSpectrums.initialize_ui()
        self.mainWindowTabInduced.initialize_ui()
        
    def on_currentChanged(self):
        """
        Keep track of the active tab.
        Show the epoch collection list epochList when in appropriate tabs.
        """

        index = self.ui.tabWidget.currentIndex()
        if index == 2:
            mode = QtWidgets.QAbstractItemView.SingleSelection
            self.epochList.setParent(self.ui.groupBoxEpochsEpoching)
        elif index == 3:
            mode = QtWidgets.QAbstractItemView.MultiSelection
            self.epochList.setParent(self.ui.groupBoxEpochsAveraging)
        else:
            self.epochList.hide()
            return

        self.epochList.setSelectionMode(mode)
        self.epochList.show()

    def collect_parameter_values(self):
        collection_names = [str(item.text()) for item 
                in self.epochList.ui.listWidgetEpochs.selectedItems()]
        return collection_names        

    def directOutput(self):
        """
        Method for directing stdout to the console and back.
        """
        if self.ui.actionDirectToConsole.isChecked():
            stdout_stream = EmittingStream(textWritten=self.normalOutputWritten)
            stdout_stream.orig_stream = sys.__stdout__
            stderr_stream = EmittingStream(textWritten=self.errorOutputWritten)
            stderr_stream.orig_stream = sys.__stderr__

            sys.stdout = stdout_stream
            sys.stderr = stderr_stream
        else:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

    def check_workspace(self):
        """
        Open the preferences dialog, in this case for choosing the workspace.
        """
        preferencesDialog = PreferencesDialog(self)
        preferencesDialog.exec_()

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

    def setup_loggers(self):

        # hide warnings-module warnings,
        # most of these are still contained
        # in mne-level logging
        warnings.simplefilter('ignore')

        logging.getLogger().setLevel(logging.DEBUG)

        # logger for mne wrapper functions
        mne_wrapper_logger = logging.getLogger('mne_wrapper_logger')
        formatter = logging.Formatter('MNE call: %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        mne_wrapper_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.experiment_name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            mne_wrapper_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        mne_wrapper_logger.addHandler(stream_handler)

        # logger for ui output
        ui_logger = logging.getLogger('ui_logger')
        formatter = logging.Formatter('Meggie: %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        ui_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.experiment_name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            ui_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('INFO')
        ui_logger.addHandler(stream_handler)

        # logger for real mne
        mne_logger = logging.getLogger('mne')
        formatter = logging.Formatter('MNE: %(asctime)s %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S')

        mne_logger.handlers = []

        # setup file handler
        if self.experiment:
            logfile = os.path.join(
                self.experiment.workspace,
                self.experiment.experiment_name,
                'meggie.log')
            file_handler = logging.FileHandler(logfile)
            file_handler.setLevel('DEBUG')
            file_handler.setFormatter(formatter)
            mne_logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel('ERROR')
        mne_logger.addHandler(stream_handler)

        # TODO: trait logger ..


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

    def fileno(self):
        return self.orig_stream.fileno()



def main():

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(app)

    window.showMaximized()
    
    sys.exit(app.exec_())
