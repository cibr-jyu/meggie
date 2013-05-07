'''
Created on Apr 26, 2013

@author: jaeilepp
'''
import mne

from PyQt4 import QtCore,QtGui
from TFRDialog_Ui import Ui_DialogEpochsTFR

class TFRDialog(QtGui.QDialog):
    
    def __init__(self, parent, raw, epoch):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.raw = raw
        self.epoch = epoch
        ch_names = self.epoch.epochs.ch_names
        self.ui = Ui_DialogEpochsTFR()
        self.ui.setupUi(self)
        self.ui.comboBoxChannels.addItems(ch_names)
    
    def accept(self):
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        ch_index = self.ui.comboBoxChannels.currentIndex()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles =  self.ui.spinBoxNcycles.value()
        decim = self.ui.spinBoxDecim.value()
        self.parent.caller.TFR(self.raw, self.epoch.epochs, ch_index, minfreq,
                               maxfreq, interval, ncycles, decim)
        self.close()