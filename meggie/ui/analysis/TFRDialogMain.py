# coding: utf-8

"""
Created on Apr 26, 2013

@author: Jaakko Leppakangas
Contains the TFRDialog-class used for creating TFRs.
"""
from PyQt4 import QtCore, QtGui

import numpy as np

from meggie.code_meggie.analysis.spectral import TFR

from meggie.ui.analysis.TFRfromEpochsUi import Ui_DialogEpochsTFR
from meggie.ui.utils.messaging import exc_messagebox

class TFRDialog(QtGui.QDialog):
    """
    """
    
    def __init__(self, parent, epochs):
        """
        Constructor. Sets up the dialog
        
        Keyword arguments:
        
        parent    --    Parent of the dialog
        epochs    --    a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.epochs = epochs
        ch_names = self.epochs.raw.ch_names
        self.ui = Ui_DialogEpochsTFR()
        self.ui.setupUi(self)
        self.ui.comboBoxChannels.addItems(ch_names)
        
        self.ui.doubleSpinBoxBaselineStart.setMinimum(epochs.raw.tmin)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(epochs.raw.tmax)
        self.ui.doubleSpinBoxBaselineStart.setValue(epochs.raw.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(epochs.raw.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(epochs.raw.tmax)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)
        

    def accept(self):
        """
        """
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        ch_index = self.ui.comboBoxChannels.currentIndex()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles =  self.ui.doubleSpinBoxNcycles.value()
        freqs = np.arange(minfreq, maxfreq, interval)        
        
        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()        
        
        if self.ui.groupBoxBaseline.isChecked():
            mode = str(self.ui.comboBoxMode.currentText())
            blstart = self.ui.doubleSpinBoxBaselineStart.value()
            blend = self.ui.doubleSpinBoxBaselineEnd.value()
        else:
            blstart, blend, mode = None, None, None
        
        decim = self.ui.spinBoxDecim.value()
        cmap = str(self.ui.comboBoxCmap.currentText())
        
        save_data = self.ui.checkBoxSaveData.isChecked()

        try:
            experiment = self.parent.experiment
            n_jobs = self.parent.preferencesHandler.n_jobs
            TFR(experiment, epochs=self.epochs.raw,
                collection_name=self.epochs.collection_name, ch_index=ch_index,
                freqs=freqs, ncycles=ncycles, decim=decim, mode=mode,
                blstart=blstart, blend=blend, save_data=save_data,
                color_map=cmap, n_jobs=n_jobs)
        except Exception as e:
            exc_messagebox(self, e)
