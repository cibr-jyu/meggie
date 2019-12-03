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

        minfreq = tfr.freqs[0]
        maxfreq = tfr.freqs[-1]

        tmin = tfr.times[0]

        self.ui.doubleSpinBoxMinFreq.setValue(minfreq)
        self.ui.doubleSpinBoxMaxFreq.setValue(maxfreq)

        self.ui.doubleSpinBoxBaselineStart.setValue(tmin)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)

    def accept(self):

        subject = self.experiment.active_subject

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()

        bstart = self.ui.doubleSpinBoxBaselineStart.value()
        bend = self.ui.doubleSpinBoxBaselineEnd.value()

        baseline = (bstart, bend)

        if self.ui.radioButtonAllChannels.isChecked():
            plot_tse_topo(self.experiment, subject, self.tfr_name, 
                          minfreq, maxfreq, baseline)
        else:
            plot_tse_averages(self.experiment, subject, self.tfr_name, 
                              minfreq, maxfreq, baseline)

        self.close()

