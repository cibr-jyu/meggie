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
import glob
 
from PyQt4 import QtCore,QtGui

import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib
 
from mainWindow_Ui import Ui_MainWindow
from createExperimentDialog_main import CreateExperimentDialog
from infoDialog_main import InfoDialog
from eventSelectionDialog_main import EventSelectionDialog
from eventSelectionDialog_Ui import Ui_EventSelectionDialog
from maxFilterDialog_main import MaxFilterDialog
from eogParametersDialog_main import EogParametersDialog
from ecgParametersDialog_main import EcgParametersDialog
from workSpaceDialog_main import WorkSpaceDialog
from preferencesDialog_main import PreferencesDialog
from addECGProjections_main import AddECGProjections
from addEOGProjections_main import AddEOGProjections
from TFRDialog_main import TFRDialog
from TFRTopologyDialog_main import TFRTopologyDialog
from spectrumDialog_main import SpectrumDialog
from widgets.epochWidget_main import EpochWidget
from about_main import AboutDialog
import messageBox

from experiment import Experiment
from epochs import Epochs
from events import Events
from caller import Caller

class MainWindow(QtGui.QMainWindow):
    """
    Class containing the logic for the MainWindow
    """

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Main window represents one experiment at a time. This experiment is
        # defined by the CreateExperimentDialog or the by the Open_experiment_
        # triggered action.
        self.experiment = None
        
        # One main window (and one experiment) only needs one caller to do its
        # bidding. 
        self.caller = Caller(self)
       
        # No tabs in the tabWidget initially
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)
        
        # Creates a listwidget for epoch analysis.  
        self.widget = EpochWidget(self)
        self.widget.hide()
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)
        
    def on_actionCreate_experiment_triggered(self, checked=None):
        """
        Creates a new CreateExperimentDialog and shows it
        """
        if checked is None: return # Standard workaround for file dialog opening twice
        if os.path.isfile('settings.cfg'):
            self.dialog = CreateExperimentDialog(self)
            self.dialog.show()
        else:
            self.check_workspace()   
        
    def on_actionOpen_experiment_triggered(self, checked=None):
        """
        Method for opening an existing experiment.
        TODO: should be moved to a separate I/O module
        """
        # Standard workaround for file dialog opening twice
        if checked is None: return 
                
        path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select experiment directory"))
        if path == '': return
        fname = path + '/' + path.split('/')[-1] + '.pro'
        # TODO needs exception checking for corrupt/wrong type of file
        # TODO the file should end with .exp
        if os.path.exists(path) and os.path.isfile(fname):
            output = open(fname, 'rb')
            self.experiment = pickle.load(output)

            # Reads the raw data info and sets it to the labels of the Raw tab
            InfoDialog(self.experiment.raw_data, self.ui, False)
            
            
            # Sets info about trigger channels and their events to
            # Triggers box in the Raw tab
            self.ui.listWidget.clear()
            events = self.experiment.event_set
            for key, value in events.iteritems():
                item = QtGui.QListWidgetItem()
                item.setText('Trigger ' + str(key) + ', ' + str(value) +
                            ' events')
                self.ui.listWidget.addItem(item)
            self.ui.labelExperimentName.setText(self.experiment.\
                                                experiment_name)
            self.ui.labelAuthorName.setText(self.experiment.author)
            self.ui.textBrowserExperimentDescription.setText(self.experiment\
                                                             .description)
            self.add_tabs()
            self._initialize_ui()
            
            # Sets the experiment for caller, so it can use its information.
            self.caller.experiment = self.experiment
            self.ui.statusbar.showMessage("Current working file: " +
                                          self.experiment.working_file.\
                                          info.get('filename'))
            
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Experiment file not found. Please check your directory.')
            self.messageBox.show()  
    
    def on_actionSet_workspace_triggered(self, checked=None):
        """
        Opens the dialog to set the workspace.
        """
        if checked is None: return
        self.check_workspace()
        
    def on_actionPreferences_triggered(self, checked=None):
        if checked is None: return
        self.dialogPreferences = PreferencesDialog()
        self.dialogPreferences.show()
        
    def on_pushButtonEventlist_clicked(self, checked=None):
        """
        Opens the epoch dialog. 
        """
        if checked is None: return
        self.epochParameterDialog = EventSelectionDialog(self)
        self.epochParameterDialog.show()
        
    def on_actionAbout_triggered(self, checked=None):
        """
        Opens the About-dialog 
        """
        if checked is None: return
        self.dialogAbout = AboutDialog()
        self.dialogAbout.show()    
        
    def on_pushButtonAverage_clicked(self, checked=None):
        """
        Method for plotting the evoked data as a topology.
        """
        if checked is None: return
        # If no events are selected, show a message to to the user and return.
        if self.widget.ui.listWidgetEpochs.currentItem() is None: 
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Please select an event collection to average.')
            self.messageBox.show()  
            return
         
        # Average the selected epochs
        epoch = self.widget.ui.listWidgetEpochs.currentItem().\
        data(32).toPyObject()
        evoked = epoch.average()
         
    def on_pushButtonMNE_Browse_Raw_clicked(self, checked=None):
        """
        Method for calling the mne_browse_raw.
        """
        if checked is None: return
        try:
            self.caller.call_mne_browse_raw(self.experiment.working_file.\
                                            info.get('filename'))
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            return        
    
    def on_pushButtonMaxFilter_clicked(self, checked=None):
        """
        Method for calling Elekta's MaxFilter.
        """
        if checked is None: return 
        try:
            self.maxFilterDialog = MaxFilterDialog(self, 
                                                   self.experiment.raw_data)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            return
        self.maxFilterDialog.show()
        
    def on_pushButtonSpectrum_clicked(self):
        """
        Opens the magnitude spectrum visualization dialog.
        """
        self.spectrumDialog = SpectrumDialog(self)
        self.spectrumDialog.show()
    
    def on_currentChanged(self):
        """
        Keeps track of the active tab.
        Shows the epoch collection list widget when in appropriate tabs.
        """
        index = self.ui.tabWidget.currentIndex()
        #self.tab = self.ui.tabWidget.currentWidget()
        
        
        if index == 2:
            self.widget.setParent(self.ui.tabEpoching)
            self.widget.show()
            return
        
        if index == 3:
            self.widget.setParent(self.ui.tabAveraging) 
            self.widget.show()
            return
       
        if index == 4:
            self.widget.setParent(self.ui.tabTFR) 
            self.widget.show()
            return 
            
        else:
            self.widget.hide()
        
    def on_pushButtonEOG_clicked(self, checked=None):
        """
        Opens the dialog for calculating the EOG PCA.
        """
        if checked is None: return 
        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.show()
        
    def on_pushButtonECG_clicked(self, checked=None):
        """
        Opens the dialog for calculating the ECG PCA.
        """
        if checked is None: return
        self.ecgDialog = EcgParametersDialog(self)
        self.ecgDialog.show()
        
    def on_pushButtonApplyEOG_clicked(self, checked=None):
        """
        Opens the dialog for applying the EOG-projections to the data.
        """
        if checked is None: return
        self.addEogProjs = AddEOGProjections(self)
        self.addEogProjs.exec_()
        
    def on_pushButtonApplyECG_clicked(self, checked=None):
        """
        Opens the dialog for applying the ECG-projections to the data.
        """
        if checked is None: return
        self.addEcgProjs = AddECGProjections(self)
        self.addEcgProjs.exec_()
        
    def on_pushButtonTFR_clicked(self, checked=None):
        """
        Opens the dialog for plotting TFR from a single channel.
        """
        if checked is None: return
        if self.widget.ui.listWidgetEpochs.currentItem() is None:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('You must create epochs ' +
                                                   'before TFR.')
            self.messageBox.show()
            return
        epoch = self.widget.ui.listWidgetEpochs.currentItem().\
        data(32).toPyObject()
        self.tfr_dialog = TFRDialog(self, self.experiment.working_file, epoch)
        self.tfr_dialog.show()
    
    def on_pushButtonTFRTopology_clicked(self,checked=None):
        """
        Opens the dialog for plotting TFR topology.
        """
        if self.widget.ui.listWidgetEpochs.currentItem() is None:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('You must create epochs ' +
                                                   'before TFR.')
            self.messageBox.show()
            return
        epoch = self.widget.ui.listWidgetEpochs.currentItem().\
        data(32).toPyObject()
        self.tfrTop_dialog = TFRTopologyDialog(self, 
                                               self.experiment.working_file, 
                                               epoch)
        self.tfrTop_dialog.show()
    
    def _initialize_ui(self):
        """
        Method for setting up the GUI.
        """        
        self.ui.labelMaxFilterAccept_2.hide()
        self.ui.labelECGComputedAccept_2.hide()
        self.ui.labelEOGComputedAccept_2.hide()
        self.ui.labelECGAppliedAccept_2.hide()
        self.ui.labelEOGAppliedAccept_2.hide()
        self.ui.pushButtonApplyEOG.setEnabled(False)
        self.ui.pushButtonApplyECG.setEnabled(False)
        
        #Check whether ECG projections are calculated
        fname = self.experiment.raw_data.info.get('filename')
        path = self.experiment._subject_directory
        files =  filter(os.path.isfile, glob.glob(path+'*_ecg_avg_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_ecg_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_ecg-eve.fif'))
        if len(files) > 1:
            self.ui.pushButtonApplyECG.setEnabled(True)
            self.ui.labelECGComputedAccept_2.show()
        
        #Check whether EOG projections are calculated
        files =  filter(os.path.isfile, glob.glob(path+'*_eog_avg_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_eog_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_eog-eve.fif'))
        if len(files) > 1:
            self.ui.pushButtonApplyEOG.setEnabled(True)
            self.ui.labelEOGComputedAccept_2.show()
        
        #Check whether ECG projections are applied
        files = filter(os.path.isfile, glob.glob(path + '*ecg_applied*'))
        if len(files) > 0:
            self.ui.labelECGAppliedAccept_2.show()
        
        #Check whether EOG projections are applied
        files = filter(os.path.isfile, glob.glob(path + '*eog_applied*'))
        if len(files) > 0:
            self.ui.labelEOGAppliedAccept_2.show()
        
        files = filter(os.path.isfile, glob.glob(path + '*sss*'))
        if len(files) > 0:
            self.ui.labelMaxFilterAccept_2.show()
        
        #TODO: applied/not applied label for MaxFilter
        
    def add_tabs(self):
        """
        Method for initializing the tabs.
        """
        self.ui.tabWidget.insertTab(0, self.ui.tabRaw, "Raw")
        self.ui.tabWidget.insertTab(1, self.ui.tabPreprocessing, 
                                    "Preprocessing")

        self.ui.tabWidget.insertTab(2, self.ui.tabEpoching, "Epoching")
        self.ui.tabWidget.insertTab(3, self.ui.tabAveraging, "Averaging")
        self.ui.tabWidget.insertTab(4, self.ui.tabTFR, "TFR")
        
    def check_workspace(self):
        """
        Open the workspace chooser dialog.
        """
        self.workSpaceDialog = WorkSpaceDialog(self)
        self.workSpaceDialog.show()
        
    def hide_workspace_option(self):
        self.ui.actionSet_workspace.setVisible(False)

def main(): 
    app = QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    
    sys.exit(app.exec_())
