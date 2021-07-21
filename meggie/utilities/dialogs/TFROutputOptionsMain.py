""" Contains a class for the tfr output options dialog.
"""
from PyQt5 import QtWidgets

from meggie.utilities.dialogs.TFROutputOptionsUi import Ui_TFROutputOptions


class TFROutputOptions(QtWidgets.QDialog):
    """ Contains logic for the tfr output options dialog.
    """

    def __init__(self, parent, experiment, tfr_name, handler, ask_condition=False):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_TFROutputOptions()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = experiment
        self.handler = handler
        self.ask_condition = ask_condition

        if not ask_condition:
            self.ui.groupBoxCondition.hide()

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
        self.ui.doubleSpinBoxTimeStart.setMinimum(start)
        self.ui.doubleSpinBoxTimeStart.setMaximum(end)
        self.ui.doubleSpinBoxTimeEnd.setMinimum(start)
        self.ui.doubleSpinBoxTimeEnd.setMaximum(end)
        self.ui.doubleSpinBoxFrequencyMin.setMinimum(minfreq)
        self.ui.doubleSpinBoxFrequencyMax.setMaximum(maxfreq)
        self.ui.doubleSpinBoxFrequencyMin.setMinimum(minfreq)
        self.ui.doubleSpinBoxFrequencyMax.setMaximum(maxfreq)
 
        self.ui.doubleSpinBoxBaselineStart.setValue(start)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)
        self.ui.doubleSpinBoxTimeStart.setValue(start)
        self.ui.doubleSpinBoxTimeEnd.setValue(end)
        self.ui.doubleSpinBoxFrequencyMin.setValue(minfreq)
        self.ui.doubleSpinBoxFrequencyMax.setValue(maxfreq)

        for key in keys:
            self.ui.comboBoxCondition.addItem(key)

        if len(keys) == 1:
            self.ui.comboBoxCondition.setEnabled(False)

    def accept(self):
        subject = self.experiment.active_subject

        if self.ask_condition:
            condition = self.ui.comboBoxCondition.currentText()
        else:
            condition = None

        if self.ui.checkBoxBaselineCorrection.isChecked():
            blmode = self.ui.comboBoxBaselineMode.currentText()
        else:
            blmode = None

        blstart = self.ui.doubleSpinBoxBaselineStart.value()
        blend = self.ui.doubleSpinBoxBaselineEnd.value()
        tmin = self.ui.doubleSpinBoxTimeStart.value()
        tmax = self.ui.doubleSpinBoxTimeEnd.value()
        fmin = self.ui.doubleSpinBoxFrequencyMin.value()
        fmax = self.ui.doubleSpinBoxFrequencyMax.value()

        if self.ui.radioButtonAllChannels.isChecked():
            output = 'all_channels'
        else:
            output = 'channel_averages'

        params = {}
        params['output_option'] = output
        params['condition'] = condition
        params['blmode'] = blmode
        params['blstart'] = blstart
        params['blend'] = blend
        params['tmin'] = tmin
        params['tmax'] = tmax
        params['fmin'] = fmin
        params['fmax'] = fmax

        self.handler(params)

        self.close()
