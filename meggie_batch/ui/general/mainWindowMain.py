# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 16, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen, Atte Rautio
Contains the MainWindow-class that holds the main window of the application.
"""

import os, sys, traceback, shutil

from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QWhatsThis, QAbstractItemView
from PyQt4.Qt import QApplication
import sip

from mne import fiff

import matplotlib
matplotlib.use('Qt4Agg')
from code_meggie.general.caller import Caller

from mainWindowUi import Ui_MainWindow
from createExperimentDialogMain import CreateExperimentDialog
from addSubjectDialogMain import AddSubjectDialog
from infoDialogMain import InfoDialog
from channelSelectionDialogMain import ChannelSelectionDialog
from ui.epoching.eventSelectionDialogMain import EventSelectionDialog
from ui.visualization.visualizeEpochChannelDialogMain import VisualizeEpochChannelDialog
from ui.preprocessing.maxFilterDialogMain import MaxFilterDialog
from ui.preprocessing.eogParametersDialogMain import EogParametersDialog
from ui.preprocessing.ecgParametersDialogMain import EcgParametersDialog
from preferencesDialogMain import PreferencesDialog
from evokedStatsDialogMain import EvokedStatsDialog
from ui.preprocessing.addECGProjectionsMain import AddECGProjections
from ui.preprocessing.addEOGProjectionsMain import AddEOGProjections
from ui.visualization.TFRDialogMain import TFRDialog
from ui.visualization.TFRTopologyDialogMain import TFRTopologyDialog
from ui.visualization.spectrumDialogMain import SpectrumDialog
from ui.visualization.powerSpectrumDialogMain import PowerSpectrumDialog
from ui.widgets.epochWidgetMain import EpochWidget
from aboutDialogMain import AboutDialog
from ui.filtering.filterDialogMain import FilterDialog
from ui.sourceModeling.forwardModelDialogMain import ForwardModelDialog
from experimentInfoDialogMain import experimentInfoDialog
from ui.sourceModeling.forwardSolutionDialogMain import ForwardSolutionDialog
from ui.sourceModeling.covarianceRawDialogMain import CovarianceRawDialog
from ui.widgets.covarianceWidgetNoneMain import CovarianceWidgetNone
from ui.widgets.covarianceWidgetRawMain import CovarianceWidgetRaw
import messageBoxes

from code_meggie.general import experiment
from code_meggie.general.experiment import Experiment
from code_meggie.epoching.epochs import Epochs
from code_meggie.general.prefecences import PreferencesHandler
from code_meggie.general import fileManager
from ui.widgets.listWidget import ListWidget
from code_meggie.general.mvcModels import ForwardModelModel, SubjectListModel


class MainWindow(QtGui.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """
    
    #custom signals
    #experiment_value_changed was made useless. All the stuff moved to
    #_initialize_ui() method.
    #experiment_value_changed = QtCore.pyqtSignal()
    caller = Caller.Instance()

    def __init__(self, application):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # List of subprocesses, used for terminating MNE-C processes on Meggie
        # quit.
        self.processes = [] 
        
        # Main window represents one _experiment at a time. This _experiment is
        # defined by the CreateExperimentDialog or the by the Open_experiment_
        # triggered action.
        #self._experiment = None
        
        # Direct output to console
        self.directOutput()
        self.ui.actionDirectToConsole.triggered.connect(self.directOutput)
        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
        sys.stderr = EmittingStream(textWritten=self.errorOutputWritten)
        
        # One main window (and one _experiment) only needs one caller to do its
        # bidding. 
        self.caller.setParent(self)
       
        # For storing and handling program wide prefences.
        self.preferencesHandler = PreferencesHandler()
        self.preferencesHandler.set_env_variables()
       
        # For handling initialization and switching of experiments.
        # TODO: currently only handles initialization.
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
        
        self.evokedList = ListWidget(self.ui.widgetEvokeds)
        self.evokedList.setMinimumWidth(345)
        self.evokedList.setMaximumHeight(120)
        #self.evokedList.setSelectionMode(QtGui.QAbstractItemView.ContiguousSelection)
        
        self.epocher = Epochs()
        
        # Populate the combobox for selecting lobes for channel averages.
        self.populate_comboBoxLobes()
        
        # Connect signals and slots.
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)
        self.epochList.item_added.connect(self.epochs_added)
        self.ui.pushButtonMNE_Browse_Raw_2.clicked.connect(
                              self.on_pushButtonMNE_Browse_Raw_clicked)
        
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
        
        self.ui.tableViewFModelsForCoregistration.\
        setModel(self.forwardModelModel)
        for colnum in range(16, 21):
            self.ui.tableViewFModelsForCoregistration.setColumnHidden(colnum,
                                                                      True)
        
        tvfs = self.ui.tableViewFModelsForSolution
        tvfs.setModel(self.proxyModelTableViewForwardSolutionSource)     
        for colnum in range(1, 16):
            tvfs.setColumnHidden(colnum, True)
        
        # TODO: should show empty mainWindow with "loading previous experiment
        # named <name>"-notification to user before starting to load
        # the experiment, currently doesn't.
        # If the user has chosen to open the previous experiment automatically.
        if self.preferencesHandler.auto_load_last_open_experiment is True:
            name = self.preferencesHandler.previous_experiment_name
            self.experimentHandler.open_existing_experiment(name)
        
        #Populate layouts combobox.
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)    
        
        self.ui.listWidgetBads.setSelectionMode(QAbstractItemView.NoSelection)
        self.ui.listWidgetProjs.setSelectionMode(QAbstractItemView.NoSelection)
        
    def update_ui(self):
        """
        Method for repainting the ui.
        Used for keeping the ui responsive when threading.
        """
        QApplication.processEvents()
        
### Code for catching signals and reacting to them ###
    def on_actionQuit_triggered(self, checked=None):
        """
        Closes the program, possibly after a confirmation by the user.
        """
        if checked is None: return
        
        if self.preferencesHandler.confirm_quit == True:
            reply = QtGui.QMessageBox.question(self, 'Close Meggie',
                     'Are you sure you want to quit Meggie?', 
                     QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                     QtGui.QMessageBox.No)
                
            if reply == QtGui.QMessageBox.Yes:
                self.close()
        else: self.close()

        
    def on_actionCreate_experiment_triggered(self, checked=None):
        """
        Create a new CreateExperimentDialog and show it
        """
        if checked is None: return # Standard workaround for file dialog opening twice
        
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
        """
        Temporary setter for experiment.
        """
        self.caller.experiment = newExperiment
        self.add_tabs()
        self._initialize_ui() 
        self.reinitialize_models() 
        
        
    def on_actionOpen_experiment_triggered(self, checked=None):
        """
        Open an existing _experiment.
        
        TODO actual experiment opening code should be in ExperimentHandler
        """
        # Standard workaround for file dialog opening twice
        if checked is None: return        
        
        path = str(QtGui.QFileDialog.getExistingDirectory(
                   self, "Select _experiment directory"))
        if path == '': return
        
        self.experimentHandler.open_existing_experiment(os.path.basename(path))
        
            
    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """
        Open subject dialog.
        """
        if checked is None: return
        
        # Check that we have an experiment that we can add a subject to 
        if self.caller.experiment is None:
            message = 'No active experiment to add a subject to. ' \
            + 'Load an experiment or make a new one, then try again.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        self.subject_dialog = AddSubjectDialog(self)
        self.subject_dialog.exec_()

    
    def on_pushButtonRemoveSubject_clicked(self, checked=None):
        """Delete the selected subject item and the files related to it.
        """
        if checked is None:
            return
        
        selIndexes = self.ui.listViewSubjects.selectedIndexes()
        
        if selIndexes == []:
            message = 'No subject selected for removal.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        subject_name = selIndexes[0].data()
            
        message = 'Permanently remove subject and the related files?'
        reply = QtGui.QMessageBox.question(self, 'delete subject',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            try:
                #TODO: What if removeRows fails?
                self.caller.experiment.remove_subject(subject_name, self)
                self.subjectListModel.removeRows(selIndexes[0].row())
            except Exception:
                message = 'Could not remove the contents of the subject' + \
                            ' folder.'
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
        
        
    def show_epoch_collection_parameters(self, epochs):
        """
        Shows parameters from the currently chosen epochs.
        
        Keyword arguments:
        epochs -- Epochs object
        """
        # Set default/empty values for epoch parameters.
        self.clear_epoch_collection_parameters()
        
        """
        TODO: get epochs from active_subject._epochs dictionary
        """
        epochs_raw = epochs._raw
        params = epochs._params
        if params is None:
            # TODO: Fill source file field if no parameters for epochs
            # collection. 'filename' is the current location of the collection,
            # so add some other information here?
            self.ui.textBrowserWorkingFile.\
            setText('Unknown source file. ' + epochs_raw.info.get('description'))
            
            # TODO: this is too slow. If remove this line remove
            # measurementInfo from imports also.
            #self.mi = MeasurementInfo(self._experiment.active_subject._working_file)
            #self.ui.textBrowserWorkingFile.\
            #setText(self.mi.subject_name)
            return
        # Dictionary stores numbers of different events.
        event_counts = dict()
        # Adds items to dictionary for corresponding events.
        for value in epochs_raw.event_id.values():
            event_counts[str(value)] = 0
        # Adds number of events to corresponding event.
        for event in epochs_raw.events:
            for key in event_counts.keys():
                if event[2] == int(key):
                    event_counts[key] += 1
        categories = ''
        # Adds event names, ids and event counts on mainWindows parameters
        # list.
        for key,value in epochs_raw.event_id.items():
            item = QtGui.QListWidgetItem()
            item.setText(key + ': ID ' + str(value) + ', ' + \
            str(event_counts[str(value)]) + ' events')
            self.epochList.ui.listWidgetEvents.addItem(item)
        # TODO: create category items to add on the listWidgetEvents widget. 
        #self.epochList.ui.listWidgetEvents.setText(categories)
        self.ui.textBrowserTmin.setText(str(params['tmin']) + ' s')
        self.ui.textBrowserTmax.setText(str(params['tmax']) + ' s')
        # Creates dictionary of strings instead of qstrings for rejections.
        params_rejections_str = dict((str(key), value) for
                          key, value in params['reject'].iteritems())
        if 'mag' in params_rejections_str:
            self.ui.textBrowserMag.setText(str(params_rejections_str['mag']\
                                                 / 1e-12) + ' fT')
        else:
            self.ui.textBrowserMag.setText('-1')
        if 'grad' in params_rejections_str:
            self.ui.textBrowserGrad.setText(str(params_rejections_str['grad']\
                                                 / 1e-12) + ' fT/cm')
        else:
            self.ui.textBrowserGrad.setText('-1')
        if 'eeg' in params_rejections_str:
            self.ui.textBrowserEEG.setText(str(params_rejections_str['eeg']\
                                                / 1e-6) + 'uV')
        else:
            self.ui.textBrowserEEG.setText('-1')
        if 'stim' in params_rejections_str:
            #self.ui.checkBoxStim.setChecked(True)
            self.ui.textBrowserStim.setText('Yes')
        else:
            self.ui.textBrowserStim.setText('-1')
        if 'eog' in params_rejections_str:
            self.ui.textBrowserEOG.setText(str(params_rejections_str['eog']\
                                                / 1e-6) + 'uV')
        else:
            self.ui.textBrowserEOG.setText('-1')
        filename_full_path = str(params['raw'])
        filename_list = filename_full_path.split('/')
        filename = filename_list[len(filename_list) - 1]
        self.ui.textBrowserWorkingFile.setText(filename)

        
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
        #self.ui.textBrowserEvents.clear()   #setText('')
        self.ui.textBrowserWorkingFile.clear()

        
    def on_actionSet_workspace_triggered(self, checked=None):
        """
        Open the preferences dialog the for specific purpose of initial setting
        of workspace.
        """
        if checked is None: return
        self.check_workspace()

        
    def on_actionPreferences_triggered(self, checked=None):
        """Open the preferences-dialog.
        """
        if checked is None: return
        self.dialogPreferences = PreferencesDialog(self)
        self.dialogPreferences.show()

        
    def on_pushButtonCreateEpochs_clicked(self, checked=None):
        """
        Open the epoch dialog. 
        """
        if checked is None: return
        self.epochParameterDialog = EventSelectionDialog(self)
        self.epochParameterDialog.epoch_params_ready.\
        connect(self.create_new_epochs)
        self.epochParameterDialog.show()

        
    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def epochs_added(self, item):
        """
        A slot for saving epochs from the added QListWidgetItem to a file.
        """
        if os.path.exists(self.caller.experiment.active_subject._epochs_directory) is False:
            self.caller.experiment.active_subject.create_epochs_directory()
        fname = str(item.text())
        fpath = os.path.join(self.caller.experiment.active_subject._epochs_directory, fname)
        epochs_object = self.caller.experiment.active_subject._epochs[fname]
        fileManager.save_epoch(fpath, epochs_object)
        

    def closeEvent(self, event):
        """
        Redefine window close event to allow confirming on quit.
        """
        
        if self.preferencesHandler.confirm_quit == True:
            reply = QtGui.QMessageBox.question(self, 'Close Meggie',
                "Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
                QtGui.QMessageBox.No, QtGui.QMessageBox.No)
    
            if reply == QtGui.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()  


    #TODO: Move to caller?  
    @QtCore.pyqtSlot(dict)
    def create_new_epochs(self, epoch_params):
        """A slot for creating new epochs with the given parameter values.
        
        Keyword arguments:
        epoch_params = A dictionary containing the parameter values for
                       creating the epochs minus the raw data.
        """
        #Raw data is not present in the dictionary so get it from the
        #current experiment.active_subject.
        epochs = self.epocher.create_epochs_from_dict(epoch_params,
                                                      self.caller.experiment.\
                                                      active_subject.\
                                                      _working_file)
        epoch_params['raw'] = self.caller.experiment.\
        _working_file_names[self.caller.experiment._active_subject_name]
        
        fname = epoch_params['collectionName']
        item = QtGui.QListWidgetItem(fname)
        self.caller.experiment.active_subject.handle_new_epochs(fname, epochs, epoch_params)
        self.epochList.addItem(item)
        self.epochList.setCurrentItem(item)

        
    def on_pushButtonLoadEpochs_clicked(self, checked=None):
        """Load epochs from a folder.
        
        Epochs are copied to /experiment/epochs. If parameters are available,
        they are saved as well.
        """
        if checked is None: return
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Load epochs',
                                                      self.caller.experiment.\
                                                      active_subject.\
                                                      _epochs_directory))
        if fname == '': return
        if not os.path.isfile(fname): return
        
        epochs, params = fileManager.load_epochs(fname)
        # Change color of the item to red if no param file available.
        fname_base = os.path.basename(fname)
        fname_prefix = fname_base.split('.')[0]
        
        fname_temp = fname_prefix

        # If trying to  load same raw epoch fif the collection name stays the
        # same and new Epochs object is not created. This changes the
        # collection name.
        suffix = 2
        while len(self.epochList.ui.listWidgetEpochs.\
               findItems(fname_prefix, QtCore.Qt.MatchExactly)) > 0:
            fname_prefix = fname_temp + str(suffix)
            if params is not None:
                params['collectionName'] = fname_prefix
            suffix += 1
        
        item = QtGui.QListWidgetItem(fname_prefix)
        if params is None:
            color = QtGui.QColor(255, 0, 0, 255)
            brush = QtGui.QBrush()
            brush.setColor(color)
            item.setForeground(brush)
        self.caller.experiment.active_subject.handle_new_epochs(fname_prefix, epochs, params)
        self.epochList.addItem(item)
        self.epochList.setCurrentItem(item)

        
    def on_pushButtonModifyEpochs_clicked(self, checked = None):
        """Modify currently selected epochs.
        """
        if checked is None: return
        if self.epochList.currentItem() is None: return
        
        """
        TODO: get ed params from active_subject._evokeds dictionary
        """
        collection_name = str(self.epochList.currentItem().text())
        params = self.caller.experiment.active_subject._epochs[collection_name]._params
        self.epochParameterDialog = EventSelectionDialog(self)

        # modify_epochs removes the previous Epochs object and raw files
        # created from it and creates new Epochs object and raw files.
        # Also removes the epochWidget item and replaces it with the new one.
        self.epochParameterDialog.epoch_params_ready.\
        connect(self.caller.experiment.active_subject.modify_epochs)
        self.epochParameterDialog.show()

                
    def on_pushButtonSaveEpochs_clicked(self, checked=None):
        """Save the epoch collections to a .fif file 
        """
        if checked is None: return
        fname = str(QtGui.QFileDialog.getSaveFileName(self, 'Save epochs',
                                                      self.caller.experiment.\
                                                      active_subject.\
                                                      _epochs_directory))
        if fname == '': return
        else: 
            """
            TODO: get epochs from active_subject._epochs dictionary
            """
            collection_name = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
            epochs = self.caller.experiment.active_subject._epochs[collection_name]._raw
            epochs.save(fname)
        #Also copy the related csv-file to the chosen folder
        shutil.copyfile(os.path.join(self.caller.experiment.active_subject.\
                                           _epochs_directory,
                              str(self.epochList.currentItem().text()) +
                              '.csv'), fname + '.csv')


    def on_actionAbout_triggered(self, checked=None):
        """
        Open the About-dialog. 
        """
        if checked is None: return
        self.dialogAbout = AboutDialog()
        self.dialogAbout.show()

        
    def on_actionShowExperimentInfo_triggered(self, checked=None):    
        """
        Open the experiment info dialog 
        """
        if checked is None: return
        if self._experiment is None:
            self.messageBox = messageBoxes.shortMessageBox()
            self.messageBox.labelException.setText \
            ('You do not currently have an experiment activated.')
            self.messageBox.show()  
            return
        self.expInfoDialog = experimentInfoDialog()
        self.expInfoDialog.show()

        
    def on_actionHide_Show_subject_list_and_info_triggered(self, checked=None):
        if checked is None: return
        if self.ui.dockWidgetSubjects.isVisible():
            self.ui.dockWidgetSubjects.hide()
        else:
            self.ui.dockWidgetSubjects.show()

            
    def on_actionToggle_whatsthis_mode_triggered(self, checked=None):
        if checked is None: return
        if QWhatsThis.inWhatsThisMode() is True: 
            QWhatsThis.leaveWhatsThisMode()
        else: QWhatsThis.enterWhatsThisMode()   

    
    def on_pushButtonCreateEvoked_clicked(self, checked=None):
        """
        Create averaged epoch collection (evoked dataset).
        Plot the evoked data as a topology.
        """
        #TODO: MULTIPLE SELECTION
        if checked is None: return

        items = self.epochList.ui.listWidgetEpochs.selectedItems()
        # If no events are selected, show a message to to the user and return.
        if len(items) == 0: 
            message = 'Please select an epoch collection to average.' 
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()  
            return
        
        
        prefix = ''
        epochs = []
        category = dict()
        for item in items:
            if not prefix == '':
                prefix = prefix + '-' 
            key = str(item.text())
            epoch = self.caller.experiment.active_subject._epochs[key]
            epochs.append(epoch)
            category.update(epoch._raw.event_id)
            prefix = prefix + item.text()
        #key = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
        #epochs = self.caller.experiment.active_subject._epochs[key]
        
        #category = epochs._raw.event_id
        
        # New dictionary for event categories must be created, if user
        # manually chooses different event categories to be averaged. 
        if len(self.epochList.ui.listWidgetEvents.selectedItems()):
            category_user_chosen = dict()
            for event in self.epochList.ui.listWidgetEvents.selectedItems():
                event_name = (str(event.text())).split(':')
                for epoch in epochs:
                    category_user_chosen[event_name[0] + epoch.name] = epoch._raw.event_id.get(event_name[0])
            evoked = self.caller.average(epochs, category_user_chosen)
            category = category_user_chosen
        else:
            evoked = self.caller.average(epochs, category)
        
        category_str = ''
        i = 0
        for key in category.keys():
            if i == 0:
                category_str += key
                i = 1
            else:
                category_str += '-' + key
        """
        epoch_collection = self.epochList.ui.listWidgetEpochs.currentItem()
        evoked_name = str(epoch_collection.\
                          text() + '[' + category_str + ']' + '_evoked.fif')
        """
        evoked_name = prefix + '[' + str(category_str) + ']_evoked.fif'
        item = QtGui.QListWidgetItem(evoked_name)
        
        # TODO: create separate method in fileManager to save evoked
        # Save evoked into evoked (average) directory with name evoked_name
        saveFolder = self.caller.experiment.active_subject._evokeds_directory
        if os.path.exists(saveFolder) is False:
            try:
                os.mkdir(saveFolder)
            except IOError:
                message = 'Writing to selected folder is not allowed. ' + \
                'You can still process the evoked file (visualize etc.).'
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()  
        try:                
            # TODO: best filename option ? (_auditory_and_visual_eeg-ave)
            print 'Writing evoked data as ' + evoked_name + ' ...'
            fiff.write_evokeds(os.path.join(saveFolder, evoked_name), evoked)
            print '[done]'
        except IOError:
            message = 'Writing to selected folder is not allowed. You can still' \
                      + ' process the evoked file (visualize etc.).'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.labelException.setText \
            ()
            self.messageBox.show()
        
        
        self.evokedList.addItem(item)
        self.caller.experiment.active_subject.handle_new_evoked(evoked_name, evoked, category)
        #self.evokedList.setCurrentItem(item)

        
    def on_pushButtonOpenEvokedStatsDialog_clicked(self, checked = None):
        """Open the evokedStatsDialog for viewing statistical data.
        """
        #Currently a mock code.
        #TODO: Pass evokeds in a dictionary
        if checked is None: return
        if self.evokedList.count() == 0: return
        
        evoked_dict = {}
        for i in range(self.evokedList.count()):
            evoked_name = str(self.evokedList.item(i).text())
            evoked = self.caller.experiment.active_subject._evokeds[evoked_name]._raw
            evoked_dict[str(self.evokedList.item(i).text())] = evoked
            #evoked_dict[str(self.evokedList.item(i).text())] = \
            #self.evokedList.item(i).data(32).toPyObject()
        self.evokedStatsDialog = EvokedStatsDialog(evoked_dict)
        self.evokedStatsDialog.exec_()

        
    def on_pushButtonVisualizeEpochChannels_clicked(self, checked = None):
        """Plot image over epochs channel
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.count() == 0:
            message = 'Create epochs before visualizing.' 
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
        
            
            return
        epochs_name = str(self.epochList.ui.listWidgetEpochs.\
                          currentItem().text())
        epochs = self.caller.experiment.active_subject._epochs[epochs_name]._raw
        self.visualizeEpochChannelsDialog = VisualizeEpochChannelDialog(epochs)
        self.visualizeEpochChannelsDialog.exec_()

        
    def on_pushButtonVisualizeEvokedDataset_clicked(self, checked=None):
        """
        Plot the evoked data as a topology
        """
        if checked is None: return
        item = self.evokedList.currentItem()
        if item is None: return
        """
        TODO: get evoked from active_subject._evokeds dictionary
        """
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        layout = ''
        if self.ui.radioButtonSelectLayout.isChecked():
            layout = str(self.ui.comboBoxLayout.currentText())
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
        if layout == '':
            QtGui.QApplication.restoreOverrideCursor()
            mBox = messageBoxes.shortMessageBox('No layout selected!')
            mBox.exec_()
            return
            
        self.ui.pushButtonVisualizeEvokedDataset.setText(
                                    '      Visualizing...      ')
        self.ui.pushButtonVisualizeEvokedDataset.setEnabled(False)
        
        evoked_name = str(self.evokedList.currentItem().text())
        evoked = self.caller.experiment.active_subject._evokeds[evoked_name]
        evoked_raw = evoked._raw
        
        print 'Meggie: Visualizing evoked collection ' + evoked_name + ' ...\n'
        try:
            self.caller.draw_evoked_potentials(evoked_raw, layout)
            print 'Meggie: Evoked collection ' + evoked_name + ' visualized! \n'
        except Exception as e:
            mBox = messageBoxes.shortMessageBox('Error while visualizing.\n' +\
                                                str(e))
            mBox.exec_()
        finally:
            oldText = 'Visualize selected dataset'
            self.ui.pushButtonVisualizeEvokedDataset.setText(oldText)
            self.ui.pushButtonVisualizeEvokedDataset.setEnabled(True)
            QtGui.QApplication.restoreOverrideCursor()
              
              
    def on_pushButtonGroupAverage_clicked(self, checked=None):
        """
        """
        if checked is None: return
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        evoked_name = str(self.evokedList.currentItem().text())
        import re
        groups = re.split('[\[\]]', evoked_name)[1] # '1-2-3'
        groups = re.split('[-]', groups) # ['1','2','3']
        layout = str(self.ui.labelLayout.text())
        try:
            self.caller.plot_group_average(groups, layout)
        except Exception as e:
            mBox = messageBoxes.shortMessageBox('Error while visualizing.\n' +\
                                                str(e))
            mBox.exec_()
        finally:
            QtGui.QApplication.restoreOverrideCursor()
        
    
    def on_pushButtonSaveEvoked_clicked(self, checked=None):
        """
        TODO: Save the evoked data (for exporting purposes if needed)
        not working currently (overwrites the same existing raw file)
        """
        if checked is None: return
        evoked_collection_name = str(self.evokedList.currentItem().text())
        evoked = self.caller.experiment.active_subject._evokeds[evoked_name]
        evoked_raw = evoked._raw
        """
        TODO: get evoked from active_subject._evokeds dictionary
        """
        
        saveFolder = os.path.join(self.caller.experiment.active_subject._epochs_directory, 'average')
        if os.path.exists(saveFolder) is False:
            try:
                os.mkdir(saveFolder)
            except IOError:
                print 'Writing to selected folder is not allowed.'
            
        try:                
            # TODO: best filename option ? (_auditory_and_visual_eeg-ave)
            print 'Writing evoked data as ' + evoked_collection_name + ' ...'
            fiff.write_evokeds(os.path.join(saveFolder, evoked_collection_name), evokeds)
            print '[done]'
        except IOError:
            print 'Writing to selected folder is not allowed.'

        
    def on_pushButtonLoadEvoked_clicked(self, checked=None):
        """
        TODO: Load evoked data (for importing purposes if needed)
        not working currently
        """
        if checked is None: return
        fname = str(QtGui.QFileDialog.\
                    getOpenFileName(self, 'Load evokeds', os.path.join(\
                                                      self.caller.experiment.\
                                                      active_subject.\
                                                      _epochs_directory, \
                                                      'average')))
        if fname == '': return
        if not os.path.isfile(fname): return
        split = os.path.split(fname)
        #folder = split[0] + '/'
        name = os.path.splitext(split[1])[0]
        # TODO: add path and filename for load_evoked, split fname correctly to do this
        evoked, category = fileManager.load_evoked(fname + '.fif')
        if evoked is None: return
        item = QtGui.QListWidgetItem(file)
        self.evokedList.addItem(item)
        self.evokedList.setCurrentItem(item)
        self.caller.experiment.active_subject.handle_new_evoked(item.text(), evoked, category)
        
        
    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Opens a dialog for selecting a layout file.
        """
        if checked is None: return
        fName = str(QtGui.QFileDialog.getOpenFileName(self,
                            "Select a layout file", '/home/', 
                            "Layout-files (*.lout *.lay);;All files (*.*)"))
        self.ui.labelLayout.setText(fName)

        
    def on_pushButtonDeleteEpochs_clicked(self, checked=None):
        """Delete the selected epoch item and the files related to it.
        """
        if checked is None:
            return
        
        if self.epochList.isEmpty():
            return
        
        elif self.epochList.currentItem() is None:
            self.messageBox = messageBoxes.shortMessageBox('No epochs selected.')
            self.messageBox.show()
            
        item_str = self.epochList.currentItem().text()
            
        root = self.caller.experiment.active_subject._epochs_directory
        message = 'Permanently remove epochs and the related files?'
            
        reply = QtGui.QMessageBox.question(self, 'delete epochs',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            self.caller.experiment.active_subject.remove_epochs(item_str)
            self.epochList.remove_item(self.epochList.currentItem())
        if self.epochList.ui.listWidgetEpochs.count() == 0:
            self.clear_epoch_collection_parameters()

            
    def on_pushButtonDeleteEvoked_clicked(self, checked=None):
        """Delete the selected evoked item and the files related to it.
        """
                
        if checked is None:
            return
        
        if self.evokedList.count() == 0:
            return
        
        elif self.evokedList.currentItem() is None:
            self.messageBox = messageBoxes.shortMessageBox('No evokeds selected.')
            self.messageBox.show()
            
        item_str = self.evokedList.currentItem().text()
            
        root = os.path.join(self.caller.experiment.active_subject._epochs_directory, 'average')
        message = 'Permanently remove evokeds and the related files?'
            
        reply = QtGui.QMessageBox.question(self, 'delete evokeds',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            #self.delete_epochs(self.ui.evokedList.currentItem())
            item = self.evokedList.currentItem()
            row = self.evokedList.row(item)
            self.evokedList.takeItem(row)
            #fileManager.delete_file_at(root, item_str)
            self.caller.experiment.active_subject.remove_evoked(item_str)
        else:
            return

                    
    def on_pushButtonMNE_Browse_Raw_clicked(self, checked=None):
        """
        Call mne_browse_raw.
        """
        if checked is None: return
        if self.caller.experiment is None: return
        # TODO: change scales ja muita optioita
        try:
            self.caller.call_mne_browse_raw(self.caller.experiment.active_subject._working_file.\
                                            info.get('filename'))
        except Exception, err:
            self.messageBox = messageBoxes.shortMessageBox(str(err))
            self.messageBox.show()
            return
        """
        #Another way of viewing the raw:
        self.experiment.active_subject._working_file.plot()
        pl.show()
        """

    def on_pushButtonMaxFilter_clicked(self, checked=None):
        """
        Call Elekta's MaxFilter.
        """
        if checked is None: return 
        try:
            self.maxFilterDialog = MaxFilterDialog(self, 
                                                   self.caller.experiment.active_subject.working_file)
        except Exception, err:
            title = 'MaxFilter error:'
            self.messageBox = messageBoxes.longMessageBox(title, str(err))
            self.messageBox.show()
            return
        self.maxFilterDialog.show()

        
    def on_pushButtonSpectrum_clicked(self, checked=None):
        """
        Open the magnitude spectrum visualization dialog.
        """
        """
        self.spectrumDialog = SpectrumDialog(self)
        self.spectrumDialog.show()
        """
        if checked is None: return
        spectrumDialog = PowerSpectrumDialog(self)
        spectrumDialog.exec_()
                
        
    def on_pushButtonEOG_clicked(self, checked=None):
        """
        Open the dialog for calculating the EOG PCA.
        """
        if checked is None: return 
        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.computed.connect(self.ui.checkBoxEOGComputed.setChecked)
        self.eogDialog.show()

        
    def on_pushButtonECG_clicked(self, checked=None):
        """
        Open the dialog for calculating the ECG PCA.
        """
        if checked is None: return
        self.ecgDialog = EcgParametersDialog(self)
        self.ecgDialog.show()

        
    def on_pushButtonApplyEOG_clicked(self, checked=None):
        """
        Open the dialog for applying the EOG-projections to the data.
        """
        if checked is None: return
        self.addEogProjs = AddEOGProjections(self)
        self.addEogProjs.exec_()

        
    def on_pushButtonApplyECG_clicked(self, checked=None):
        """
        Open the dialog for applying the ECG-projections to the data.
        """
        if checked is None: return
        self.addEcgProjs = AddECGProjections(self)
        self.addEcgProjs.exec_()

        
    def on_pushButtonTFR_clicked(self, checked=None):
        """
        Open the dialog for plotting TFR from a single channel.
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must create epochs before TFR.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        epochs_collection_name = str(self.epochList.ui.listWidgetEpochs.\
                                     currentItem().text())
        epochs = self.caller.experiment.active_subject._epochs[epochs_collection_name]
        epochs_raw = epochs._raw
        self.tfr_dialog = TFRDialog(self, self.caller.experiment.active_subject.\
                                    _working_file, epochs_raw)
        self.tfr_dialog.show()
    
    
    def on_pushButtonTFRTopology_clicked(self,checked=None):
        """
        Opens the dialog for plotting TFR topology.
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must create epochs before TFR.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        epochs_collection_name = str(self.epochList.ui.listWidgetEpochs.\
                                     currentItem().text())
        epochs = self.caller.experiment.active_subject._epochs[epochs_collection_name]
        self.tfrTop_dialog = TFRTopologyDialog(self, 
                                               self.caller.experiment.active_subject.\
                                               _working_file, 
                                               epochs._raw)
        self.tfrTop_dialog.exec_()
    
        
    def on_pushButtonChannelAverages_clicked(self, checked=None):
        """
        Shows the channels average graph.
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.currentItem() is None: 
            message = 'Please select an epoch collection to channel average.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()  
            return
        
        """
        TODO: get epochs from active_subject._epochs dictionary
        """
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        epochs_name = str(self.epochList.ui.listWidgetEpochs.\
                          currentItem().text())
        #epochs = self.caller.experiment.active_subject._epochs[epochs_name]._raw
        if self.ui.radioButtonLobe.isChecked() == True:
            self.caller.average_channels(epochs_name, self.ui.comboBoxLobes.\
                                         currentText(), None)
        else:
            channels = []
            for i in xrange(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                channels.append(str(item.text()))
            self.caller.average_channels(epochs_name, None, set(channels))
        QtGui.QApplication.restoreOverrideCursor()
        
        
    def on_pushButtonModifyChannels_clicked(self, checked=None):
        """
        Slot for adding channels to the list for averaging epochs.
        """
        if checked is None: return
        channels = []
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
        if checked is None: return
    
        self.filterDialog = FilterDialog(self)
        self.filterDialog.show()
    
    
    def on_pushButtonActivateSubject_clicked(self, checked=None):
        """
        Activates a subject.
        """
        if checked is None: return
        if self.ui.listViewSubjects.selectedIndexes() == []: return
        
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        selIndexes = self.ui.listViewSubjects.selectedIndexes()
        subject_name = selIndexes[0].data()
        
        
        # Not much point trying to activate an already active subject.
        if subject_name == self.caller.experiment.active_subject_name:
            return      
        # This prevents taking the epoch list currentItem from the previously
        # open subject when activating another subject.
        self.clear_epoch_collection_parameters()
        self.caller.activate_subject(subject_name)
        self._initialize_ui()
        
        # To tell the MVC models that the active subject has changed.
        self.reinitialize_models() 
        QtGui.QApplication.restoreOverrideCursor()


    def on_pushButtonBrowseRecon_clicked(self, checked=None):
        """
        Copies reconstructed mri files from the directory supplied by the user
        to the corresponding directory under the active subject directory
        """
        
        if checked is None : return
        
        activeSubject = self.caller.experiment._active_subject
        
        # Probably not created yet, because this is the first step of source
        # analysis.
        if not os.path.isdir(activeSubject._source_analysis_directory):
            activeSubject.create_sourceAnalysis_directory()
        
        if activeSubject.check_reconFiles_copied():
            reply = QtGui.QMessageBox.question(self, 'Please confirm',
            "Do you really want to change the reconstructed files? This will " +
            " invalidate all later source analysis work and clear the results "+ 
            "of the later phases",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        
            if reply == QtGui.QMessageBox.No:
                return
        
        path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select directory of the reconstructed MRI image"))
        if path == '':
            return
        
        mriDir = os.path.join(path, 'mri')
        surfDir = os.path.join(path, 'surf')  
        if not (os.path.isdir(mriDir) and os.path.isdir(surfDir)):
            message = "Reconstructed image directory should have both 'surf' " + \
             "and 'mri' directories in it."
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox.exec_()
            return  
        
        activeSubject = self.caller.experiment._active_subject
          
        try: 
            fileManager.copy_recon_files(activeSubject, path)
            self.ui.lineEditRecon.setText(path)
        except Exception:
            message = 'Could not copy files. Either the disk is full ' + \
            ' , you have no rights to read the directory or something weird' + \
            ' happened.'
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox.exec_()   
            
        self._initialize_ui()
        
        
    def on_pushButtonConvertToMNE_clicked(self, checked=None):
        if checked is None : return
        
        self.caller.convert_mri_to_mne()
        self._initialize_ui()
            
        
    def on_pushButtonCreateNewForwardModel_clicked(self, checked=None):
        """
        Open up a dialog for creating a new forward model.
        """
        if checked is None: return
        
        self.fmodelDialog = ForwardModelDialog(self)
        self.fmodelDialog.show()
        

    def on_pushButtonRemoveSelectedForwardModel_clicked(self, checked=None):
        """
        Removes selected forward model from the forward model list and
        from the disk.
        """
        if checked is None: return
        
        if self.ui.tableViewForwardModels.selectedIndexes() == []:
            message = 'Please select a forward model to remove.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        reply = QtGui.QMessageBox.question(self, 'Removing forward model',
                'Do you really want to ' + \
                'the selected forward model, including the coregistration ' + \
                'and forward solution files related to it?',                                            
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
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
            message = 'There was a problem removing forward model. Nothing ' + \
            'was removed.'
            self. messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()


    def on_pushButtonBrowseCoregistration_clicked(self, checked=None):
        """
        Open a file browser dialog for the user to choose
        a translated coordinate file to use with the currently selected forward
        model.
        """
        if checked is None: return
        
        activeSubject = self._experiment._active_subject
        tableView = self.ui.tableViewFModelsForCoregistration
        
        # Selection for the view is SingleSelection / SelectRows, so this
        # should return indexes for single row.
        selectedRowIndexes = tableView.selectedIndexes()
        selectedFmodelName = selectedRowIndexes[0].data() 
        
        subjectPath = activeSubject._subject_path
        targetName = os.path.join(subjectPath, 'sourceAnalysis', 'forwardModels',
                                  selectedFmodelName, 'reconFiles',
                                  'reconFiles-trans.fif')   
    
        path = QtGui.QFileDialog.getOpenFileName(
               self, 'Select the existing coordinate file ' +
               '(the file should end with "-trans.fif")' )
        if path == '':
            return
        else: 
            try:
                shutil.copyfile(path, targetName)
            except IOError:
                message = 'There was a problem while copying the coordinate file.'
                messageBox = messageBoxes.shortMessageBox(message)
                messageBox.exec_()
        
        self.forwardModelModel.initialize_model()
        
    
    def on_pushButtonMNECoregistration_clicked(self, checked=None):
        """
        Open a dialog for coregistering the currently selected
        forward model in tableViewFModelsForCoregistration.
        """
        if checked is None: return
        
        if self.ui.tableViewFModelsForCoregistration.selectedIndexes() == []:
            message = 'Please select a forward model to (re-)coregister.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        self.caller.coregister_with_mne_gui_coregistration()
        
        
    def on_pushButtonCreateForwardSolution_clicked(self, checked=None):
        """
        Open a dialog for creating a forward solution for the currently selected
        forward model in tableViewFModelsForSolution.
        """
        if checked is None: return
        
        if self.ui.tableViewFModelsForSolution.selectedIndexes() == []:
            message = 'Please select a forward model to (re)create a forward ' + \
            'solution for.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        self.fSolutionDialog = ForwardSolutionDialog(self)
        self.fSolutionDialog.show()
        
        
    def on_pushButtonMNE_AnalyzeCoregistration_clicked(self, checked=None):
        if checked is None: return
        # TODO: Implement this last if needed.
        return


    def on_pushButtonComputeCovarianceRaw_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on raw file
        (measurement file with a subject but without epochs, or an empty room 
        measurement).
        """
        if checked is None: return
        
        self.covarianceRawDialog = CovarianceRawDialog(self)
        self.covarianceRawDialog.show()    
          
    
    def on_pushButtonComputeCovarianceEpochs_clicked(self, checked=None):
        """
        Open a dialog for computing noise covariance matrix based on data before
        epochs.
        """
        if checked is None: return
    
    

### Code for populating and updating various lists and tables in the MainWindow ###       
    
    

### Code for UI initialization (when starting the program) and updating when something changes ### 
    
    def _initialize_ui(self):
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
        self.evokedList.clear()
        
        # Clears and sets labels, checkboxes etc. on mainwindow.
        self.ui.textBrowserEvents.clear()
        self.ui.labelDateValue.clear()
        self.ui.labelEEGValue.clear()
        self.ui.labelGradMEGValue.clear()
        self.ui.labelHighValue.clear()
        self.ui.labelLowValue.clear()
        self.ui.labelMagMEGValue.clear()
        self.ui.labelSamplesValue.clear()
        self.ui.labelSubjectValue.clear()
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
        self.ui.pushButtonCreateNewForwardModel.setEnabled(False)
        
        if self.caller.experiment.active_subject is not None:
            # Populate epoch and evoked lists
            epochs_items = self.caller.experiment.load_epochs(self.caller.experiment.active_subject)
            evokeds_items = self.caller.experiment.load_evokeds(self.caller.experiment.active_subject)
            if epochs_items is not None:
                for item in epochs_items:
                    self.epochList.addItem(item)
                    self.epochList.setCurrentItem(item)
            if evokeds_items is not None:
                for item in evokeds_items:
                    self.evokedList.addItem(item)
                    self.evokedList.setCurrentItem(item)
            
            # This updates the 'Subject info' section below the subject list.
            InfoDialog(self.caller.experiment.active_subject.working_file,
                        self.ui, False)
            if self.caller.experiment.active_subject._event_set is not None:
                self.populate_raw_tab_event_list()    
            
        self.setWindowTitle('Meggie - ' + self.caller.experiment.experiment_name)
        if self.caller.experiment.active_subject is None:
            self.statusLabel.setText("Add or activate" + \
                                     " subjects before " + \
                                     "continuing.")
            return
        else:
            status = "Current working file: " + \
            os.path.basename(self.caller._experiment._working_file_names[self.caller.experiment._active_subject_name])
            self.statusLabel.setText(status)
            
            try:
                #Check whether ECG projections are calculated
                if self.caller.experiment.active_subject.check_ecg_projs():
                    self.ui.pushButtonApplyECG.setEnabled(True)
                    self.ui.checkBoxECGComputed.setChecked(True)
                #Check whether EOG projections are calculated
                if self.caller.experiment.active_subject.check_eog_projs():
                    self.ui.pushButtonApplyEOG.setEnabled(True)
                    self.ui.checkBoxEOGComputed.setChecked(True)
                #Check whether ECG projections are applied
                if self.caller.experiment.active_subject.check_ecg_applied():
                    self.ui.checkBoxECGApplied.setChecked(True)
                #Check whether EOG projections are applied
                if self.caller.experiment.active_subject.check_eog_applied():
                    self.ui.checkBoxEOGApplied.setChecked(True)
                #Check whether sss/tsss method is applied.
                if self.caller.experiment.active_subject.check_sss_applied():
                    self.ui.checkBoxMaxFilterComputed.setChecked(True)
                    self.ui.checkBoxMaxFilterApplied.setChecked(True)
            except AttributeError:
                print 'No active subject in experiment.'
                
        # Check whether reconstructed mri files have been copied to the recon
        # files directory under the subject and set up the UI accordingly.
        if self.caller._experiment._active_subject.check_reconFiles_copied():
            self.ui.lineEditRecon.setText('Reconstructed mri image already ' + 
                                          'copied.')
            self.ui.pushButtonConvertToMNE.setEnabled(True)
            self.ui.pushButtonCheckTalairach.setEnabled(True)
            self.ui.pushButtonSkullStrip.setEnabled(True)
            self.ui.pushButtonCheckSurfaces.setEnabled(True)
            self.ui.pushButtonCheckSegmentations.setEnabled(True)
        
        # Check if MRI image has been setup with mne_setup_forward solution
        if self.caller._experiment._active_subject.check_mne_setup_mri_run():
            self.ui.checkBoxConvertedToMNE.setChecked(True)
            self.ui.pushButtonCreateNewForwardModel.setEnabled(True)
        
        projs = self.caller.experiment._active_subject.working_file.info['projs']
        self.ui.listWidgetProjs.clear()
        for proj in projs:
            self.ui.listWidgetProjs.addItem(str(proj))
        
        bads = self.caller.experiment._active_subject.working_file.info['bads']
        self.ui.listWidgetBads.clear()
        for bad in bads:
            self.ui.listWidgetBads.addItem(bad)
        
        self.update_covariance_info_box()

    
    def update_covariance_info_box(self):
        """
        Fills the info box in the covariance tab with info about the
        current covariance matrix info for the active subject, if said info
        exists.
        """
        
        cvParamFilePath = os.path.join(self.caller.experiment.active_subject.
        _source_analysis_directory, 'covariance.param')
        
        cvdict = None
        if os.path.isfile(cvParamFilePath):
            try:
                cvdict = fileManager.unpickle(cvParamFilePath)
            except Exception:
                pass
        
        if self.ui.frameCovarianceInfoWidget.layout() != None:
            sip.delete(self.ui.frameCovarianceInfoWidget.layout())
        
        for child in self.ui.frameCovarianceInfoWidget.children():
            child.setParent(None)
        
        covLayout = QtGui.QGridLayout()
        self.ui.frameCovarianceInfoWidget.setLayout(covLayout)
        
        if cvdict == None:
            covarianceWidgetNone = CovarianceWidgetNone()
            covLayout.addWidget(covarianceWidgetNone)
            return
        
        if cvdict['covarianceSource'] == 'raw':
            covarianceWidgetRaw = CovarianceWidgetRaw()
            cvwui = covarianceWidgetRaw.ui
            if cvdict['rawsubjectname'] != None:
                cvwui.textBrowserBasedOn.setText(cvdict['rawsubjectname'])
            else:
                cvwui.textBrowserBasedOn.setText(cvdict['rawfilepath'])
            cvwui.textBrowserTmin.setText(str(cvdict['starttime']))
            cvwui.textBrowserTmax.setText(str(cvdict['endtime']))
            cvwui.textBrowserTstep.setText(str(cvdict['tstep']))
            if cvdict['reject'] != None:
                cvwui.textBrowserGradPeakCovariance.setText(
                str(cvdict.get('reject').get('grad', '')))
                cvwui.textBrowserMagPeakCovariance.setText(
                str(cvdict.get('reject').get('mag', '')))
                cvwui.textBrowserEEGPeakCovariance.setText(
                str(cvdict.get('reject').get('eeg', '')))
                cvwui.textBrowserEOGPeakCovariance.setText(
                str(cvdict.get('reject').get('eog', '')))
            if cvdict['flat'] != None:
                cvwui.textBrowserFlatGrad.setText(
                str(cvdict.get('flat').get('grad', '')))
                cvwui.textBrowserFlatMag.setText(
                str(cvdict.get('flat').get('mag', '')))
                cvwui.textBrowserFlatEEG.setText(
                str(cvdict.get('flat').get('eeg', '')))
                cvwui.textBrowserFlatEOG.setText(
                str(cvdict.get('flat').get('eog', '')))
                cvwui.textBrowserFlatECG.setText(
                str(cvdict.get('flat').get('ecg', 'Not used')))
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
        #TODO: trigger ---> event, also in the UI
        events = self.caller.experiment.active_subject._event_set
        
        
        events_string = ''
        for key, value in events.iteritems():
            events_string += 'Event ' + str(key) + ', ' + str(value) +\
            ' events\n'
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
        """
        Method for initializing the tabs.
        """
        self.ui.tabWidget.insertTab(1, self.ui.tabPreprocessing, 
                                    "Preprocessing")
        self.ui.tabWidget.insertTab(2, self.ui.tabEpoching, "Epoching")
        self.ui.tabWidget.insertTab(3, self.ui.tabAveraging, "Averaging")
        self.ui.tabWidget.insertTab(4, self.ui.tabTFR, "TFR")
        self.ui.tabWidget.insertTab(5, self.ui.tabSourcePreparation, "Source modelling preparation")
        self.ui.tabWidget.insertTab(6, self.ui.tabForwardModel, "Forward model creation")
        self.ui.tabWidget.insertTab(7, self.ui.tabCoregistration, "Coregistration")
        self.ui.tabWidget.insertTab(8, self.ui.tabForwardSolution, "Forward solution creation")
        self.ui.tabWidget.insertTab(9, self.ui.tabNoiseCovariance, "Noise covariance")
        self.ui.tabWidget.insertTab(10, self.ui.tabInverseOperator, "Inverse operator")
        self.ui.tabWidget.insertTab(11, self.ui.tabSourceEstimate, "Source estimate")
        self.ui.tabWidget.insertTab(12, self.ui.tabSourceAnalysis, "Source analysis")
        

    def on_currentChanged(self):
            """
            TODO: should use a proper mcv system to avoid this crap.
            Keep track of the active tab.
            Show the epoch collection list epochList when in appropriate tabs.
            """
            index = self.ui.tabWidget.currentIndex()
            #self.tab = self.ui.tabWidget.currentWidget()
             
            if index == 1:
                self.epochList.setParent(self.ui.groupBoxEpochsEpoching)
                #self.epochParamsList.setParent(self.ui.groupBoxEpochParamsEpoching)
                self.epochList.show()
                #self.epochParamsList.show()
                return
            
            if index == 2:
                self.epochList.setParent(self.ui.groupBoxEpochsAveraging)
                #self.epochParamsList.setParent(self.ui.groupBoxEpochParamsAveraging)
                self.epochList.show()
                #self.epochParamsList.show()
                return
           
            if index == 3:
                self.epochList.setParent(self.ui.groupBoxEpochsTFR)
                #self.epochParamsList.setParent(self.ui.groupBoxEpochParamsTFR)
                self.epochList.show()
                #self.epochParamsList.show()
                return 
                
            else:
                self.epochList.hide()
                #self.epochParamsList.hide()


    def reinitialize_models(self):
        """
        Tell all the MVC models of the views in Meggie that they should
        (re)initialize themselves. Should only be needed when active subject
        changes, updating the models when items are added to them is based
        on events.
        """
        self.forwardModelModel.initialize_model()
        self.subjectListModel.initialize_model()


### Miscellaneous code ###

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
        self.preferencesDialog = PreferencesDialog(self)
        self.preferencesDialog.exec_()


    def hide_workspace_option(self):
        self.ui.actionSet_workspace.setVisible(False)
        

    """
    @atexit.register
    def terminate_subprocesses(self, procs):
        
        TODO: currently of no use, as this does not run when Meggie is simply
        killed (and the only way to shutdown Meggie mid-processing
        with current unthreaded design is by killing it with SIGKILL) 
        For terminating MNE-C subprocesses at Meggie exit.
        
        for proc in self.processes:
            proc.terminate()
    """
    
    
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


class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
        
    def flush(self):
        pass
        
### Code related to application initialization ###     


def exception_hook(exctype, value, tracebackObj):
    print str(exctype) + ': ' + str(value)
    traceback.print_tb(tracebackObj)
    title = 'Unknown error'
    message = 'Something unexpected happened. Please copy the following ' + \
    'to your bug report:\n\n' + 'Exception type: ' + str(exctype) + '\n\n' + \
    'Exception value: ' + str(value) + '\n\n\n' + 'Traceback:\n\n' + \
    ''.join(traceback.format_tb(tracebackObj))
    messagebox = messageBoxes.longMessageBox(title, message)
    messagebox.exec_()
   
        
def main():
    sys.excepthook = exception_hook
    
    app = QtGui.QApplication(sys.argv)
    window=MainWindow(app)
            
    window.showMaximized()
    
    sys.exit(app.exec_())