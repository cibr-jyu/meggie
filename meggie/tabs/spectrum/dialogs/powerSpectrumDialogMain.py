"""
"""

import logging

from collections import OrderedDict

from PyQt5 import QtWidgets

import numpy as np

from meggie.ui.analysis.powerSpectrumDialogUi import Ui_PowerSpectrumDialog
from meggie.ui.analysis.powerSpectrumEventsDialogMain import PowerSpectrumEvents

from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

from meggie.tabs.spectrum.controller.spectral import create_power_spectrum

from meggie.code_meggie.utils.validators import validate_name
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox


class PowerSpectrumDialog(QtWidgets.QDialog):

    def __init__(self, experiment, parent):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_PowerSpectrumDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.intervals = []

        raw = self.experiment.active_subject.get_raw()

        tmax = np.floor(raw.times[raw.n_times - 1]) - 0.1
        self.ui.doubleSpinBoxTmin.setValue(0)
        self.ui.doubleSpinBoxTmax.setValue(tmax)
        self.ui.doubleSpinBoxTmin.setMaximum(tmax)
        self.ui.doubleSpinBoxTmax.setMaximum(tmax)

        # set nfft initially to ~2 seconds and overlap to ~1 seconds
        sfreq = raw.info['sfreq']
        window_in_seconds = 2
        nfft = int(
            np.power(2, np.ceil(np.log(sfreq * window_in_seconds) / np.log(2))))
        overlap = nfft / 2

        self.ui.spinBoxNfft.setValue(nfft)
        self.ui.spinBoxOverlap.setValue(overlap)

        if raw.info.get('highpass'):
            if self.ui.spinBoxFmin.value() < raw.info['highpass']:
                self.ui.spinBoxFmin.setValue(
                    int(np.ceil(raw.info['highpass'])))

        if raw.info.get('lowpass'):
            if self.ui.spinBoxFmax.value() > raw.info['lowpass']:
                self.ui.spinBoxFmax.setValue(int(raw.info['lowpass']))

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return
        group = int(self.ui.comboBoxAvgGroup.currentText())
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        if tmin >= tmax:
            messagebox(
                self.parent, "End time must be higher than the starting time")
            return

        self.add_intervals([(group, tmin, tmax)])

    def add_intervals(self, intervals):
        for interval in intervals:
            self.intervals.append(interval)
            item = QtWidgets.QListWidgetItem(
                '%s: %s - %s s' % (
                    interval[0],
                    round(interval[1], 4),
                    round(interval[2], 4)
                ))
            self.ui.listWidgetIntervals.addItem(item)

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return
        self.intervals = []
        self.ui.listWidgetIntervals.clear()

    def on_pushButtonClearRow_clicked(self, checked=None):
        if checked is None:
            return
        current_row = self.ui.listWidgetIntervals.currentRow()
        self.ui.listWidgetIntervals.takeItem(current_row)
        self.intervals.pop(current_row)

    def on_pushButtonAddEvents_clicked(self, checked=None):
        if checked is None:
            return
        self.event_dialog = PowerSpectrumEvents(self)
        self.event_dialog.show()

    def validate_settings(self, name, times, fmin, fmax, sfreq):
        if not times:
            raise Exception("Must have at least one interval")

        if fmin >= fmax:
            raise Exception(
                "End frequency must be higher than the starting frequency")

        valid = True
        for interval in times:
            if (interval[2] - interval[1]) * \
                    sfreq < float(self.ui.spinBoxNfft.value()):
                valid = False

        if not valid:
            raise Exception("Sampling rate times shortest interval "
                            "should be more than window size")

    def accept(self, *args, **kwargs):
        """Starts the computation."""

        try:
            name = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        times = self.intervals
        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()

        experiment = self.experiment

        subject = experiment.active_subject
        sfreq = subject.get_working_file().info['sfreq']

        try:
            self.validate_settings(name, times, fmin, fmax, sfreq)
        except Exception as exc:
            messagebox(self.parent, str(exc))
            return

        params = dict()
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['log'] = self.ui.checkBoxLogarithm.isChecked()
        params['overlap'] = self.ui.spinBoxOverlap.value()

        raw = subject.get_working_file()

        try:
            raw_blocks = OrderedDict()
            for interval in times:

                block = raw.copy().crop(tmin=interval[1], tmax=interval[2])

                if interval[0] not in raw_blocks:
                    raw_blocks[interval[0]] = []

                raw_blocks[interval[0]].append(block)

            update_ui = self.parent.update_ui
            create_power_spectrum(experiment, name, params, raw_blocks,
                                  update_ui=update_ui)
        except Exception as e:
            exc_messagebox(self.parent, e)
            return

        experiment.save_experiment_settings()
        self.parent.initialize_ui()

        self.close()

    def acceptBatch(self, *args):

        try:
            name = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        times = self.intervals
        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()

        experiment = self.experiment

        subject = experiment.active_subject
        sfreq = subject.get_working_file().info['sfreq']

        try:
            self.validate_settings(name, times, fmin, fmax, sfreq)
        except Exception as exc:
            messagebox(self.parent, str(exc))
            return

        params = dict()
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['log'] = self.ui.checkBoxLogarithm.isChecked()
        params['overlap'] = self.ui.spinBoxOverlap.value()

        selected_subject_names = self.batching_widget.selected_subjects
        recently_active_subject = experiment.active_subject.subject_name

        for subject_name, subject in self.experiment.subjects.items():
            if subject_name in selected_subject_names:
                try:
                    experiment.activate_subject(subject_name)
                    raw = subject.get_working_file()

                    raw_blocks = OrderedDict()
                    for interval in times:

                        block = raw.copy().crop(
                            tmin=interval[1], tmax=interval[2])

                        if interval[0] not in raw_blocks:
                            raw_blocks[interval[0]] = []

                        raw_blocks[interval[0]].append(block)

                    update_ui = self.parent.update_ui
                    create_power_spectrum(experiment, name, params, raw_blocks,
                                          update_ui=update_ui)
                except Exception as e:
                    self.batching_widget.failed_subjects.append((subject,
                                                                 str(e)))
                    logging.getLogger('ui_logger').exception(str(e))

        experiment.activate_subject(recently_active_subject)

        self.batching_widget.cleanup()
        experiment.save_experiment_settings()

        self.parent.initialize_ui()
        self.close()
