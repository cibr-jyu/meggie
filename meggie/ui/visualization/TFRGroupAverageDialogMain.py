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
Created on Wed Apr  1 08:20:59 2015

@author: Jaakko Leppakangas
"""
from PyQt4 import QtGui, QtCore

from ui.visualization.TFRGroupAverageDialogUi import Ui_DialogGroupTFR
from ui.general.channelSelectionDialogMain import ChannelSelectionDialog

class TFRGroupAverageDialog(QtGui.QDialog):
    """
    Class containing the logic for plotting group average TFRs over all
    subjects
    """
    channels_selected = QtCore.pyqtSignal(list, str, int, bool, bool, bool)
    
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_DialogGroupTFR()
        self.ui.setupUi(self)
        # Topology plotting causes crashes at the moment. Disable option:
        self.ui.checkBoxSaveTopo.setVisible(False)

    def on_pushButtonModify_clicked(self, checked=None):
        """
        Opens a dialog for selecting channels.
        """
        if checked is None: return
        selChannels = list()
        for i in xrange(self.ui.listWidgetChannels.count()):
            selChannels.append(str(self.ui.listWidgetChannels.item(i).text()))
        title = 'Select channels of interest.'
        channelSelector = ChannelSelectionDialog(selChannels, title)
        channelSelector.channelsChanged.connect(self.channels_modified)
        channelSelector.exec_()


    @QtCore.pyqtSlot(list)
    def channels_modified(self, channels):
        """
        Slot for signal from channelSelectionDialog.
        Adds selected channels to the list of channels of interest.
        Keyword arguments:
        channels -- Channels to add to the list.
        """
        self.ui.listWidgetChannels.clear()
        self.ui.listWidgetChannels.addItems(channels)
        
    
    def getFigureParameters(self):
        """
        Method for getting parameters for the saved figures.
        """
        form = str(self.ui.comboBoxFormat.currentText())
        dpi = self.ui.spinBoxDpi.value()
        saveTopo = self.ui.checkBoxSaveTopo.isChecked()
        return form, dpi, saveTopo


    def accept(self):
        """
        Emits a signal for starting the computation.
        """
        form = str(self.ui.comboBoxFormat.currentText())
        dpi = self.ui.spinBoxDpi.value()
        saveTopo = self.ui.checkBoxSaveTopo.isChecked()
        channels = list()
        if self.ui.groupBox.isChecked():
            for i in xrange(self.ui.listWidgetChannels.count()):
                channels.append(str(self.ui.listWidgetChannels.item(i).text()))
        savePlot = self.ui.checkBoxSavePlot.isChecked()
        saveMax = self.ui.checkBoxSaveMaxima.isChecked()
        self.channels_selected.emit(channels, form, dpi, saveTopo, savePlot,
                                    saveMax)
        self.close()
        
