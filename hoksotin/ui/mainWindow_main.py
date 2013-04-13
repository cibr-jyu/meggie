'''
Created on Mar 16, 2013

@author: jaeilepp
'''

import os,sys
import pickle
import subprocess
 
from PyQt4 import QtCore,QtGui

import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
 
from mainWindow_Ui import Ui_MainWindow
from CreateProjectDialog_main import CreateProjectDialog
from infoDialog_main import InfoDialog
from parameterDialog_main import ParameterDialog
from maxFilterDialog_main import MaxFilterDialog
from eogParametersDialog_main import EogParametersDialog
import messageBox

from experiment import Experiment
from epochs import Epochs
from events import Events

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
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabEvoked = None
        
        #Only leaves the blank tab in tabWidget initially
        self.ui.tabWidget.removeTab(1)
        self.ui.tabWidget.removeTab(1)
        
        self.experiment = None
        self.raw = None
         
        #info = InfoDialog(self.raw, self.ui, False)
        self.ui.pushButtonAverage.setEnabled(False)
        self.ui.pushButtonVisualize.setEnabled(False)
        self.ui.tabWidget.currentChanged.connect(self.on_currentChanged)
        
        
    def on_actionCreate_experiment_triggered(self):
        """
        Creates a new CreateProjectDialog and shows it
        """       
        self.dialog = CreateProjectDialog(self)
        self.dialog.show()
        
        
    def on_actionOpen_experiment_triggered(self, checked=None):
         # Standard workaround for file dialog opening twice
        if checked is None: return 
        
        path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select project directory"))
        
        fname = path + '/' + path.split('/')[-1] + '.pro'
         # TODO needs exception checking for corrupt/wrong type of file
        if os.path.exists(path) and os.path.isfile(fname):
            output = open(fname, 'rb')
            self.experiment = pickle.load(output)
            #workaround for setting up the raw object
            self.experiment.raw_data = mne.fiff.Raw(experiment.raw_data.info.get('filename'))
            
        
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Project files not found.')
            self.messageBox.show()
          
        
    def on_pushButtonEpoch_clicked(self, checked=None):
        """
        Opens the epoch dialog. 
        """
        # Standard workaround for file dialog opening twice
        if checked is None: return
        self.epochParameterDialog = ParameterDialog(self)
        self.epochParameterDialog.show()
        #eveFile = self.raw.info.get('filename')[:-4] + '-eve.fif'
        #self.epochParameterDialog.fileEdit.setText(eveFile)
        
        
    def on_pushButtonAverage_clicked(self, checked=None):
        # Standard workaround for file dialog opening twice
        if checked is None: return 
        epoch = self.ui.listWidgetEpochs.currentItem().data(1).toPyObject()
        evoked = epoch.average()
        
        #Check if the tab has already been created
        if self.ui.tabEvoked == None:
            self.ui.tabEvoked = QtGui.QWidget()
            self.ui.listWidgetAverage = self.__create_tab(self.ui.tabEvoked,
                                                          'Evoked')
        item = QtGui.QListWidgetItem()
        item.setText('TestElement')
        item.setData(1,evoked)
        self.ui.listWidgetAverage.addItem(item)
        evoked.plot()
        
        
    def on_pushButtonMNE_Browse_Raw_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        
        # Should this path be in the program settings?
        os.environ['MNE_ROOT'] = '/usr/local/bin/MNE-2.7.0-3106-Linux-x86_64'
        subprocess.Popen('$MNE_ROOT', shell=True)
        
        # Opens browse_raw in a separate thread
        proc = subprocess.Popen('$MNE_ROOT/bin/mne_browse_raw --raw ' + self.raw.info.get('filename'), shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()
        print "the program return code was %d" % retval  
        
        
    def on_pushButtonMaxFilter_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.maxFilterDialog = MaxFilterDialog(self, self.raw)
        self.maxFilterDialog.show()
       
    
    def on_currentChanged(self):
        print self.ui.tabWidget.currentIndex()
        self.tab = self.ui.tabWidget.currentWidget()
        if self.tab.winId == 'epoch':
            self.ui.pushButtonAverage.setEnabled(True)
        else:
            self.ui.pushButtonAverage.setEnabled(False)
        
    def on_pushButtonEOG_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.eogDialog = EogParametersDialog(self)
        self.eogDialog.show()
       
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
