# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
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
@author: Jaakko Leppakangas
Contains the InfoDialog-class used for viewing background info from
a raw data file.
"""

import sys
from PyQt4 import QtCore, QtGui
from infoDialogUi import Ui_infoDialog
from measurementInfo import MeasurementInfo
import mne


class InfoDialog(QtGui.QDialog):
    """
    Dialog to get and show the info from the raw file. Can be used to direct
    the extracted information from the file to the dialog itself or some
    other ui with similar element names. Currently used for setting the
    subject info fields below the subject list in the mainWindow. 
    """
    def __init__(self, raw, targetUi, create_window):
        """
        Constructor    
        Keyword arguments:
        raw           -- Raw object.
        targetUi      -- Ui object that receives the info data.
        create_window -- Boolean to determine if a new dialog window 
        is created.
        """
        QtGui.QDialog.__init__(self)
        self.raw = raw
        self.ui = targetUi
        if create_window:
            self.ui.setupUi(self)
            self.ui.tab_list = []
        
        self._setLabelTestValues()
    
    def on_ButtonClose_clicked(self):
        """
        Closes the dialog
        """
        self.close()
        
    def _setLabelTestValues(self):
        """
        Sets the data info to the labels.
        """
        self.mi = MeasurementInfo(self.raw)
        
        self.ui.labelDateValue.setText(self.mi.date)
        self.ui.labelEEGValue.setText(str(self.mi.EEG_channels))
        self.ui.labelGradMEGValue.setText(str(self.mi.grad_channels))
        self.ui.labelHighValue.setText(str(self.mi.high_pass) + ' Hz')
        self.ui.labelLowValue.setText(str(self.mi.low_pass) + ' Hz')
        self.ui.labelMagMEGValue.setText(str(self.mi.mag_channels))
        self.ui.labelSamplesValue.setText(str(self.mi.sampling_freq) + ' Hz')
        self.ui.labelSubjectValue.setText(self.mi.subject_name)
