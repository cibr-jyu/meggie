# coding: utf-8

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

from meggie.code_meggie.general import fileManager
from meggie.code_meggie.general.caller import Caller

from meggie.ui.visualization.TFRtopologyUi import Ui_DialogTFRTopology
from meggie.ui.visualization.TFRGroupAverageDialogMain import TFRGroupAverageDialog
from meggie.ui.general.messageBoxes import shortMessageBox


class TFRTopologyDialog(QtGui.QDialog):
    """
    Class containing the logic for TFRTopologyDialog. Collects the necessary
    parameter values and passes them to the Caller-class.
    """
    caller = Caller.Instance()    
    
    def __init__(self, parent, epoch_name, tfr=None):
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
        layouts = fileManager.get_layouts()
        self.ui.comboBoxLayout.addItems(layouts)
        if tfr is None:
            self.tfr = None
            subject = self.caller.experiment.active_subject
            epochs = subject.get_epochs(epoch_name)
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
        else:
            self.tfr = tfr
            if tfr.method == 'morlet-power':
                self.ui.radioButtonInduced.setChecked(True)
            elif tfr.method == 'morlet-itc':
                self.ui.radioButtonPhase.setChecked(True)
            self.ui.radioButtonInduced.setEnabled(False)
            self.ui.radioButtonPhase.setEnabled(False)
            self.ui.groupBoxFrequencies.setVisible(False)
            self.ui.groupBoxScalp.setVisible(False)
            self.ui.pushButtonGroupAverage.setVisible(False)
            self.ui.doubleSpinBoxBaselineStart.setMinimum(tfr.times[0])
            self.ui.doubleSpinBoxBaselineStart.setMaximum(tfr.times[-1])
            self.ui.doubleSpinBoxBaselineStart.setValue(tfr.times[0])
            self.ui.doubleSpinBoxBaselineEnd.setMinimum(tfr.times[0])
            self.ui.doubleSpinBoxBaselineEnd.setMaximum(tfr.times[-1])

    def on_pushButtonBrowseLayout_clicked(self, checked=None):
        """
        Opens a dialog for selecting a layout file.
        """
        if checked is None:
            return
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
        cmap = self.ui.comboBoxCmap.currentText()
        if self.ui.radioButtonSelectLayout.isChecked():
            layout = self.ui.comboBoxLayout.currentText()
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
        if layout == 'No layout selected' or layout == '':
            self.messageBox = shortMessageBox('No layout selected')
            self.messageBox.show()
            return
        if self.ui.groupBoxBaseline.isChecked():
            mode = self.ui.comboBoxMode.currentText()
            if self.ui.checkBoxBaselineStartNone.isChecked():
                blstart = None
            else:
                blstart = self.ui.doubleSpinBoxBaselineStart.value()

            if ( self.ui.checkBoxBaselineEndNone.isChecked() ):
                blend = None
            else:
                blend = self.ui.doubleSpinBoxBaselineEnd.value()
        else:
            blstart, blend, mode = None, None, None
        if self.ui.radioButtonInduced.isChecked():
            reptype = 'average'
        elif self.ui.radioButtonPhase.isChecked():
            reptype = 'itc'
        if self.tfr is not None:
            self.caller.TFR_topology(self.tfr, reptype, None, None, None, mode,
                                     blstart, blend, None, None, layout, None,
                                     None, cmap, parent_handle=self.parent)
            return

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles = self.ui.spinBoxNcycles.value()

        ch_type = str(self.ui.comboBoxChannels.currentText())

        epochs = self.caller.experiment.active_subject.get_epochs(self.
                                                                  epoch_name)
        epochs.name = self.epoch_name  # not stored in epochs when saved
        scalp = dict()
        if self.ui.groupBoxScalp.isChecked():
            scalp['tmin'] = self.ui.doubleSpinBoxScalpTmin.value()
            scalp['tmax'] = self.ui.doubleSpinBoxScalpTmax.value()
            scalp['fmin'] = self.ui.doubleSpinBoxScalpFmin.value()
            scalp['fmax'] = self.ui.doubleSpinBoxScalpFmax.value()
        else:
            scalp = None
        self.caller.TFR_topology(epochs, reptype, minfreq, maxfreq,
                                 decim, mode, blstart, blend, interval,
                                 ncycles, layout, ch_type, scalp, cmap,
                                 parent_handle=self.parent)
        self.parent.update_power_list()

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
        cmap = self.ui.comboBoxCmap.currentText()
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        ncycles = self.ui.spinBoxNcycles.value()
        if self.ui.groupBoxBaseline.isChecked():
            mode = self.ui.comboBoxMode.currentText()
            if self.ui.checkBoxBaselineStartNone.isChecked():
                blstart = None
            else:
                blstart = self.ui.doubleSpinBoxBaselineStart.value()

            if ( self.ui.checkBoxBaselineEndNone.isChecked() ):
                blend = None
            else:
                blend = self.ui.doubleSpinBoxBaselineEnd.value()
        else:
            blstart, blend, mode = None, None, None
        if self.ui.radioButtonInduced.isChecked(): 
            reptype = 'average'
        elif self.ui.radioButtonPhase.isChecked(): 
            reptype = 'itc'

        if saveMax:
            saveMax = reptype
        else:
            saveMax = None

        if self.ui.radioButtonSelectLayout.isChecked():
            layout = self.ui.comboBoxLayout.currentText()
        elif self.ui.radioButtonLayoutFromFile.isChecked():
            layout = str(self.ui.labelLayout.text())
        if layout == 'No layout selected' or layout == '':
            self.messageBox = shortMessageBox('No layout selected')
            self.messageBox.show()
            return

        self.caller.TFR_average(self.epoch_name, reptype, cmap, mode,
                                minfreq, maxfreq, interval, blstart,
                                blend, ncycles, decim, layout, channels,
                                form, dpi, saveTopo, savePlot, saveMax,
                                parent_handle=self.parent)
