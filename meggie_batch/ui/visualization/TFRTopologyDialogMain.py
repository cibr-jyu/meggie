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
Created on Apr 26, 2013

@author: Kari Aliranta, Jaakko Leppakangas
Contains the TFRTopologyDialog-class used for creating TFR-topologies.
"""
from PyQt4 import QtCore, QtGui

from code_meggie.general.caller import Caller
from TFRtopologyUi import Ui_DialogTFRTopology
from TFRGroupAverageDialogMain import TFRGroupAverageDialog
from ui.general.messageBoxes import shortMessageBox
from code_meggie.general import fileManager

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
        
        parent    --   this dialog's parent
        epoch_name    --   the name of a collection of epochs
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.epoch_name = epoch_name
        self.ui = Ui_DialogTFRTopology()
        self.ui.setupUi(self)
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)
        epochs = self.caller.experiment.active_subject._epochs[epoch_name]._raw
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

    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Opens a dialog for selecting a layout file.
        """
        if checked is None: return
        fName = str(QtGui.QFileDialog.getOpenFileName(self,
                            "Select a layout file", '/home/', 
                            "Layout-files (*.lout *.lay);;All files (*.*)"))
        self.ui.labelLayout.setText(fName)

    def accept(self):
        """
        Collects the parameter values from the dialog window and passes them
        to the caller. Also checks for erroneus parameter values and gives 
        feedback to the user.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
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

        if self.ui.radioButtonInduced.isChecked(): reptype = 'average'
        elif self.ui.radioButtonPhase.isChecked(): reptype = 'itc'
        ch_type = str(self.ui.comboBoxChannels.currentText())
        if self.ui.radioButtonSelectLayout.isChecked():
            layout = self.ui.comboBoxLayout.currentText()
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
        if layout == 'No layout selected' or layout == '':
            QtGui.QApplication.restoreOverrideCursor()
            self.messageBox = shortMessageBox('No layout selected')
            self.messageBox.show()
            return
        epochs = self.caller.experiment.active_subject._epochs[self.epoch_name]
        scalp = dict()
        if self.ui.groupBoxScalp.isChecked():
            scalp['tmin'] = self.ui.doubleSpinBoxScalpTmin.value()
            scalp['tmax'] = self.ui.doubleSpinBoxScalpTmax.value()
            scalp['fmin'] = self.ui.doubleSpinBoxScalpFmin.value()
            scalp['fmax'] = self.ui.doubleSpinBoxScalpFmax.value()
        else:
            scalp = None
        try:
            self.caller.TFR_topology(epochs._raw, reptype, minfreq, maxfreq,
                                     decim, mode, blstart, blend, interval,
                                     ncycles, layout, ch_type, scalp)
        except Exception, err:
            QtGui.QApplication.restoreOverrideCursor()
            self.messageBox = shortMessageBox(str(err))
            self.messageBox.show()
            return
        QtGui.QApplication.restoreOverrideCursor()
        self.close()

    def on_pushButtonGroupAverage_clicked(self, checked=None):
        """
        Opens a dialog for group average parameters.
        """
        if checked is None: return
        averageDialog = TFRGroupAverageDialog()
        averageDialog.channels_selected.connect(self.compute_group_average)
        averageDialog.exec_()

    @QtCore.pyqtSlot(list, str, int, bool, bool, bool)
    def compute_group_average(self, channels, form, dpi, saveTopo, savePlot,
                              saveMax):
        """
        Starts the computation of group average TFR.
        Parameters:
        channels - Selected channels of interest.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
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

        if self.ui.radioButtonInduced.isChecked(): reptype = 'average'
        elif self.ui.radioButtonPhase.isChecked(): reptype = 'itc'

        if saveMax:
            saveMax = reptype
        else:
            saveMax = None

        if self.ui.radioButtonSelectLayout.isChecked():
            layout = self.ui.comboBoxLayout.currentText()
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
        if layout == 'No layout selected' or layout == '':
            QtGui.QApplication.restoreOverrideCursor()
            self.messageBox = shortMessageBox('No layout selected')
            self.messageBox.show()
            return
        try:
            self.caller.TFR_average(self.epoch_name, reptype, mode,
                                    minfreq, maxfreq, interval, blstart,
                                    blend, ncycles, decim, layout, channels,
                                    form, dpi, saveTopo, savePlot, saveMax)
        except Exception, err:
            QtGui.QApplication.restoreOverrideCursor()
            self.messageBox = shortMessageBox(str(err))
            self.messageBox.show()
            QtGui.QApplication.restoreOverrideCursor()
            return
        QtGui.QApplication.restoreOverrideCursor()
