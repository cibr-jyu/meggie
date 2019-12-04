"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.tfr.dialogs.TFRPlotDialogUi import Ui_TFRPlotDialog

from meggie.tabs.tfr.controller.tfr import plot_tfr_topo
from meggie.tabs.tfr.controller.tfr import plot_tfr_averages

from meggie.utilities.messaging import exc_messagebox


class TFRPlotDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment, tfr_name):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_TFRPlotDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = experiment
        self.tfr_name = tfr_name

        active_subject = self.experiment.active_subject

        meggie_tfr = active_subject.tfr[tfr_name]

        tfr = list(meggie_tfr.content.values())[0]
        keys = list(meggie_tfr.content.keys())

        start, end = tfr.times[0], tfr.times[-1]
        minfreq, maxfreq = tfr.freqs[0], tfr.freqs[-1]

        self.ui.doubleSpinBoxBaselineStart.setMinimum(start)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(end)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(start)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(end)
        self.ui.doubleSpinBoxCropStart.setMinimum(start)
        self.ui.doubleSpinBoxCropStart.setMaximum(end)
        self.ui.doubleSpinBoxCropEnd.setMinimum(start)
        self.ui.doubleSpinBoxCropEnd.setMaximum(end)
        self.ui.doubleSpinBoxCropMinFreq.setMinimum(minfreq)
        self.ui.doubleSpinBoxCropMinFreq.setMaximum(maxfreq)
        self.ui.doubleSpinBoxCropMaxFreq.setMinimum(minfreq)
        self.ui.doubleSpinBoxCropMaxFreq.setMaximum(maxfreq)
 
        self.ui.doubleSpinBoxBaselineStart.setValue(start)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)
        self.ui.doubleSpinBoxCropStart.setValue(start)
        self.ui.doubleSpinBoxCropEnd.setValue(end)
        self.ui.doubleSpinBoxCropMinFreq.setValue(minfreq)
        self.ui.doubleSpinBoxCropMaxFreq.setValue(maxfreq)

        for key in keys:
            self.ui.comboBoxCondition.addItem(key)

        if len(keys) == 1:
            self.ui.comboBoxCondition.setEnabled(False)

    def accept(self):

        subject = self.experiment.active_subject
        condition = self.ui.comboBoxCondition.currentText()

        if self.ui.checkBoxBaselineCorrection.isChecked():
            blmode = self.ui.comboBoxBaselineMode.currentText()
        else:
            blmode = None

        blstart = self.ui.doubleSpinBoxBaselineStart.value()
        blend = self.ui.doubleSpinBoxBaselineEnd.value()
        crop_start = self.ui.doubleSpinBoxCropStart.value()
        crop_end = self.ui.doubleSpinBoxCropEnd.value()
        crop_minfreq = self.ui.doubleSpinBoxCropMinFreq.value()
        crop_maxfreq = self.ui.doubleSpinBoxCropMaxFreq.value()

        if self.ui.radioButtonAllChannels.isChecked():
            plot_tfr_topo(self.experiment, subject, self.tfr_name,
                          condition, blmode, blstart, blend, 
                          crop_start, crop_end, crop_minfreq, crop_maxfreq)
        else:
            plot_tfr_averages(self.experiment, subject, self.tfr_name,
                              condition, blmode, blstart, blend,
                              crop_start, crop_end, crop_minfreq, crop_maxfreq)

        self.close()
