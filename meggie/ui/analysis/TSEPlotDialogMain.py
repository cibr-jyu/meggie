"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.ui.analysis.TSEPlotDialogUi import Ui_TSEPlotDialog

from meggie.code_meggie.analysis.spectral import plot_tse

from meggie.ui.utils.messaging import exc_messagebox


class TSEPlotDialog(QtWidgets.QDialog):
    
    def __init__(self, parent, experiment, tfr_name):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_TSEPlotDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = experiment
        self.tfr_name = tfr_name

        active_subject = self.experiment.active_subject

        meggie_tfr = active_subject.tfrs[self.tfr_name]

        tfr = list(meggie_tfr.tfrs.values())[0]

        minfreq = tfr.freqs[0]
        maxfreq = tfr.freqs[-1]

        self.ui.doubleSpinBoxMinFreq.setValue(minfreq)
        self.ui.doubleSpinBoxMaxFreq.setValue(maxfreq)


    def accept(self):

        if self.ui.radioButtonAllChannels.isChecked():
            output = 'all_channels'
        else:
            output = 'channel_averages'

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()

        plot_tse(self.experiment, self.tfr_name, minfreq, maxfreq, output)
   
        self.close()

