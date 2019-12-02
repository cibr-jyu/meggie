# coding: utf-8

"""
"""
import logging

import numpy as np

from PyQt5 import QtWidgets

from meggie.tabs.tfr.controller.tfr import create_tfr

from meggie.tabs.tfr.dialogs.TFRDialogUi import Ui_TFRDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.validators import validate_name
from meggie.utilities.decorators import threaded
from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox


class TFRDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, experiment, parent, epoch_names):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_TFRDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.epoch_names = epoch_names
        self.experiment = experiment

        subject = experiment.active_subject
        epochs = subject.epochs[epoch_names[0]].content

        self.ui.lineEditEpochName.setText(', '.join(epoch_names))

        if epochs.info.get('highpass'):
            self.ui.doubleSpinBoxMinFreq.setValue(
                max(int(np.ceil(epochs.info['highpass'])),
                    self.ui.doubleSpinBoxMinFreq.value()))

        if epochs.info.get('lowpass'):
            self.ui.doubleSpinBoxMaxFreq.setValue(
                min(int(np.floor(epochs.info['lowpass'])),
                    self.ui.doubleSpinBoxMaxFreq.value()))

        epoch_length = epochs.times[-1] - epochs.times[0]

        # try to use as many cycles as possible
        # (window ~= 10 * (n_cycles / (2.0 * np.pi * freq))
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        n_cycles = epoch_length * 2.0 * np.pi * minfreq / 10.0
        n_cycles = max(np.floor(n_cycles), 1)

        self.ui.doubleSpinBoxNcycles.setValue(n_cycles)

        # select factor such that minfreq / factor = n_cycles,
        # and then ceil
        factor = np.ceil(minfreq / float(n_cycles))
        self.ui.doubleSpinBoxCycleFactor.setValue(factor)

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def accept(self):
        """
        """

        tfr_name = self.ui.lineEditTFRName.text()

        try:
            validate_name(tfr_name)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        freqs = np.arange(minfreq, maxfreq, interval)

        subtract_evoked = self.ui.checkBoxSubtractEvoked.isChecked()

        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()

        experiment = self.experiment
        subject = experiment.active_subject

        try:
            create_tfr(subject, tfr_name, self.epoch_names,
                       freqs=freqs, decim=decim, ncycles=ncycles,
                       subtract_evoked=subtract_evoked,
                       do_meanwhile=self.parent.update_ui)

        except Exception as exc:
            exc_messagebox(self.parent, exc)
            return

        experiment.save_experiment_settings()
        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):

        tfr_name = self.ui.lineEditTFRName.text()

        try:
            validate_name(tfr_name)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        freqs = np.arange(minfreq, maxfreq, interval)

        subtract_evoked = self.ui.checkBoxSubtractEvoked.isChecked()

        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()

        selected_subject_names = self.batching_widget.selected_subjects
        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    create_tfr(subject, tfr_name,
                               self.epoch_names, freqs=freqs,
                               decim=decim, ncycles=ncycles,
                               subtract_evoked=subtract_evoked,
                               do_meanwhile=self.parent.update_ui)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception(str(exc))

        self.batching_widget.cleanup()
        experiment.save_experiment_settings()
        self.parent.initialize_ui()
        self.close()
