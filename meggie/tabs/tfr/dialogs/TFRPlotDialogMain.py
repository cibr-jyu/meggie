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
        self.ui.doubleSpinBoxBaselineStart.setMinimum(start)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(end)
        self.ui.doubleSpinBoxBaselineStart.setValue(start)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(start)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(end)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)

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

        if self.ui.radioButtonAllChannels.isChecked():
            plot_tfr_topo(self.experiment, subject, self.tfr_name,
                          condition, blmode, blstart, blend)
        else:
            plot_tfr_averages(self.experiment, subject, self.tfr_name,
                              condition, blmode, blstart, blend)

        self.close()
