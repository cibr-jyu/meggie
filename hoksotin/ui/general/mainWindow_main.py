'''
Created on Mar 16, 2013

@author: jaeilepp
'''

import os,sys
import pickle
import subprocess
import glob
 
from PyQt4 import QtCore,QtGui

import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
 
from mainWindow_Ui import Ui_MainWindow
from createExperimentDialog_main import CreateExperimentDialog
from infoDialog_main import InfoDialog
from parameterDialog_main import ParameterDialog
from maxFilterDialog_main import MaxFilterDialog
from eogParametersDialog_main import EogParametersDialog
from ecgParametersDialog_main import EcgParametersDialog
from workSpaceDialog_main import WorkSpaceDialog
from preferencesDialog_main import PreferencesDialog
from addECGProjections_main import AddECGProjections
from addEOGProjections_main import AddEOGProjections
from TFRDialog_main import TFRDialog
from TFRTopologyDialog_main import TFRTopologyDialog
from widgets.epochWidget_main import EpochWidget
import messageBox

from experiment import Experiment
from epochs import Epochs
from events import Events
from caller import Caller

#from createEpochs import CreateEpochs
#from widgets.create_tab import Tab, EpochTab

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        
        """
        Main window represents one experiment at a time. This experiment is
        defined by the CreateExperimentDialog or the by the Open_experiment_
        trigger action.
        """
        self.experiment = None
        
        """
        One main window (and one experiment) only needs one caller to do its
        bidding. 
        """
        self.caller = Caller(self)
        
       
        # No tabs in the tabWidget initially
        while self.ui.tabWidget.count() > 0:
            self.ui.tabWidget.removeTab(0)
        
        """Creates a listwidget for epoch analysis."""    
             
        self.widget = EpochWidget(self)
        self.widget.setGeometry(QtCore.QRect(450, 140, 381, 231))
        self.widget.hide()
                
        #self.ui.horizontalLayout.addWidget(self.widget)
        '''
        Old code for activating buttons when experiment state changes
        TODO: check and remove
        #self.ui.pushButtonAverage.setEnabled(False)
        #self.ui.pushButtonVisualize.setEnabled(False)
        '''
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)
        
        
    def on_actionCreate_experiment_triggered(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        """
        Creates a new CreateExperimentDialog and shows it
        """       
        if os.path.isfile('settings.cfg'):
            self.dialog = CreateExperimentDialog(self)
            self.dialog.show()
            """
            Sets the experiment for caller, so it can use its information
            self.caller.experiment = self.experiment
            """
        else:
            self.check_workspace()
        
    def on_actionOpen_experiment_triggered(self, checked=None):
         # Standard workaround for file dialog opening twice
        if checked is None: return 
                
        path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select experiment directory"))
        if path == '': return
        fname = path + '/' + path.split('/')[-1] + '.pro'
        # TODO needs exception checking for corrupt/wrong type of file
        if os.path.exists(path) and os.path.isfile(fname):
            output = open(fname, 'rb')
            self.experiment = pickle.load(output)
            
            # workaround for setting up the raw object after pickling
            self.experiment.raw_data = mne.fiff.Raw(
                self.experiment.raw_data.info.get('filename'),
                 preload=True)

            # Reads the raw data info and sets it to the labels of the Raw tab
            InfoDialog(self.experiment.raw_data, self.ui, False)
            
            #self.ui.textBrowserExperimentDescription self.experiment.description
            
            """
            Sets info about trigger channels and their events to
            Triggers box in the Raw tab
            """
            self.ui.listWidget.clear()
            events = self.experiment.event_set
            for key, value in events.iteritems():
                item = QtGui.QListWidgetItem()
                item.setText('Trigger ' + str(key) + ', ' + str(value) +
                            ' events')
                self.ui.listWidget.addItem(item)
            self.ui.labelExperimentName.setText(self.experiment.experiment_name)
            self._initialize_ui()
            
            """
            Sets the experiment for caller, so it can use its information
            """
            self.caller.experiment = self.experiment
            self.ui.statusbar.showMessage("Current working file: " +
                                          self.experiment.working_file.info.get('filename'))
            
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Experiment file not found. Please check your directory.')
            self.messageBox.show()  
     
    #def setup_ui_by_experiment_state(self):
    
    def on_actionSet_workspace_triggered(self, checked=None):
        # Standard workaround for file dialog opening twice
        if checked is None: return
        self.check_workspace()
        
    def on_actionPreferences_triggered(self, checked=None):
        # Standard workaround for file dialog opening twice
        if checked is None: return
        self.dialogPreferences = PreferencesDialog()
        self.dialogPreferences.show()
        
    def on_pushButtonEventlist_clicked(self, checked=None):
        """
        Opens the epoch dialog. 
        """
        # Standard workaround for file dialog opening twice
        if checked is None: return
        self.epochParameterDialog = ParameterDialog(self)
        self.epochParameterDialog.show()        
        
    def on_pushButtonAverage_clicked(self, checked=None):
        # Standard workaround for file dialog opening twice
        if checked is None: return
        
        # If no events are selected, show a message to to the user and return
        if ( self.widget.ui.listWidgetEpochs.currentItem() == None ): 
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Please select an event collection to average.')
            self.messageBox.show()  
            return
         
        epoch = self.widget.ui.listWidgetEpochs.currentItem().data(32).toPyObject()
        evoked = epoch.average()
        
        #Check if the tab has already been created
        #if self.ui.tabEvoked == None:
        #    self.ui.tabEvoked = QtGui.QWidget()
        #    self.ui.listWidgetAverage = self.__create_tab(self.ui.tabEvoked,
        #                                                  'Evoked')
        #item = QtGui.QListWidgetItem()
        #item.setText('TestElement')
        #item.setData(1,evoked)
        #self.ui.listWidgetAverage.addItem(item)
        evoked.plot()
         
    def on_pushButtonMNE_Browse_Raw_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.caller.call_mne_browse_raw(self.experiment.raw_data.info.get('filename'))
    
    def on_pushButtonMaxFilter_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.maxFilterDialog = MaxFilterDialog(self, self.experiment.raw_data)
        self.maxFilterDialog.show()
    
    def on_currentChanged(self):
        """
        Keeps track of the active tab.
        Shows the epoch widget when in analysis.
        """
        index = self.ui.tabWidget.currentIndex()
        #self.tab = self.ui.tabWidget.currentWidget()
        if index == 2 or index == 1:
            self.widget.show()
        else:
            self.widget.hide()
        
    def on_pushButtonEOG_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.show()
        
    def on_pushButtonECG_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.ecgDialog = EcgParametersDialog(self)
        self.ecgDialog.show()
        
    def on_pushButtonApplyEOG_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.addEogProjs = AddEOGProjections(self)
        self.addEogProjs.exec_()
        
    def on_pushButtonApplyECG_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.addEcgProjs = AddECGProjections(self)
        self.addEcgProjs.exec_()
        
    def on_pushButtonTFR_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        epoch = self.widget.ui.listWidgetEpochs.currentItem().data(32).toPyObject()
        self.tfr_dialog = TFRDialog(self, self.experiment.raw_data, epoch)
        self.tfr_dialog.show()
    
    def on_pushButtonTFRTopology_clicked(self,checked=None):
        epoch = self.widget.ui.listWidgetEpochs.currentItem().data(32).toPyObject()
        self.tfrTop_dialog = TFRTopologyDialog(self, self.experiment.raw_data, epoch)
        self.tfrTop_dialog.show()
    
    def _initialize_ui(self):
        self.ui.tabWidget.insertTab(0, self.ui.tabRaw, "Raw")
        self.ui.tabWidget.insertTab(1, self.ui.tabPreprocessing, 
                                    "Preprocessing")
        self.ui.tabWidget.insertTab(2, self.ui.tabAnalysis, "Analysis")
        self.ui.checkBoxECG.hide()
        self.ui.checkBoxEOG.hide()
        self.ui.checkBoxMaxFilter.hide()
        self.ui.checkBoxEOGApplied.hide()
        self.ui.checkBoxECGApplied.hide()
        self.ui.pushButtonApplyEOG.setEnabled(False)
        self.ui.pushButtonApplyECG.setEnabled(False)
        
        #Check whether ECG projections are calculated
        fname = self.experiment.raw_data.info.get('filename')
        path = self.experiment._subject_directory
        files =  filter(os.path.isfile, glob.glob(path+'*_ecg_avg_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_ecg_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_ecg-eve.fif'))
        if len(files) > 1:
            self.ui.checkBoxECG.setCheckState(QtCore.Qt.Checked)
            self.ui.checkBoxECG.show()
            self.ui.pushButtonApplyECG.setEnabled(True)
        
        #Check whether EOG projections are calculated
        files =  filter(os.path.isfile, glob.glob(path+'*_eog_avg_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_eog_proj.fif'))
        files += filter(os.path.isfile, glob.glob(path+'*_eog-eve.fif'))
        if len(files) > 1:
            self.ui.checkBoxEOG.setCheckState(QtCore.Qt.Checked)
            self.ui.checkBoxEOG.show()
            self.ui.pushButtonApplyEOG.setEnabled(True)
        
        #Check whether ECG projections are applied
        files = filter(os.path.isfile, glob.glob(path + '*ecg_applied*'))
        if len(files) > 0:
            self.ui.checkBoxECGApplied.show()
            self.ui.checkBoxECGApplied.setCheckState(QtCore.Qt.Checked)
        
        #Check whether EOG projections are applied
        files = filter(os.path.isfile, glob.glob(path + '*eog_applied*'))
        if len(files) > 0:
            self.ui.checkBoxEOGApplied.show()
            self.ui.checkBoxEOGApplied.setCheckState(QtCore.Qt.Checked)
        
        files = filter(os.path.isfile, glob.glob(path + '*sss*'))
        if len(files) > 0:
            self.ui.checkBoxMaxFilter.show()
            self.ui.checkBoxMaxFilter.setCheckState(QtCore.Qt.Checked)
        
        #TODO: Maxfilter
    def check_workspace(self):
        self.workSpaceDialog = WorkSpaceDialog(self)
        self.workSpaceDialog.show()
        
    def hide_workspace_option(self):
        self.ui.actionSet_workspace.setVisible(False)

def main(): 
    app = QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
