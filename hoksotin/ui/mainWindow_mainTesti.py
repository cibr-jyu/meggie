'''
Created on Mar 16, 2013

@author: jaeilepp
'''

import os,sys
import pickle
import subprocess
 
from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
import messageBox
from mainWindow_UiTesti import Ui_MainWindow
from CreateProjectDialog_mainTesti import CreateProjectDialog
#from UIehd1_main import MainWindow

from experiment import Experiment

import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from infoDialog_main import InfoDialog
from parameterDialog_main import ParameterDialog
from maxFilterDialog_main import MaxFilterDialog

from epochs import Epochs
from eventList import Events
from createEpochs import CreateEpochs
from widgets.create_tab import Tab, EpochTab

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
        self.ui.tabRaw.hide()
        self.ui.tabPreprocessing.hide()
        self.experiment = None
        self.raw = None
         
        #info = InfoDialog(self.raw, self.ui, False)
        self.ui.pushButtonAverage.setEnabled(False)
        self.ui.pushButtonVisualize.setEnabled(False)
        self.ui.tabWidget_2.currentChanged.connect(self.on_currentChanged)
        """ Draws a graph to the window"""
        
        """
        self.dpi = 100
        self.fig = Figure((5.0, 4.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.ui.centralwidget)
        self.axes = self.fig.add_subplot(111)
        
        picks = mne.fiff.pick_types(self.raw.info, meg='mag')
        start, stop = self.raw.time_as_index([0, 15])  # read the first 15s of data
        data, times = self.raw[picks[:5], start:(stop + 1)]  # take 5 first channels
        self.axes.plot(times, data.T)
        self.canvas.draw()
        #pl.xlabel('time (s)')
        #pl.ylabel('MEG data (T)')
        """
        
    def on_actionCreate_experiment_triggered(self):
        """
        Creates a new CreateProjectDialog and shows it
        """       
        self.dialog = CreateProjectDialog(self)
        self.dialog.show()
        
        
    def on_actionOpen_experiment_clicked(self, checked=None):
         # Standard workaround for file dialog opening twice
        if checked is None: return 
        
        path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select project directory"))
        
        fname = path + '/' + path.split('/')[-1] + '.pro'
        
        
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
        #os.environ['SUBJECT'] = 'jn'
        #os.environ['SUBJECTS_DIR'] = '/usr/local/bin/ParkkosenPurettu/mri-fs'
        #subprocess.Popen('export MNE_ROOT=/usr/local/bin/MNE-2.7.0-3106-Linux-x86_64', shell=True)
        #subprocess.Popen('export SUBJECT=jn', shell=True)
        #subprocess.Popen('export SUBJECTS_DIR=/usr/local/bin/ParkkosenPurettu/mri-fs', shell=True)
        subprocess.Popen('$MNE_ROOT', shell=True)
        #proc = subprocess.Popen('/usr/local/bin/MNE-2.7.0-3106-Linux-x86_64/bin/mne_browse_raw', shell=True, stdout=subprocess.PIPE,
        #                        stderr=subprocess.STDOUT)
        
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
      
      
    def create_epochs(self):
        stim_channel = str(self.epochParameterDialog.ui.comboBoxStimulus.currentText())
        event_id = int(self.epochParameterDialog.ui.spinBoxEventID.value())
        tmin = float(self.epochParameterDialog.ui.doubleSpinBoxTmin.value())
        tmax = float(self.epochParameterDialog.ui.doubleSpinBoxTmax.value())
        epoch_name = self.epochParameterDialog.ui.lineEditName.text()
        mag = self.epochParameterDialog.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.epochParameterDialog.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.epochParameterDialog.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.epochParameterDialog.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.epochParameterDialog.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        epochs = Epochs(self.raw, stim_channel, mag, grad, eeg, stim, eog, epoch_name, float(tmin),
                        float(tmax), int(event_id))
        #self.ui.tabEpoch = QtGui.QWidget()
        self.__create_tab(epoch_name, 'epoch')
        
        """
        
        print eveFile
        events = Events(eveFile)
        self.epochs = Epochs(self.raw, events.events)
        evoked = self.epochs.average()
        evoked.plot()
        """
    
    def on_currentChanged(self):
        print self.ui.tabWidget.currentIndex()
        self.tab = self.ui.tabWidget.currentWidget()
        if self.tab.winId == 'epoch':
            self.ui.pushButtonAverage.setEnabled(True)
        else:
            self.ui.pushButtonAverage.setEnabled(False)
    
    def __create_tab(self, title, id):
        """
        Creates a new tab with a listWidget to tabWidget.
        
        Keyword arguments:
        tab           -- A QWidget
        title         -- Title for the tab
        """
        EpochTab(title, self.ui, id)
        """
        self.ui.tabWidget.addTab(tab, title)
        self.horizontalLayoutWidget = QtGui.QWidget(tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 341, 481))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.metaBox = QtGui.QGroupBox(self.horizontalLayoutWidget)
        self.metaBox.setTitle("Background")
        self.verticalLayout.addWidget(self.metaBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        """
        
       
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
