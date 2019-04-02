"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.ui.analysis.TFRPlotTopologyDialogUi import Ui_TFRPlotTopologyDialog

from meggie.code_meggie.analysis.spectral import plot_tfr

from meggie.ui.utils.messaging import exc_messagebox


class TFRPlotTopologyDialog(QtWidgets.QDialog):
    
    def __init__(self, parent, experiment, tfr_name):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_TFRPlotTopologyDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = experiment
        self.tfr_name = tfr_name

        active_subject = self.experiment.active_subject

        tfr = active_subject.tfrs[self.tfr_name].tfr

        start, end = tfr.times[0], tfr.times[-1]
        self.ui.doubleSpinBoxBaselineStart.setMinimum(start)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(end)
        self.ui.doubleSpinBoxBaselineStart.setValue(start)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(start)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(end)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)

    def accept(self):

        active_subject = self.experiment.active_subject

        tfr = active_subject.tfrs[self.tfr_name].tfr

        if self.ui.checkBoxBaselineCorrection.isChecked():
            blmode = self.ui.comboBoxBaselineMode.currentText()
        else:
            blmode = None

        if self.ui.radioButtonAllChannels.isChecked():
            output = 'all_channels'
        else:
            output = 'channel_averages'

        blstart = self.ui.doubleSpinBoxBaselineStart.value()
        blend = self.ui.doubleSpinBoxBaselineEnd.value()
   
        plot_tfr(self.experiment, tfr, self.tfr_name, 
                 blmode, blstart, blend, output)

        self.close()

