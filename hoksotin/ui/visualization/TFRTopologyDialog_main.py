# coding: latin1
"""
Created on Apr 26, 2013

@author: Kari Aliranta, Jaakko Leppakangas
"""
import mne

from PyQt4 import QtCore,QtGui
from TFRTopologyDialog_Ui import Ui_DialogTFRTopology
import messageBox

class TFRTopologyDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRTopologyDialog.
    """
    
    def __init__(self, parent, raw, epoch):
        """
        Initializes the TFR topology dialog.
        
        Keyword arguments:
        
        parent    --   this dialog's parent
        raw       --   a raw data file
        epoch     --   a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.raw = raw
        self.epoch = epoch
        ch_names = self.epoch.epochs.ch_names
        self.ui = Ui_DialogTFRTopology()
        self.ui.setupUi(self)
    
    def accept(self):
        """
        Collects the parameter values from the dialog window and passes them
        to the Caller. Also checks for erroneus parameter values and gives 
        feedback to the user.
        """
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        mode = self.ui.comboBoxMode.currentText()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles = self.ui.spinBoxNcycles.value()
        if ( self.ui.checkBoxBaselineStartNone.isChecked() ):
            blstart = None
        else: blstart = self.ui.doubleSpinBoxBaselineStart.value()
        
        if ( self.ui.checkBoxBaselineEndNone.isChecked() ):
            blend = None
        else: blend = self.ui.doubleSpinBoxBaselineEnd.value()
        
        if ( self.ui.radioButtonInduced.isChecked() ):
            reptype = 'induced'
        else: reptype = 'phase'
        try:
            self.parent.caller.TFR_topology(self.raw, self.epoch.epochs,
                                            reptype, minfreq, maxfreq, decim,
                                            mode, blstart, blend, interval,
                                            ncycles)
        except ValueError, err:
            if len(str(err)) < 100:
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText('Check parameters. ' +
                                                       str(err))
                self.messageBox.exec_()
            else:
                print str(err)
            return
            
        self.close()