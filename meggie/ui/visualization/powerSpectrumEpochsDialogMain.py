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
Created on 30.5.2016

@author: jaolpeso
"""
from PyQt4 import QtGui

from meggie.ui.visualization.powerSpectrumEpochsDialogUi import Ui_Dialog
from meggie.code_meggie.general.caller import Caller
from meggie.ui.utils.messaging import exc_messagebox

class PowerSpectrumEpochsDialog(QtGui.QDialog):
    """
    """
    
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
        self.ui.comboBoxChannelType.addItem('grad')
        self.ui.comboBoxChannelType.addItem('mag')
        self.ui.comboBoxChannelType.addItem('planar1')
        self.ui.comboBoxChannelType.addItem('planar2')
        
    def accept(self):
        """
        Collects parameters and calls the caller class to create a TFR.
        """
        ch_type = self.ui.comboBoxChannelType.currentText()
        normalize = False
        if self.ui.checkBoxNormalize.isChecked():
            normalize = True
        caller = Caller.Instance()
        
        try:
            caller.plot_power_spectrum_epochs(self.epochs, ch_type, normalize)
        except Exception as e:
            exc_messagebox(self, e)
