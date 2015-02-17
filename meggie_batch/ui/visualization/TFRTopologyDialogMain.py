# coding: latin1

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
import mne

from PyQt4 import QtCore,QtGui
from TFRtopologyUi import Ui_DialogTFRTopology
from code_meggie.general.caller import Caller
import messageBoxes

class TFRTopologyDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRTopologyDialog. Collects the necessary
    parameter values and passes them to the Caller-class.
    """
    
    def __init__(self, parent, raw, epochs):
        """
        Initializes the TFR topology dialog.
        
        Keyword arguments:
        
        parent    --   this dialog's parent
        raw       --   a raw data file
        epochs    --   a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.raw = raw
        self.epochs = epochs
        ch_names = self.epochs.ch_names
        self.ui = Ui_DialogTFRTopology()
        self.ui.setupUi(self)
    
    def accept(self):
        """
        Collects the parameter values from the dialog window and passes them
        to the caller. Also checks for erroneus parameter values and gives 
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
            caller = Caller.Instance()
            caller.TFR_topology(self.raw, self.epochs,
                                            reptype, minfreq, maxfreq, decim,
                                            mode, blstart, blend, interval,
                                            ncycles)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            return
        self.close()