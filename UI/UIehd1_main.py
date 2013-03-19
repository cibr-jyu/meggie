'''
Created on Mar 16, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from UIehdotus4 import Ui_MainWindow
import mne
import pylab as pl
from matplotlib.figure import Figure
import matplotlib
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from infoDialog_main import InfoDialog
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
        self.item = QtGui.QTreeWidgetItem(self.ui.treeWidget)
        self.raw = project.get_raw_data()
        self.ui.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("MainWindow", str(self.raw), None, QtGui.QApplication.UnicodeUTF8))
        self.ui.treeWidget.editItem
        info = InfoDialog(self.raw, self.ui, False)
        
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