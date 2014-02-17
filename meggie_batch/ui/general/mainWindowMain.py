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
import pickle
import subprocess
from sets import Set

import shutil
 
from PyQt4 import QtCore,QtGui

import mne
from mne import fiff
from mne.datasets import sample
from mne.layouts.layout import _pair_grad_sensors_from_ch_names

from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt4Agg')
import pylab as pl
 
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
from workSpaceDialogMain import WorkSpaceDialog
from preferencesDialogMain import PreferencesDialog
from evokedStatsDialogMain import EvokedStatsDialog
from addECGProjectionsMain import AddECGProjections
from addEOGProjectionsMain import AddEOGProjections
from TFRDialogMain import TFRDialog
from TFRTopologyDialogMain import TFRTopologyDialog
from spectrumDialogMain import SpectrumDialog
from widgets.epochWidgetMain import EpochWidget
from widgets.epochParamsWidgetMain import EpochParamsWidget
from aboutDialogMain import AboutDialog
from filterDialogMain import FilterDialog
from consoleMain import Console
import messageBox

from experiment import Experiment
from epochs import Epochs
from events import Events
from caller import Caller
from fileManager import FileManager
from listWidget import ListWidget


class MainWindow(QtGui.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """
    
    #custom signals
    experiment_value_changed = QtCore.pyqtSignal()

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
        
        # Creates a listwidget for parameters of chosen epochs on epochList.
        """
        self.epochParamsList = EpochParamsWidget(self)
        self.epochParamsList.hide()
        """
        
        self.fileManager = FileManager()
        self.epocher = Epochs()
        
        #Populate the combobox for selecting lobes for channel averages.
        self.populate_comboBoxLobes()
        
        #Connect signals and slots
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)
        self.experiment_value_changed.connect\
        (self.open_active_subject)
        self.experiment_value_changed.connect\
        (self.load_epoch_collections)
        self.experiment_value_changed.connect\
        (self.load_evoked_collections)
        self.epochList.item_added.connect(self.epochs_added)
        self.ui.pushButtonMNE_Browse_Raw_2.clicked.connect(self.on_pushButtonMNE_Browse_Raw_clicked)
                        
        # For output logging.
        self.console = Console()
        
        
    #Property definitions below
    @property
    def experiment(self):
        return self._experiment
    
    @experiment.setter
    def experiment(self, experiment):
        self._experiment = experiment
        self.experiment_value_changed.emit()
        
    def on_actionQuit_triggered(self, checked=None):
        """
        Closes the program.
        """
        if checked is None: return
        reply = QtGui.QMessageBox.question(self, 'Close Meggie',
                                           'Are you sure you want to quit' + \
                                           ' Meggie?', QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            self.close()
        
    def on_actionCreate_experiment_triggered(self, checked=None):
        """
        Create a new CreateExperimentDialog and show it
        """
        if checked is None: return # Standard workaround for file dialog opening twice
        if os.path.isfile('settings.cfg'):
            self.dialog = CreateExperimentDialog(self)
            self.dialog.show()
        else:
            self.check_workspace()
            if os.path.isfile('settings.cfg'):
                self.dialog = CreateExperimentDialog(self)
                self.dialog.show()   
        
    def on_actionOpen_experiment_triggered(self, checked=None):
        """
        Open an existing _experiment.
        """
        #TODO: should be moved to a separate I/O module
        # Standard workaround for file dialog opening twice
        if checked is None: return 
                
        path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select _experiment directory"))
        if path == '': return
        
        fname = os.path.join(path, path.split('/')[-1] + '.pro')
        # TODO needs exception checking for corrupt/wrong type of file
        # TODO the file should end with .exp
        if os.path.exists(path) and os.path.isfile(fname):
            output = open(fname, 'rb')
            
            # This emits experiment_value_changed signal and invokes methods
            # load_active_subject, load_epoch_collections and
            # load_evoked_collections.
            self.experiment = pickle.load(output)
            self._initialize_ui()
            
            # TODO: needs to be added to _initialize_ui so that after
            # activating subject the updated experiment will be given
            # to the caller? 
            # Sets the experiment for caller, so it can use its information.
            self.caller.experiment = self.experiment
            
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Experiment file not found. Please check your directory.')
            self.messageBox.show()  
    
    def on_pushButtonAddSubjects_clicked(self, checked=None):
        """
        Open subject dialog.
        """
        if checked is None: return
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
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('No subject selected.')
            self.messageBox.show()
            return
            
        item_str = self.ui.listWidgetSubjects.currentItem().text()
            
        root = self.experiment.active_subject_path
        message = 'Permanently remove subject and the related files?'
            
        reply = QtGui.QMessageBox.question(self, 'delete subject',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            self.experiment.remove_subject(self.ui.listWidgetSubjects.currentItem(), self)
            # TODO: listWidgetSubects.currentItem() should be removed here
    
    def on_actionShow_Hide_Console_triggered(self, checked=None):
        """
        Show / Hide console window.
        """
        if checked is None: return
        if self.console.isVisible():
            self.console.hide()
        else:
            self.console.show()
        
    
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
        
    def show_epoch_collection_parameters(self, item):
        """
        Sets parameters from the currently chosen epochs.
        
        Keyword arguments:
        item = epochWidget item that is currently chosen,
               includes .fif and .param files
        """
        
        # Set default/empty values for epoch parameters.
        self.clear_epoch_collection_parameters()
        
        params = item.data(33).toPyObject()
        if params is None: return
       
        epochs = item.data(32).toPyObject()
        
        # Dictionary stores numbers of different events.
        event_counts = dict()
        
        # Adds items to dictionary for corresponding events.
        for value in epochs.event_id.values():
            event_counts[str(value)] = 0
        
        # Adds number of events to corresponding event.
        for event in epochs.events:
            for key in event_counts.keys():
                if event[2] == int(key):
                    event_counts[key] += 1
        
        categories = ''
        # Adds event names, ids and event counts on mainWindows parameters
        # list.
        for key,value in epochs.event_id.items():
            item = QtGui.QListWidgetItem()
            item.setText(key + ': ID ' + str(value) + ', ' + \
            str(event_counts[str(value)]) + ' events')
            
            self.epochList.ui.listWidgetEvents.addItem(item)
            
        # TODO: create category items to add on the listWidgetEvents widget. 
        #self.epochList.ui.listWidgetEvents.setText(categories)
        
        self.ui.textBrowserTmin.setText(str(params[QtCore.QString('tmin')]) + ' s')
        self.ui.textBrowserTmax.setText(str(params[QtCore.QString('tmax')]) + ' s')

        # Creates dictionary of strings instead of qstrings for rejections.
        params_rejections_str = dict((str(key), value) for
                          key, value in params[QtCore.QString(u'reject')].\
                          iteritems())
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
        
        filename_full_path = str(params[QtCore.QString(u'raw')])
        filename_list = filename_full_path.split('/')
        filename = filename_list[len(filename_list) - 1]
        self.ui.textBrowserWorkingFile.setText(filename)
        #self.ui.textBrowserWorkingFile.setText(params[QtCore.QString(u'raw')])
        
        
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
        Open the dialog to set the workspace.
        """
        if checked is None: return
        self.check_workspace()
        
    def on_actionPreferences_triggered(self, checked=None):
        """Open the preferences-dialog.
        """
        if checked is None: return
        self.dialogPreferences = PreferencesDialog()
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
        Calls Subject to handle with new epochs.
        """
        if os.path.exists(self.experiment.active_subject._epochs_directory) is False:
            self.experiment.active_subject.create_epochs_directory
        fname = str(item.text())
        fpath = os.path.join(self.experiment.active_subject._epochs_directory, fname)
        self.fileManager.save_epoch_item(fpath, item)
        
        # Creates Epochs object and adds it to Subject epochs list.
        self.experiment.active_subject.handle_new_epochs(fname, item)
        
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
        epoch_params['raw'] = self.experiment.active_subject_raw_path
        #Create a QListWidgetItem and add the actual epochs to slot 32.
        item = QtGui.QListWidgetItem(epoch_params['collectionName'])
        item.setData(32, epochs)
        item.setData(33, epoch_params)
        self.epochList.addItem(item)
        self.epochList.setCurrentItem(item)
        
    @QtCore.pyqtSlot()
    def handle_new_experiment(self):
        """Clear the epoch list and load new epochs for the new experiment.
        """
        if self.experiment is None:
            return
        
        else:
            self.epochList.clearItems()
            self.load_epoch_collections()
            self.evokedList.clear()
            self.load_evoked_collections()
        
    def open_active_subject(self):
        """
        Opens the active subject of the experiment.
        """
        if self.experiment.active_subject_path != '':
            if len(self.experiment._subject_paths) > 0:
                    raw_path = self.experiment.active_subject_raw_path
                    subject_name = self.experiment.active_subject_name
                    self.experiment.activate_subject(self, raw_path, subject_name,
                                                     self.experiment)
        
    def load_epoch_collections(self):
        """Load epoch collections from a folder.
        
        Load the epoch collections from workspace/experiment/epochs/ 
        and show them on the epoch collection list.
        """
        if len(self.experiment._subject_paths) == 0:
            return
        if self.experiment.active_subject_path == '':
            return
        # Get epochs as QListWidgetItems from subject object.
        # This is used when epochs are already created from earlier
        # activation of the subject.
        if len(self.experiment.active_subject._epochs) > 0:
            epoch_items = self.experiment.active_subject.\
            convert_epoch_collections_as_items()
            self.epochList.clearItems()
            
            # TODO: Every time when adding item calls load_evoked_collections
            # method. Fix by creating Evoked class for handling those objects.
            # Check if Evoked objects are already created.
            for item in epoch_items:
                self.epochList.addItem(item)
                self.epochList.setCurrentItem(item)
            return
        if os.path.exists(self.experiment.\
                          active_subject._epochs_directory) is False:
            self.experiment.active_subject.create_epochs_directory
            return
        self.epochList.clearItems()
        path = self.experiment.active_subject._epochs_directory
        files = os.listdir(path)
        
        # TODO: Every time when adding item calls load_evoked_collections
        # method. Fix by creating Evoked class for handling those objects.
        # Check if Evoked objects are already created.
        for file in files:
            if file.endswith('.fif'):
                name = file[:-4]
                item = self.fileManager.load_epoch_item(path, name)
                self.epochList.addItem(item)
                self.epochList.setCurrentItem(item)
       
    @QtCore.pyqtSlot(dict)
    def modifyEpochs(self, epoch_params):
        """Overwrite the existing epoch_item with new epochs.
        
        Keyword arguments:
        epoch_params -- A dict containing the parametervalues for the epochs.
        """
        
        epochs = self.epocher.create_epochs_from_dict(epoch_params,
                                                      self.experiment.\
                                                      active_subject.\
                                                      working_file)
        epoch_params['raw'] = self.experiment.active_subject_raw_path #working_file_path
        #Create a QListWidgetItem and add the actual epochs to slot 32.
        item = QtGui.QListWidgetItem(epoch_params['collectionName'])
        item.setData(32, epochs)
        item.setData(33, epoch_params)
        if self.delete_epochs(self.epochList.currentItem()):
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
        item = self.fileManager.load_epochs(fname)
        if item is None: return
        self.epochList.addItem(item)
                
    def on_pushButtonModifyEpochs_clicked(self, checked = None):
        """Modify currently selected epochs.
        """
        if checked is None: return
        if self.epochList.currentItem() is None: return
        params = self.epochList.currentItem().data(33).toPyObject()
        self.epochParameterDialog = EventSelectionDialog(self, self.\
                                                         experiment.\
                                                         active_subject.working_file,
                                                         params)
        self.epochParameterDialog.epoch_params_ready.\
        connect(self.modifyEpochs)
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
            epochs = self.epochList.currentItem().data(32).toPyObject()
            epochs.save(fname)
        #Also copy the related csv-file to the chosen folder
        self.fileManager.copy(os.path.join(self.experiment.active_subject.\
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
        
    def on_pushButtonCreateEvoked_clicked(self, checked=None):
        """
        Create averaged epoch collection (evoked dataset).
        Plot the evoked data as a topology.
        """
        if checked is None: return
        # If no events are selected, show a message to to the user and return.
        if self.epochList.ui.listWidgetEpochs.currentItem() is None: 
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Please select an epoch collection to average.')
            self.messageBox.show()  
            return
        epochs = self.epochList.ui.listWidgetEpochs.currentItem().data(32).\
        toPyObject()
        category = epochs.event_id
        
        # New dictionary for event categories must be created, if user
        # manually chooses different event categories to be averaged. 
        if len(self.epochList.ui.listWidgetEvents.selectedItems()):
            category_user_chosen = dict()
            for event in self.epochList.ui.listWidgetEvents.selectedItems():
                event_name = (str(event.text())).split(':')
                category_user_chosen[event_name[0]] = epochs.event_id.get(event_name[0])
            evoked = self.caller.average(epochs,category_user_chosen)
            category = category_user_chosen
        else:
            #category = epochs.event_id
            evoked = self.caller.average(epochs,category)
        
        category_str = ''
        i = 0
        for key in category.keys():
            if i == 0:
                category_str += key
                i = 1
            else:
                category_str += '-' + key
        item = QtGui.QListWidgetItem()
        epoch_collection = self.epochList.ui.listWidgetEpochs.currentItem()
        item.setText(epoch_collection.text() + '[' + category_str + ']' + '_evoked.fif')
        item.setData(32, evoked)
        item.setData(33, category)
        
        self.evokedList.addItem(item)
        #self.evokedList.setCurrentItem(item)
        
        #evoked = self.caller.average(epochs,category)
        
    def on_pushButtonOpenEvokedStatsDialog_clicked(self, checked = None):
        """Open the evokedStatsDialog for viewing statistical data.
        """
        #Currently a mock code.
        #TODO: Pass evokeds in a dictionary
        if checked is None: return
        if self.evokedList.count() == 0: return
        
        evoked_dict = {}
        for i in range(self.evokedList.count()):
            evoked_dict[str(self.evokedList.item(i).text())] = \
            self.evokedList.item(i).data(32).toPyObject()
            
        self.evokedStatsDialog = EvokedStatsDialog(evoked_dict)
        self.evokedStatsDialog.exec_()
        
    def on_pushButtonVisualizeEpochChannels_clicked(self, checked = None):
        """Plot image over epochs channel
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.count() == 0:
            # TODO: show messagebox
            print 'Create epochs before visualizing.'
            return
        epochs = self.epochList.ui.listWidgetEpochs.currentItem().data(32).\
        toPyObject()
        
        self.visualizeEpochChannelsDialog = VisualizeEpochChannelDialog(epochs)
        self.visualizeEpochChannelsDialog.exec_()
        
    
    def on_pushButtonVisualizeEvokedDataset_clicked(self, checked=None):
        """
        Plot the evoked data as a topology
        """
        if checked is None: return
        item = self.evokedList.currentItem()
        if item is None: return
        evoked = item.data(32).toPyObject()
        category = item.data(33).toPyObject()
        self.caller.draw_evoked_potentials(evoked,category)
        
    def on_pushButtonSaveEvoked_clicked(self, checked=None):
        """
        Save the evoked data
        """
        if checked is None: return
        item = self.evokedList.currentItem()
        evokeds = item.data(32).toPyObject()
        
        
        evoked_collection_name = str(item.text())
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
        Load evoked data
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
        
        item = self.fileManager.load_evokeds(fname + '.fif')
        if item is None: return
        self.evokedList.addItem(item)
        
        
    def load_evoked_collections(self):
        """Load evoked collections from a folder.
        
        Load the evoked collections from workspace/experiment/epochs/average/
        and show them on the evoked collection list.
        """
        if len(self.experiment._subject_paths) == 0:
            return
        if self.experiment.active_subject_path == '':
            return
        if not os.path.exists(os.path.join(self.experiment.active_subject.\
                                           _epochs_directory, 'average')):
            self.evokedList.clear()
            return  
        self.evokedList.clear()
        #self.epochList.clearItems()
        path = os.path.join(self.experiment.active_subject._epochs_directory, 'average')
        files = os.listdir(path)
        for file in files:
            if file.endswith('.fif'):
                #name = file[:-4]            
                # TODO: Add load_evoked_item method on fileManager to read
                # evoked datasets and create QListWidgetItem object in the
                # same method. Connect loadk_evoked_item to
                # experiment_value_changed signal on mainWindow __init__
                # (constructor: self.experiment_value_changed.connect\
                # (self.load_evoked_collections)).
                item = self.fileManager.load_evoked_item(path, file)
                if item is None:
                    print 'One or more evoked.fif data files has more than' + \
                    ' 8 datasets and the loading of this/these data file/s' + \
                    ' was terminated.'
                else:
                    self.evokedList.addItem(item)
                    self.evokedList.setCurrentItem(item)
                #self.evokedList.addItem(item)
                #self.evokedList.setCurrentItem(item)
        
    def on_pushButtonDeleteEpochs_clicked(self, checked=None):
        """Delete the selected epoch item and the files related to it.
        """
        if checked is None:
            return
        
        if self.epochList.isEmpty():
            return
        
        elif self.epochList.currentItem() is None:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('No epochs selected.')
            self.messageBox.show()
            
        item_str = self.epochList.currentItem().text()
            
        root = self.experiment.active_subject._epochs_directory
        message = 'Permanently remove epochs and the related files?'
            
        reply = QtGui.QMessageBox.question(self, 'delete epochs',
                                           message, QtGui.QMessageBox.Yes |
                                           QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No)
            
        if reply == QtGui.QMessageBox.Yes:
            #self.delete_epochs(self.epochList.currentItem())
            self.experiment.active_subject.remove_epochs(item_str)
            self.epochList.remove_item(self.epochList.currentItem())
            
    def on_pushButtonDeleteEvoked_clicked(self, checked=None):
        """Delete the selected evoked item and the files related to it.
        """
                
        if checked is None:
            return
        
        if self.evokedList.count() == 0:
            return
        
        elif self.evokedList.currentItem() is None:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('No evokeds selected.')
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
            self.fileManager.delete_file_at(root, item_str)
            
            # TODO: What to do if can't delete the .fif file.
            """
            if self.fileManager.delete_file_at(root, item_str):
                return
            else:
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText('Unable to delete the'\
                                                        + ' file.')
                self.messageBox.show()
                return
            """
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
            self.messageBox = messageBox.AppForm()
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
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            return
        self.maxFilterDialog.show()
        
    def on_pushButtonSpectrum_clicked(self):
        """
        Open the magnitude spectrum visualization dialog.
        """
        self.spectrumDialog = SpectrumDialog(self)
        self.spectrumDialog.show()
    
    def on_currentChanged(self):
        """
        Keep track of the active tab.
        Show the epoch collection list epochList when in appropriate tabs.
        """
        index = self.ui.tabWidget.currentIndex()
        #self.tab = self.ui.tabWidget.currentWidget()
        
        
        if index == 3:
            self.epochList.setParent(self.ui.groupBoxEpochsEpoching)
            #self.epochParamsList.setParent(self.ui.groupBoxEpochParamsEpoching)
            self.epochList.show()
            #self.epochParamsList.show()
            return
        
        if index == 4:
            self.epochList.setParent(self.ui.groupBoxEpochsAveraging)
            #self.epochParamsList.setParent(self.ui.groupBoxEpochParamsAveraging)
            self.epochList.show()
            #self.epochParamsList.show()
            return
       
        if index == 5:
            self.epochList.setParent(self.ui.groupBoxEpochsTFR)
            #self.epochParamsList.setParent(self.ui.groupBoxEpochParamsTFR)
            self.epochList.show()
            #self.epochParamsList.show()
            return 
            
        else:
            self.epochList.hide()
            #self.epochParamsList.hide()
        
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
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('You must create epochs ' +
                                                   'before TFR.')
            self.messageBox.show()
            return
        epoch = self.epochList.ui.listWidgetEpochs.currentItem().\
        data(32).toPyObject()
        self.tfr_dialog = TFRDialog(self, self.experiment.active_subject._working_file, epoch)
        self.tfr_dialog.show()
    
    def on_pushButtonTFRTopology_clicked(self,checked=None):
        """
        Opens the dialog for plotting TFR topology.
        """
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('You must create epochs ' +
                                                   'before TFR.')
            self.messageBox.show()
            return
        epoch = self.epochList.ui.listWidgetEpochs.currentItem().\
        data(32).toPyObject()
        self.tfrTop_dialog = TFRTopologyDialog(self, 
                                               self.experiment.active_subject._working_file, 
                                               epoch)
        self.tfrTop_dialog.show()
        
    def on_pushButtonChannelAverages_clicked(self, checked=None):
        """
        Shows the channels average graph.
        """
        if checked is None: return
        if self.epochList.ui.listWidgetEpochs.currentItem() is None: 
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Please select an epoch collection to channel average.')
            self.messageBox.show()  
            return
        epochs = self.epochList.ui.listWidgetEpochs.currentItem().data(32).\
        toPyObject()
        
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
        working_file_name = ''
        subject_to_be_activated = str(self.ui.listWidgetSubjects.currentItem().
                                      text())
        working_file_name = self.experiment.\
        _working_file_names[subject_to_be_activated]
        if len(working_file_name) == 0:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('There is no working file in the chosen subject folder.')
            self.messageBox.show()  
            return
        raw_path = working_file_name
        subject_name = self.ui.listWidgetSubjects.currentItem().text()
        self.experiment.activate_subject(self, str(raw_path), str(subject_name), self.experiment)
        self.experiment.update_experiment_settings()
        self._initialize_ui()
    
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
    
    
    def _initialize_ui(self):
        """
        Method for setting up the GUI.
        """  
        # Clears the events data.
        self.ui.textBrowserEvents.clear()
        # Clears the data info of the labels.
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

        path = self.experiment.active_subject_path
        # To make sure that glob is not using path = '' as a root folder.
        if path == '' and len(self.experiment._subject_paths) > 0:
            a = 0 # just a useless code to prevent error for doing nothing..
        else:
            try:
                #Check whether ECG projections are calculated
                if self.experiment.active_subject.check_ecg_projs():
                    self.ui.pushButtonApplyECG.setEnabled(True)
                    self.ui.checkBoxECGComputed.setChecked(True)
                else:    
                    self.ui.pushButtonApplyECG.setEnabled(False)
                    self.ui.checkBoxECGComputed.setChecked(False)
                #Check whether EOG projections are calculated
                if self.experiment.active_subject.check_eog_projs():
                    self.ui.pushButtonApplyEOG.setEnabled(True)
                    self.ui.checkBoxEOGComputed.setChecked(True)
                else:    
                    self.ui.pushButtonApplyEOG.setEnabled(False)
                    self.ui.checkBoxEOGComputed.setChecked(False)
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
                else:
                    self.ui.checkBoxMaxFilterComputed.setChecked(False)
                    self.ui.checkBoxMaxFilterApplied.setChecked(False)
            except AttributeError:
                print 'No active subject in experiment.'    
                
        # QLabel created on __init__ can't take normal string objects.
        if len(self.experiment._subjects) == 0 or self.experiment.active_subject_path == '':
            self.statusLabel.setText(QtCore.QString("Add or activate" + \
                                                    " subjects before " + \
                                                    "continuing."))
        else:
            """
            self.statusLabel.setText(QtCore.QString("Current working file: " +
                                                    self.experiment.\
                                                    active_subject.working_file.\
                                                    info.get('filename')))
            """
            self.statusLabel.setText(QtCore.QString("Current working file: " +
                                                    self.experiment.\
                                                    active_subject_raw_path))
        self.setWindowTitle('Meggie - ' + self.experiment.experiment_name)
        self.ui.labelExperimentName.setText(self.experiment.\
                                            experiment_name)
        self.ui.labelAuthorName.setText(self.experiment.author)
        self.ui.textBrowserExperimentDescription.\
        setText(self.experiment.description)
        # Clear the list and add all subjects to it.
        self.ui.listWidgetSubjects.clear()
        # If experiment has subjects added the active_subject info will be added
        # and tabs enabled for processing.
        if (len(self.experiment._subject_paths) > 0):
            for path in self.experiment._subject_paths:
                item = QtGui.QListWidgetItem()
                # -1 is the index for the subject name
                item.setText(path.split('/')[-1])
                self.ui.listWidgetSubjects.addItem(item)
            # In case trying to open experiment that includes subjects but
            # there is no activated subject. Happens if you delete currently
            # active subject and try to open that experiment again.
            if self.experiment.active_subject_path != '':
                InfoDialog(self.experiment.active_subject.working_file,
                            self.ui, False)
                if self.experiment.active_subject._event_set != None:
                    self.populate_raw_tab_event_list()
                if self.ui.tabWidget.count() == 0:
                    self.add_tabs()
                self.enable_tabs()
            else:
                self.add_tabs()
        else:
            self.add_tabs()

    def add_tabs(self):
        """
        Method for initializing the tabs.
        """
        self.ui.tabWidget.insertTab(0, self.ui.tabRaw, "Experiment")
        self.ui.tabWidget.insertTab(1, self.ui.tabSubjects, "Subjects")
        self.ui.tabWidget.insertTab(2, self.ui.tabPreprocessing, 
                                    "Preprocessing")
        self.ui.tabWidget.insertTab(3, self.ui.tabEpoching, "Epoching")
        self.ui.tabWidget.insertTab(4, self.ui.tabAveraging, "Averaging")
        self.ui.tabWidget.insertTab(5, self.ui.tabTFR, "TFR")
        
        # If no subjects added to the experiment, there is no reason to enable
        # more tabs to confuse the user.
        if len(self.experiment._subject_paths) == 0 or \
        self.experiment.active_subject_path == '':
            self.ui.tabWidget.setTabEnabled(2,False)
            self.ui.tabWidget.setTabEnabled(3,False)
            self.ui.tabWidget.setTabEnabled(4,False)
            self.ui.tabWidget.setTabEnabled(5,False)
        
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
        
    def check_workspace(self):
        """
        Open the workspace chooser dialog.
        """
        self.workSpaceDialog = WorkSpaceDialog(self)
        self.workSpaceDialog.exec_()
        
    def hide_workspace_option(self):
        self.ui.actionSet_workspace.setVisible(False)
        
    def write(self, output):
        self.console.show_log(output)
        
        
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=MainWindow()
    
    # sys.stdout redirects the output to any object that implements
    # a write(str) method, in this case the write method of MainWindow.
    #sys.stdout=sys.stderr=window
    
    window.show()
    
    sys.exit(app.exec_())
