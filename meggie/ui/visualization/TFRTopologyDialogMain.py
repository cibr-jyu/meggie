# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
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

@author: Kari Aliranta, Jaakko Leppakangas
Contains the TFRTopologyDialog-class used for creating TFR-topologies.
"""
from PyQt4 import QtCore, QtGui
import numpy as np

from meggie.code_meggie.general import fileManager
from meggie.code_meggie.general.caller import Caller

from meggie.ui.visualization.TFRtopologyUi import Ui_DialogTFRTopology

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox

class TFRTopologyDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRTopologyDialog. Collects the necessary
    parameter values and passes them to the Caller-class.
    """
    caller = Caller.Instance()    
    
    def __init__(self, parent, epoch_name):
        """
        Initializes the TFR topology dialog.
        
        Keyword arguments:
        
        parent     --   This dialog's parent.
        epoch_name --   The name of a collection of epochs.
        tfr        --   A pre-calculated TFR to plot. Defaults to None.
        """
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.epoch_name = epoch_name
        self.ui = Ui_DialogTFRTopology()
        self.ui.setupUi(self)

        subject = self.caller.experiment.active_subject
        epochs = subject.epochs[epoch_name].raw
        self.ui.labelEpochName.setText(epoch_name)
        self.ui.doubleSpinBoxScalpTmin.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxScalpTmax.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxScalpTmin.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxScalpTmax.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineStart.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineStart.setValue(epochs.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)

    def accept(self):
        """
        Collects the parameter values from the dialog window and passes them
        to the caller. Also checks for erroneus parameter values and gives 
        feedback to the user.
        """
        cmap = str(self.ui.comboBoxCmap.currentText())
        
        if self.ui.groupBoxBaseline.isChecked():
            mode = str(self.ui.comboBoxMode.currentText())
            blstart = self.ui.doubleSpinBoxBaselineStart.value()
            blend = self.ui.doubleSpinBoxBaselineEnd.value()
        else:
            blstart, blend, mode = None, None, None
            
        if self.ui.radioButtonInduced.isChecked():
            reptype = 'average'
        elif self.ui.radioButtonPhase.isChecked():
            reptype = 'itc'

        save_data = self.ui.checkBoxSaveData.isChecked()

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        freqs = np.arange(minfreq, maxfreq, interval)
        
        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()

        ch_type = str(self.ui.comboBoxChannels.currentText())

        subject = self.caller.experiment.active_subject
        epochs = subject.epochs[self.epoch_name].raw
        
        # not stored in epochs when saved                             
        epochs.name = self.epoch_name  
        
        scalp = dict()
        if self.ui.groupBoxScalp.isChecked():
            scalp['tmin'] = self.ui.doubleSpinBoxScalpTmin.value()
            scalp['tmax'] = self.ui.doubleSpinBoxScalpTmax.value()
            scalp['fmin'] = self.ui.doubleSpinBoxScalpFmin.value()
            scalp['fmax'] = self.ui.doubleSpinBoxScalpFmax.value()
        else:
            scalp = None
        try:             
            self.caller.TFR_topology(inst=epochs, reptype=reptype, freqs=freqs, 
                decim=decim, mode=mode, blstart=blstart, blend=blend, 
                ncycles=ncycles, ch_type=ch_type, scalp=scalp, 
                color_map=cmap, save_data=save_data)
        except Exception as e:
            exc_messagebox(self.parent, e)


