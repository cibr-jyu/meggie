'''
Created on Mar 16, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from UIehd5 import Ui_MainWindow
import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from infoDialog_main import InfoDialog
from parameterDialog_main import ParameterDialog

from epochs import Epochs
from eventList import Events
from createEpochs import CreateEpochs

class MainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''


    def __init__(self, project):
        '''
        Constructor
        '''
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.tabEvoked = None
        #self.item = QtGui.QTreeWidgetItem(self.ui.treeWidget)
        self.raw = project.get_raw_data()
        #self.ui.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("MainWindow", str(self.raw), None, QtGui.QApplication.UnicodeUTF8))
        #self.ui.treeWidget.editItem
        info = InfoDialog(self.raw, self.ui, False)
        
        
        #print self.events
        #self.epochs = Epochs
        
        
        
        
        
        
        
        
        
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
        
        
        
    def on_pushButtonEpoch_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.epochParameterDialog = ParameterDialog(self)
        self.epochParameterDialog.show()
        #eveFile = self.raw.info.get('filename')[:-4] + '-eve.fif'
        #self.epochParameterDialog.fileEdit.setText(eveFile)
        
    def on_pushButtonAverage_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        epoch = self.ui.listWidgetEpochs.currentItem().data(1).toPyObject()
        evoked = epoch.average()
        
        #Check if the tab has already been created
        if self.ui.tabEvoked == None:
            self.ui.tabEvoked = QtGui.QWidget()
            self.ui.listWidgetAverage = QtGui.QListWidget()
            self.ui.listWidgetAverage = self.__create_tab(self.ui.tabEvoked, 'Evoked', self.ui.listWidgetAverage)
        item = QtGui.QListWidgetItem()
        item.setText('TestElement')
        item.setData(1,evoked)
        self.ui.listWidgetAverage.addItem(item)
        evoked.plot()
        
    def create_epochs(self):
        stim_channel = str(self.epochParameterDialog.ui.comboBoxStimulus.currentText())
        event_id = self.epochParameterDialog.ui.lineEditEventID.text()
        tmin = self.epochParameterDialog.ui.lineEditTmin.text()
        tmax = self.epochParameterDialog.ui.lineEditTmax.text()
        reject = self.epochParameterDialog.ui.lineEditReject.text()
        meg = self.epochParameterDialog.ui.checkBoxMeg.checkState() == QtCore.Qt.Checked
        eeg = self.epochParameterDialog.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.epochParameterDialog.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.epochParameterDialog.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        epochs = CreateEpochs(self.raw, event_id, stim_channel, tmin,
                              tmax, reject, meg, eeg, stim, eog)
        item = QtGui.QListWidgetItem()
        item.setText('Event ID: ' + str(epochs.e.epochs.event_id))
        item.setData(1,epochs.e.epochs)
        self.ui.listWidgetEpochs.addItem(item)
        """
        
        print eveFile
        events = Events(eveFile)
        self.epochs = Epochs(self.raw, events.events)
        evoked = self.epochs.average()
        evoked.plot()
        """
    
    def __create_tab(self, tab, title, list):
        """
        Creates a new tab with a listWidget to tabWidget.
        
        Keyword arguments:
        tab           -- A QWidget
        title         -- Title for the tab
        list          -- A QListWidget
        returns a reference to the newly created listWidget
        """
        self.ui.horizontalLayoutWidget = QtGui.QWidget(tab)
        self.ui.tabWidget.addTab(tab, title)
        self.ui.horizontalLayoutWidget = QtGui.QWidget(tab)
        self.ui.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10,
                                                                341, 511))
        list = QtGui.QListWidget(self.ui.horizontalLayoutWidget)
        #self.ui.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.ui.horizontalLayout = QtGui.QHBoxLayout(self.ui.
                                                     horizontalLayoutWidget)
        self.ui.horizontalLayout.setMargin(0)
        self.ui.horizontalLayout.addWidget(list)
        return list
        #self.listWidget.setObjectName(("listWidgetEpochs"))
        