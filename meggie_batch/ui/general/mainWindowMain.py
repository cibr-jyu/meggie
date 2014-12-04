# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
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

import os,sys
 
from PyQt4 import QtCore,QtGui
from PyQt4.QtGui import QWhatsThis, QFont


from mne import fiff

import matplotlib
matplotlib.use('Qt4Agg')
import pylab as pl
from caller import Caller

# For using MNE-Python drawing methods in separate processes
# (can't use threads, as MNE-Python usually uses pyplot, which is not thread-
# safe)
import multiprocessing

from mainWindowUi import Ui_MainWindow
from createExperimentDialogMain import CreateExperimentDialog
from addSubjectDialogMain import AddSubjectDialog
from infoDialogMain import InfoDialog
from eventSelectionDialogMain import EventSelectionDialog
from eventSelectionDialogUi import Ui_EventSelectionDialog
from visualizeEpochChannelDialogMain import VisualizeEpochChannelDialog
from maxFilterDialogMain import MaxFilterDialog
from eogParametersDialogMain import EogParametersDialog
from ecgParametersDialogMain import EcgParametersDialog
# from workSpaceDialogMain import WorkSpaceDialog
from preferencesDialogMain import PreferencesDialog
from evokedStatsDialogMain import EvokedStatsDialog
from addECGProjectionsMain import AddECGProjections
from addEOGProjectionsMain import AddEOGProjections
from TFRDialogMain import TFRDialog
from TFRTopologyDialogMain import TFRTopologyDialog
from spectrumDialogMain import SpectrumDialog
from epochWidgetMain import EpochWidget
from aboutDialogMain import AboutDialog
from filterDialogMain import FilterDialog
from forwardModelDialogMain import ForwardModelDialog
from experimentInfoDialogMain import experimentInfoDialog
import messageBoxes

import experiment
from epochs import Epochs
from events import Events
from prefecences import PreferencesHandler
import fileManager
from listWidget import ListWidget
from mvcModels import ForwardModelModel

class MainWindow(QtGui.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """
    
    #custom signals
    #experiment_value_changed was made useless. All the stuff moved to
    #_initialize_ui() method.
    #experiment_value_changed = QtCore.pyqtSignal()


    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Main window represents one _experiment at a time. This _experiment is
        # defined by the CreateExperimentDialog or the by the Open_experiment_
        # triggered action.
        self._experiment = None
        
        # One main window (and one _experiment) only needs one caller to do its
        # bidding. 
        self.caller = Caller(self)
       
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
        
        self.epocher = Epochs()
        
        # Populate the combobox for selecting lobes for channel averages.
        self.populate_comboBoxLobes()
        
        # Connect signals and slots
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)
        self.epochList.item_added.connect(self.epochs_added)
        self.ui.pushButtonMNE_Browse_Raw_2.clicked.connect(
                              self.on_pushButtonMNE_Browse_Raw_clicked)
        
        # TODO should show empty mainWindow with "loading previous experiment
        # named <name>"-notification to user before starting to load
        # the experiment, currently doesn't.
        # If the user has chosen to open the previous experiment automatically.
        if self.preferencesHandler.auto_load_last_open_experiment is True:
            name = self.preferencesHandler.previous_experiment_name
            self.experimentHandler.open_existing_experiment(name)
        
        
        # Models for several views in tab, e.g. forward model setup tab. 
        # Also linking corresponding views to models.
        
        if self._experiment != None:
            self.forwardModelModel = ForwardModelModel(self._experiment, self)
            self.ui.tableViewForwardModels.setModel(self.forwardModelModel) 
            self.ui.tableViewFModelsForCoregistration.setModel(
                                                      self.forwardModelModel)
    
        
        
    #Property definitions below
    @property
    def experiment(self):
        return self._experiment

    
    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment
        
        
        
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
            self.dialog.show()
        else:
            self.check_workspace()
            if self.preferencesHandler.working_directory != '':
                self.dialog = CreateExperimentDialog(self)
                self.dialog.show()   

        
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
        if self._experiment is None:
            message = 'No active experiment to add a subject to. ' \
            + 'Load an experiment or make a new one, then try again.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
                
        self.subject_dialog = AddSubjectDialog(self)
        self.subject_dialog.show()

    
    def on_pushButtonRemoveSubject_clicked(self, checked=None):
        """Delete the selected subject item and the files related to it.
        """
        if checked is None:
            return
        
        if self.ui.listWidgetSubjects.count() == 0:
            return
        
        elif self.ui.listWidgetSubjects.currentItem() is None:
            self.messageBox = messageBoxes.shortMessageBox('No subject selected.')
            self.messageBox.show()
            return
            
        item_str = self.ui.listWidgetSubjects.currentItem().text()
            
        message = 'Permanently remove subject and the related files?'
            
        reply = QtGui.QMessageBox.question(self, 'delete subject',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            self.experiment.remove_subject(self.ui.listWidgetSubjects.currentItem(), self)
            # TODO: listWidgetSubects.currentItem() should be removed here

        
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
        self.epochParameterDialog = EventSelectionDialog(self, self.\
                                                         experiment.\
                                                         active_subject.\
                                                         working_file)
        self.epochParameterDialog.epoch_params_ready.\
        connect(self.create_new_epochs)
        self.epochParameterDialog.show()

        
    @QtCore.pyqtSlot(QtGui.QListWidgetItem)
    def epochs_added(self, item):
        """
        A slot for saving epochs from the added QListWidgetItem to a file.
        """
        if os.path.exists(self.experiment.active_subject._epochs_directory) is False:
            self.experiment.active_subject.create_epochs_directory
        fname = str(item.text())
        fpath = os.path.join(self.experiment.active_subject._epochs_directory, fname)
        epochs_object = self.experiment.active_subject._epochs[fname]
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
                                                      self.experiment.\
                                                      active_subject.\
                                                      _working_file)
        epoch_params['raw'] = self.experiment.\
        _working_file_names[self.experiment._active_subject_name]
        
        fname = epoch_params['collectionName']
        item = QtGui.QListWidgetItem(fname)
        self.experiment.active_subject.handle_new_epochs(fname, epochs, epoch_params)
        self.epochList.addItem(item)
        self.epochList.setCurrentItem(item)

        
    def on_pushButtonLoadEpochs_clicked(self, checked=None):
        """Load epochs from a folder.
        
        Epochs are copied to /experiment/epochs. If parameters are available,
        they are saved as well.
        """
        if checked is None: return
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Load epochs',
                                                      self.experiment.\
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
        self.experiment.active_subject.handle_new_epochs(fname_prefix, epochs, params)
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
        params = self.experiment.active_subject._epochs[collection_name]._params
        self.epochParameterDialog = EventSelectionDialog(self, self.\
                                                         experiment.\
                                                         active_subject.working_file,
                                                         params)

        # modify_epochs removes the previous Epochs object and raw files
        # created from it and creates new Epochs object and raw files.
        # Also removes the epochWidget item and replaces it with the new one.
        self.epochParameterDialog.epoch_params_ready.\
        connect(self.experiment.active_subject.modify_epochs)
        self.epochParameterDialog.show()

                
    def on_pushButtonSaveEpochs_clicked(self, checked=None):
        """Save the epoch collections to a .fif file 
        """
        if checked is None: return
        fname = str(QtGui.QFileDialog.getSaveFileName(self, 'Save epochs',
                                                      self.experiment.\
                                                      active_subject.\
                                                      _epochs_directory))
        if fname == '': return
        else: 
            """
            TODO: get epochs from active_subject._epochs dictionary
            """
            collection_name = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
            epochs = self.experiment.active_subject._epochs[collection_name]._raw
            epochs.save(fname)
        #Also copy the related csv-file to the chosen folder
        fileManager.copy(os.path.join(self.experiment.active_subject.\
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
        self.expInfoDialog = experimentInfoDialog(self)
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
        if checked is None: return
        # If no events are selected, show a message to to the user and return.
        if self.epochList.ui.listWidgetEpochs.currentItem() is None: 
            message = 'Please select an epoch collection to average.' 
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()  
            return
        key = str(self.epochList.ui.listWidgetEpochs.currentItem().text())
        epochs = self.experiment.active_subject._epochs[key]
        
        category = epochs._raw.event_id
        
        # New dictionary for event categories must be created, if user
        # manually chooses different event categories to be averaged. 
        if len(self.epochList.ui.listWidgetEvents.selectedItems()):
            category_user_chosen = dict()
            for event in self.epochList.ui.listWidgetEvents.selectedItems():
                event_name = (str(event.text())).split(':')
                category_user_chosen[event_name[0]] = epochs._raw.event_id.get(event_name[0])
            evoked = self.caller.average(epochs._raw,category_user_chosen)
            category = category_user_chosen
        else:
            evoked = self.caller.average(epochs._raw,category)
        
        category_str = ''
        i = 0
        for key in category.keys():
            if i == 0:
                category_str += key
                i = 1
            else:
                category_str += '-' + key
        epoch_collection = self.epochList.ui.listWidgetEpochs.currentItem()
        evoked_name = str(epoch_collection.\
                          text() + '[' + category_str + ']' + '_evoked.fif')
        item = QtGui.QListWidgetItem(evoked_name)
        
        # TODO: create separate method in fileManager to save evoked
        # Save evoked into evoked (average) directory with name evoked_name
        saveFolder = self.experiment.active_subject._evokeds_directory
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
            fiff.write_evoked(os.path.join(saveFolder, evoked_name), evoked)
            print '[done]'
        except IOError:
            message = 'Writing to selected folder is not allowed. You can still' \
                      + ' process the evoked file (visualize etc.).'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.labelException.setText \
            ()
            self.messageBox.show()
        
        
        self.evokedList.addItem(item)
        self.experiment.active_subject.handle_new_evoked(evoked_name, evoked, category)
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
            evoked = self.experiment.active_subject._evokeds[evoked_name]._raw
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
        epochs = self.experiment.active_subject._epochs[epochs_name]._raw
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
        
        # Cue for the user that we are preparing visualization.
        # TODO: should use threads and events.
        self.ui.pushButtonVisualizeEvokedDataset.setText(
                                    '      Visualizing...      ')
        self.ui.pushButtonVisualizeEvokedDataset.setEnabled(False)
        QtCore.QCoreApplication.processEvents()
        
        evoked_name = str(self.evokedList.currentItem().text())
        evoked = self.experiment.active_subject._evokeds[evoked_name]
        evoked_raw = evoked._raw
        category = evoked._categories
        
        print 'Meggie: Visualizing evoked collection ' + evoked_name + ' ...\n'
        self.caller.draw_evoked_potentials(evoked_raw, category)
        print 'Meggie: Evoked collection ' + evoked_name + ' visualized! \n'
        
        oldText = 'Visualize selected dataset'
        self.ui.pushButtonVisualizeEvokedDataset.setText(oldText)
        self.ui.pushButtonVisualizeEvokedDataset.setEnabled(True)
              
    
    def on_pushButtonSaveEvoked_clicked(self, checked=None):
        """
        TODO: Save the evoked data (for exporting purposes if needed)
        not working currently (overwrites the same existing raw file)
        """
        if checked is None: return
        evoked_collection_name = str(self.evokedList.currentItem().text())
        evoked = self.experiment.active_subject._evokeds[evoked_name]
        evoked_raw = evoked._raw
        """
        TODO: get evoked from active_subject._evokeds dictionary
        """
        
        saveFolder = os.path.join(self.experiment.active_subject._epochs_directory, 'average')
        if os.path.exists(saveFolder) is False:
            try:
                os.mkdir(saveFolder)
            except IOError:
                print 'Writing to selected folder is not allowed.'
            
        try:                
            # TODO: best filename option ? (_auditory_and_visual_eeg-ave)
            print 'Writing evoked data as ' + evoked_collection_name + ' ...'
            fiff.write_evoked(os.path.join(saveFolder, evoked_collection_name), evokeds)
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
                                                      self.experiment.\
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
        self.experiment.active_subject.handle_new_evoked(item.text(), evoked, category)

        
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
            
        root = self.experiment.active_subject._epochs_directory
        message = 'Permanently remove epochs and the related files?'
            
        reply = QtGui.QMessageBox.question(self, 'delete epochs',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            self.experiment.active_subject.remove_epochs(item_str)
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
            
        root = os.path.join(self.experiment.active_subject._epochs_directory, 'average')
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
            self.experiment.active_subject.remove_evoked(item_str)
        else:
            return

                    
    def on_pushButtonMNE_Browse_Raw_clicked(self, checked=None):
        """
        Call mne_browse_raw.
        """
        if checked is None: return
        # TODO: change scales ja muita optioita
        self.experiment.active_subject._working_file.plot()
        pl.show()
        """
        try:
            self.caller.call_mne_browse_raw(self.experiment.active_subject._working_file.\
                                            info.get('filename'))
        except Exception, err:
            self.messageBox = messageBox.shortMessageBox()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            return        
        """

        
    def on_pushButtonMaxFilter_clicked(self, checked=None):
        """
        Call Elekta's MaxFilter.
        """
        if checked is None: return 
        try:
            self.maxFilterDialog = MaxFilterDialog(self, 
                                                   self.experiment.active_subject.working_file)
        except Exception, err:
            title = 'MaxFilter error:'
            self.messageBox = messageBoxes.longMessageBox(title, str(err))
            self.messageBox.show()
            return
        self.maxFilterDialog.show()

        
    def on_pushButtonSpectrum_clicked(self):
        """
        Open the magnitude spectrum visualization dialog.
        """
        self.spectrumDialog = SpectrumDialog(self)
        self.spectrumDialog.show()
    
        
    def on_pushButtonEOG_clicked(self, checked=None):
        """
        Open the dialog for calculating the EOG PCA.
        """
        if checked is None: return 
        self.eogDialog = EogParametersDialog(self)
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
            self.messageBox = messageBoxes.shortMessageBox()
            self.messageBox.show()
            return
        
        epochs_collection_name = str(self.epochList.ui.listWidgetEpochs.\
                                     currentItem().text())
        epochs = self.experiment.active_subject._epochs[epochs_collection_name]
        epochs_raw = epochs._raw
        self.tfr_dialog = TFRDialog(self, self.experiment.active_subject.\
                                    _working_file, epochs_raw)
        self.tfr_dialog.show()
    
    
    def on_pushButtonTFRTopology_clicked(self,checked=None):
        """
        Opens the dialog for plotting TFR topology.
        """
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must create epochs before TFR.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        epochs_collection_name = str(self.epochList.ui.listWidgetEpochs.\
                                     currentItem().text())
        epochs = self.experiment.active_subject._epochs[epochs_collection_name]
        epochs_raw = epochs._raw
        self.tfrTop_dialog = TFRTopologyDialog(self, 
                                               self.experiment.active_subject.\
                                               _working_file, 
                                               epochs._raw)
        self.tfrTop_dialog.show()
    
        
    def on_pushButtonChannelAverages_clicked(self, checked=None):
        """
        Shows the channels average graph.
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.currentItem() is None: 
            message = 'Please select an epoch collection to channel average.'
            self.messageBox = messageBoxes.shortMessageBox()
            self.messageBox.show()  
            return
        
        """
        TODO: get epochs from active_subject._epochs dictionary
        """
        epochs_name = str(self.epochList.ui.listWidgetEpochs.\
                          currentItem().text())
        epochs = self.experiment.active_subject._epochs[epochs_name]._raw
        if self.ui.radioButtonLobe.isChecked() == True:
            self.caller.average_channels(epochs, self.ui.comboBoxLobes.\
                                         currentText(), None)
        else:
            customChannels = self.ui.plainTextEditCustomChannelsToAverage.\
            plainText
            self.caller.average_channels(epochs, None, customChannels)
    
            
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
        subject_name = str(self.ui.listWidgetSubjects.currentItem().text())
        # Not much point trying to activate an already active subject.
        if subject_name == self.experiment.active_subject_name:
            return      
        # This prevents taking the epoch list currentItem from the previously
        # open subject when activating another subject.
        self.clear_epoch_collection_parameters()
        self.experiment.activate_subject(subject_name)
        self._initialize_ui()


    def on_pushButtonBrowseRecon_clicked(self, checked=None):
        if checked is None : return
        
        activeSubject = self._experiment._active_subject
        
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
        
        activeSubject = self.experiment._active_subject
          
        if fileManager.copy_recon_files(activeSubject, path) == True:
            self.ui.lineEditRecon.setText(path)
            
            # Scourging of the source analysis files here - actually, is this
            # necessary?
            # fileManager.remove_sourceAnalysis_files(activeSubject)
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
            Removes selected forward model from the forward model list.
            """
            # TODO: do this after the mvc system works.
            return


    def on_pushButtonBrowseCoregistration_clicked(self, checked=None):
        if checked is None: return
        
        subjectPath = self._experiment._active_subject._subject_path
        targetName = os.path.join(subjectPath, 'reconFiles-trans.fif')
        
        path = QtGui.QFileDialog.getOpenFileName(
               self, 'Select the existing coordinate file ' +
               '(the file should end with "-trans.fif")' )
        if path == '':
            return
        else: 
            try:
                fileManager.copy(path, targetName)
            except IOError:
                message = 'There was a problem while copying the coordinate file.'
                messageBox = messageBoxes.shortMessageBox(message)
                messageBox.exec_()
                
    
    def on_pushButtonMNECoregistration_clicked(self, checked=None):
        if checked is None: return
        
        
        if self.ui.tableViewFModelsForCoregistration.selectedIndexes() == []:
            message = 'Please select a forward model to coregister.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        self.caller.coregister_with_mne_gui_coregistration()
        
        
    def on_pushButtonMNE_AnalyzeCoregistration_clicked(self, checked=None):
        if checked is None: return
        # TODO: Implement this last if needed.
        return



### Code for populating and updating various lists and tables in the MainWindow ###       
    
    def add_new_fModel_to_MVCModel(self, mparamdict):
        fmlist = self.forwardModelModel.fmodel_dict_to_list(mparamdict)
        self.forwardModelModel.add_fmodel(fmlist)



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
        self.ui.listWidgetSubjects.clear()
        
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
        self.ui.pushButtonConvertToMNE.setEnabled(False)
        self.ui.pushButtonCheckTalairach.setEnabled(False)
        self.ui.pushButtonSkullStrip.setEnabled(False)
        self.ui.pushButtonCheckSurfaces.setEnabled(False)
        self.ui.pushButtonCheckSegmentations.setEnabled(False)
        self.ui.pushButtonCreateNewForwardModel.setEnabled(False)
        
        # If experiment has subjects added, the active_subject info will be added
        # and tabs enabled for processing.
        if (len(self.experiment._subject_paths) > 0):
            for path in self.experiment._subject_paths:
                item = QtGui.QListWidgetItem()
                # -1 is the index for the subject name
                itemSubjectName = path.split('/')[-1]
                item.setText(itemSubjectName)
                # Let's bold the name of the active subject in the subject list.
                if itemSubjectName == self.experiment.active_subject_name:
                    itemFont = QFont('defaultFamily')
                    itemFont.setBold(True)
                    item.setFont(itemFont)
                self.ui.listWidgetSubjects.addItem(item)
        
        if self.experiment.active_subject is not None:
            #item = QtGui.QListWidgetItem(self.experiment._active_subject_name)
            self.ui.listWidgetSubjects.addItem(item)
            epochs_items = self.experiment.load_epochs(self.experiment.active_subject)
            evokeds_items = self.experiment.load_evokeds(self.experiment.active_subject)
            if epochs_items is not None:
                for item in epochs_items:
                    self.epochList.addItem(item)
                    self.epochList.setCurrentItem(item)
            if evokeds_items is not None:
                for item in evokeds_items:
                    self.evokedList.addItem(item)
                    self.evokedList.setCurrentItem(item)
            InfoDialog(self.experiment.active_subject.working_file,
                        self.ui, False)
            if self.experiment.active_subject._event_set is not None:
                self.populate_raw_tab_event_list()
            
            
        self.setWindowTitle('Meggie - ' + self.experiment.experiment_name)
        if self.experiment.active_subject is None:
            self.statusLabel.setText("Add or activate" + \
                                     " subjects before " + \
                                     "continuing.")
            return
        else:
            status = "Current working file: " + \
            os.path.basename(self._experiment._working_file_names[self.experiment._active_subject_name])
            self.statusLabel.setText(status)
            try:
                #Check whether ECG projections are calculated
                if self.experiment.active_subject.check_ecg_projs():
                    self.ui.pushButtonApplyECG.setEnabled(True)
                    self.ui.checkBoxECGComputed.setChecked(True)
                #Check whether EOG projections are calculated
                if self.experiment.active_subject.check_eog_projs():
                    self.ui.pushButtonApplyEOG.setEnabled(True)
                    self.ui.checkBoxEOGComputed.setChecked(True)
                #Check whether ECG projections are applied    
                if self.experiment.active_subject.check_ecg_applied():
                    self.ui.checkBoxECGApplied.setChecked(True)
                #Check whether EOG projections are applied
                if self.experiment.active_subject.check_eog_applied():
                    self.ui.checkBoxEOGApplied.setChecked(True)
                #Check whether sss/tsss method is applied.
                if self.experiment.active_subject.check_sss_applied():
                    self.ui.checkBoxMaxFilterComputed.setChecked(True)
                    self.ui.checkBoxMaxFilterApplied.setChecked(True)
            except AttributeError:
                print 'No active subject in experiment.'
                
        # Check whether reconstructed mri files have been copied to the recon
        # files directory under the subject and set up the UI accordingly.
        if self._experiment._active_subject.check_reconFiles_copied():
            self.ui.lineEditRecon.setText('Reconstructed mri image already ' + 
                                          'copied.')
            self.ui.pushButtonConvertToMNE.setEnabled(True)
            self.ui.pushButtonCheckTalairach.setEnabled(True)
            self.ui.pushButtonSkullStrip.setEnabled(True)
            self.ui.pushButtonCheckSurfaces.setEnabled(True)
            self.ui.pushButtonCheckSegmentations.setEnabled(True)
        
        # Check if MRI image has been setup with mne_setup_forward solution
        if self._experiment._active_subject.check_mne_setup_mri_run():
            self.ui.checkBoxConvertedToMNE.setChecked(True)
            self.ui.pushButtonCreateNewForwardModel.setEnabled(True)
            
        
    def populate_raw_tab_event_list(self):
        """
        Fill the raw tab event list with info about event IDs and
        amount of events with those IDs.
        """
        #TODO: trigger ---> event, also in the UI
        events = self.experiment.active_subject._event_set
        
        
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
        
        
    def enable_tabs(self):
        """
        Method for enabling the tabs.
        """
        self.ui.tabWidget.setTabEnabled(0,True)
        self.ui.tabWidget.setTabEnabled(1,True)
        self.ui.tabWidget.setTabEnabled(2,True)
        self.ui.tabWidget.setTabEnabled(3,True)
        self.ui.tabWidget.setTabEnabled(4,True)
        self.ui.tabWidget.setTabEnabled(5,True)
        self.ui.tabWidget.setTabEnabled(6,True)
        self.ui.tabWidget.setTabEnabled(7,True)
        self.ui.tabWidget.setTabEnabled(8,True)


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



### Miscellaneous code ###
        
    def check_workspace(self):
        """
        Open the workspace chooser dialog.
        """
        self.preferencesDialog = PreferencesDialog(self)
        self.preferencesDialog.exec_()

        
    def hide_workspace_option(self):
        self.ui.actionSet_workspace.setVisible(False)
        
        
        
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=MainWindow()
            
    window.show()
    
    sys.exit(app.exec_())

    