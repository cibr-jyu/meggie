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
Created on May 15, 2013

@author: Jaakko Leppakangas
Contains the SpectrumDialog-class used in plotting magnitude spectrums.
"""
from PyQt4 import QtCore,QtGui

from spectrumDialogUi import Ui_DialogSpectrum

class SpectrumDialog(QtGui.QDialog):
    """
    Dialog for getting the channel from the user and plotting
    the magnitude spectrum.
    """

    def __init__(self, parent):
        '''
        Constructor
        Keyword arguments:
        parent        -- Parent of this object.
        '''
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogSpectrum()
        self.ui.setupUi(self)
        ch_names = self.parent.experiment.active_subject._working_file.ch_names
        self.ui.comboBoxChannel.addItems(ch_names)
        
    def accept(self):
        """
        Reads values from the dialog, saves them in a dictionary and initiates
        a caller to actually call the backend.
        """
        # TODO: muuta
        ch_index = self.ui.comboBoxChannel.currentIndex()
        raw = self.parent.experiment.active_subject._working_file
        print ch_index
        #self.parent.caller.magnitude_spectrum(raw, ch_index)
        # TODO: fmin ja fmax valinnat
        self.parent.experiment.active_subject._working_file.plot_psds(picks=ch_index)
        self.close()