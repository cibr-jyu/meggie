"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.tfr.dialogs.TSEPlotDialogUi import Ui_TSEPlotDialog

from meggie.tabs.tfr.controller.tfr import plot_tse_topo
from meggie.tabs.tfr.controller.tfr import plot_tse_averages

from meggie.utilities.messaging import exc_messagebox


class TSEPlotDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment, tfr_name):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_TSEPlotDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = experiment
        self.tfr_name = tfr_name

        active_subject = self.experiment.active_subject

        meggie_tfr = active_subject.tfr[self.tfr_name]

        tfr = list(meggie_tfr.content.values())[0]

        minfreq, maxfreq = tfr.freqs[0], tfr.freqs[-1]
        tmin, tmax = tfr.times[0], tfr.times[-1]

        self.ui.doubleSpinBoxBaselineStart.setMinimum(tmin)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(tmax)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(tmax)
        self.ui.doubleSpinBoxAveMinFreq.setMinimum(minfreq)
        self.ui.doubleSpinBoxAveMinFreq.setMaximum(maxfreq)
        self.ui.doubleSpinBoxAveMaxFreq.setMinimum(minfreq)
        self.ui.doubleSpinBoxAveMaxFreq.setMaximum(maxfreq)
        self.ui.doubleSpinBoxCropStart.setMinimum(tmin)
        self.ui.doubleSpinBoxCropStart.setMaximum(tmax)
        self.ui.doubleSpinBoxCropEnd.setMinimum(tmin)
        self.ui.doubleSpinBoxCropEnd.setMaximum(tmax)
 
        self.ui.doubleSpinBoxBaselineStart.setValue(tmin)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)
        self.ui.doubleSpinBoxAveMinFreq.setValue(minfreq)
        self.ui.doubleSpinBoxAveMaxFreq.setValue(maxfreq)
        self.ui.doubleSpinBoxCropStart.setValue(tmin)
        self.ui.doubleSpinBoxCropEnd.setValue(tmax)

    def accept(self):

        subject = self.experiment.active_subject

        minfreq = self.ui.doubleSpinBoxAveMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxAveMaxFreq.value()

        bstart = self.ui.doubleSpinBoxBaselineStart.value()
        bend = self.ui.doubleSpinBoxBaselineEnd.value()

        crop_start = self.ui.doubleSpinBoxCropStart.value()
        crop_end = self.ui.doubleSpinBoxCropEnd.value()

        baseline = (bstart, bend)

        if self.ui.radioButtonAllChannels.isChecked():
            plot_tse_topo(self.experiment, subject, self.tfr_name, 
                          minfreq, maxfreq, baseline,
                          crop_start, crop_end)
        else:
            plot_tse_averages(self.experiment, subject, self.tfr_name, 
                              minfreq, maxfreq, baseline,
                              crop_start, crop_end)

        self.close()

