'''
Created on Apr 26, 2013

@author: Janne Leppakangas
'''
import messageBox

import mne

from PyQt4 import QtCore,QtGui
from TFRDialog_Ui import Ui_DialogEpochsTFR

class TFRDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRDialog.
    """
    
    def __init__(self, parent, raw, epoch):
        """
        Constructor. Sets up the dialog
        
        Keyword arguments:
        
        parent    --    Parent of the dialog
        raw       --    raw data file
        epoch     --    a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.raw = raw
        self.epoch = epoch
        ch_names = self.epoch.epochs.ch_names
        self.ui = Ui_DialogEpochsTFR()
        self.ui.setupUi(self)
        self.ui.comboBoxChannels.addItems(ch_names)
    
    def accept(self):
        """
        Collects parameters and calls the caller class to create a TFR.
        """
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        ch_index = self.ui.comboBoxChannels.currentIndex()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles =  self.ui.spinBoxNcycles.value()
        decim = self.ui.spinBoxDecim.value()
        try:
            self.parent.caller.TFR(self.raw, self.epoch.epochs, ch_index,
                                   minfreq, maxfreq, interval, ncycles, decim)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            #self.computeDialog.close()
            return
        self.close()