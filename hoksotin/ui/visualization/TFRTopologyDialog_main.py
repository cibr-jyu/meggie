'''
Created on Apr 26, 2013

@author: jaeilepp
'''
import mne

from PyQt4 import QtCore,QtGui
from TFRTopologyDialog_Ui import Ui_DialogTFRTopology

class TFRTopologyDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRTopologyDialog.
    """
    
    def __init__(self, parent, raw, epoch):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.raw = raw
        self.epoch = epoch
        ch_names = self.epoch.epochs.ch_names
        self.ui = Ui_DialogTFRTopology()
        self.ui.setupUi(self)
    
    def accept(self):
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        mode = self.ui.comboBoxMode.currentText()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles = self.ui.doubleSpinBoxNcycles.value()
        if ( self.ui.checkBoxBaselineStartNone.isChecked() ):
            blstart = None
        else: blstart = self.ui.doubleSpinBoxBaselineStart.value()
        
        if ( self.ui.checkBoxBaselineEndNone.isChecked() ):
            blend = None
        else: blend = self.ui.doubleSpinBoxBaselineEnd.value()
        
        if ( self.ui.radioButtonInduced.isChecked() ):
            reptype = 'induced'
        else: reptype = 'phase'
        
        self.parent.caller.TFR_topology(self.raw, self.epoch.epochs, reptype,
                                        minfreq, maxfreq, decim, mode, 
                                        blstart, blend, interval, ncycles)
        self.close()