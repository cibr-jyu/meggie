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
Created on 24.5.2016

@author: jaolpeso
"""
from PyQt4 import QtGui

from meggie.ui.visualization.TFRfromRawDialogUi import Ui_DialogRawTFR
from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.general import fileManager
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class TFRRawDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRDialog. Collects the necessary parameter
    values and passes them to the Caller-class.
    """
    caller = Caller.Instance()
    
    def __init__(self, parent):
        """
        Constructor. Sets up the dialog
        
        Keyword arguments:
        
        parent    --    Parent of the dialog
        epochs    --    a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogRawTFR()
        self.ui.setupUi(self)
        
        raw = self.caller.experiment.active_subject.get_working_file()
        channels = raw.info['ch_names']
        self.ui.comboBoxChannel.addItems(channels)

        # Populate layouts combobox.
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)

        
    def accept(self):
        """
        Collects parameters and calls the caller class to create a TFR.
        """
        wsize = self.ui.spinBoxWsize.value()
        if self.ui.checkBoxTstep.isChecked():
            tstep = wsize / 2
        else:
            tstep = self.ui.spinBoxTstep.value()
            
        channel = self.ui.comboBoxChannel.currentText()
        fmin, fmax = None, None

        if self.ui.checkBoxFrequency.isChecked():
            fmin = self.ui.spinBoxFmin.value()
            fmax = self.ui.spinBoxFmax.value()
        
        if self.ui.radioButtonSelectLayout.isChecked():
            layout = str(self.ui.comboBoxLayout.currentText())
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
            if layout == 'No layout selected':
                messagebox(self.parent, 'No layout selected!')
                return
        
        try:
            self.caller.TFR_raw(wsize, tstep, layout, channel, fmin, fmax)
        except Exception as e:
            exc_messagebox(self, e)
            
        self.close()

    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Called when browse layout button is clicked.
        Opens a file dialog for selecting a file.
        """
        if checked is None:
            return
        fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                      '/home/', "Layout-files "
                                                      "(*.lout *.lay);;All "
                                                      "files (*.*)"))
        self.ui.labelLayout.setText(fname)
