# coding: utf-8

"""
Created on 30.5.2016

@author: jaolpeso
"""

from collections import OrderedDict

from PyQt4 import QtGui

from meggie.ui.analysis.powerSpectrumEpochsDialogUi import Ui_Dialog
from meggie.code_meggie.general.caller import Caller
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class PowerSpectrumEpochsDialog(QtGui.QDialog):
    """
    """
    caller = Caller.Instance()
    
    def __init__(self, parent, epochs):
        """
        Constructor. Sets up the dialog
        
        Keyword arguments:
        
        parent    --    Parent of the dialog
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.epochs = epochs
        
        self.ui.spinBoxNfft.setValue(128)
        self.ui.spinBoxOverlap.setValue(64)
        
    def accept(self):
        """
        Collects parameters and calls the caller class to create a TFR.
        """
        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()
        if fmin >= fmax:
            messagebox(self.parent, 
                "End frequency must be higher than the starting frequency")
            return

        valid = True
        for epoch in self.epochs:
            length = len(epoch.raw[0].times)
            if length < float(self.ui.spinBoxNfft.value()):
                valid = False
        if not valid:
            messagebox(self.parent, "Sampling rate times shortest epoch length should be more than window size")  # noqa
            return
        
        params = dict()
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['log'] = self.ui.checkBoxLogarithm.isChecked()
        params['overlap'] = self.ui.spinBoxOverlap.value()
        # params['average'] = self.ui.checkBoxAverage.isChecked()
        save_data = self.ui.checkBoxSaveData.isChecked()
             
        average = self.ui.checkBoxAverage.isChecked()
        
        mne_epochs = OrderedDict()
        for epoch in self.epochs:
            mne_epoch = epoch.raw
            mne_epoch.comment = epoch.collection_name
            if average:
                if 'average' not in mne_epochs:
                    mne_epochs['average'] = []
                mne_epochs['average'].append(mne_epoch)                
            else:
                mne_epochs[epoch.collection_name] = [mne_epoch]
            
        try:
            self.caller.plot_power_spectrum(params, save_data, mne_epochs, basename='epochs')
        except Exception as e:
            exc_messagebox(self, e)
