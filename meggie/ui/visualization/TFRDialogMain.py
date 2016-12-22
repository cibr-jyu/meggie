# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Apr 26, 2013

@author: Jaakko Leppakangas
Contains the TFRDialog-class used for creating TFRs.
"""
from PyQt4 import QtCore, QtGui

import numpy as np

from meggie.ui.visualization.TFRfromEpochsUi import Ui_DialogEpochsTFR
from meggie.code_meggie.general.caller import Caller
from meggie.ui.utils.messaging import exc_messagebox

class TFRDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRDialog. Collects the necessary parameter
    values and passes them to the Caller-class.
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
        Collects parameters and calls the caller class to create a TFR.
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

        caller = Caller.Instance()
        try:
            caller.TFR(epochs=self.epochs.raw,
                collection_name=self.epochs.collection_name, ch_index=ch_index,
                freqs=freqs, ncycles=ncycles, decim=decim, mode=mode,
                blstart=blstart, blend=blend, save_data=save_data,
                color_map=cmap)
        except Exception as e:
            exc_messagebox(self, e)
