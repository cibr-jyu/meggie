""" Contains a class for logic of the power spectrum creation dialog.
"""

import logging

from collections import OrderedDict

from PyQt5 import QtWidgets

import numpy as np

from meggie.utilities.dialogs.powerSpectrumDialogUi import Ui_PowerSpectrumDialog
from meggie.utilities.dialogs.powerSpectrumAddAdvancedDialogMain import PowerSpectrumAddAdvancedDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.validators import validate_name
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class PowerSpectrumDialog(QtWidgets.QDialog):
    """ Contains logic for the power spectrum creation dialog.
    """
    def __init__(self, experiment, parent, default_name, handler=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_PowerSpectrumDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.handler = handler

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
        overlap = int(nfft / 2)

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
            experiment_getter=self._experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

        self.ui.lineEditName.setText(default_name)

    def _experiment_getter(self):
        return self.experiment

    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return
        group = str(self.ui.comboBoxAvgGroup.currentText())
        tmin = self.ui.doubleSpinBoxTmin.value()
        tmax = self.ui.doubleSpinBoxTmax.value()
        if tmin >= tmax:
            messagebox(
                self.parent, "End time must be higher than the starting time")
            return

        self.add_intervals([('fixed', (group, tmin, tmax))])

    def add_intervals(self, intervals):
        """ Add intervals to the interval list.
        """
        for ival_type, interval in intervals:
            self.intervals.append((ival_type, interval))
            if ival_type == 'fixed':
                item = QtWidgets.QListWidgetItem(
                    '%s: %s - %s s (fixed)' % (
                        interval[0],
                        round(interval[1], 4),
                        round(interval[2], 4)
                    ))
            else:
                item_string = str(interval[0]) + ': ['
                if interval[1][0] == 'events':
                    item_string += ', '.join([str(elem)
                                              for elem in interval[1][1:]])
                elif interval[1][0] == 'start':
                    item_string += 'start, ' + str(interval[1][3])
                elif interval[1][0] == 'end':
                    item_string += 'end, ' + str(interval[1][3])

                item_string += '] – ['

                if interval[2][0] == 'events':
                    item_string += ', '.join([str(elem)
                                              for elem in interval[2][1:]])
                elif interval[2][0] == 'start':
                    item_string += 'start, ' + str(interval[2][3])

                elif interval[2][0] == 'end':
                    item_string += 'end, ' + str(interval[2][3])

                item_string += '] (dynamic)'

                item = QtWidgets.QListWidgetItem(
                    item_string)
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
        if current_row == -1:
            return

        self.ui.listWidgetIntervals.takeItem(current_row)
        self.intervals.pop(current_row)

    def on_pushButtonAddAdvanced_clicked(self, checked=None):
        if checked is None:
            return
        dialog = PowerSpectrumAddAdvancedDialog(self)
        dialog.show()

    def accept(self, *args, **kwargs):
        try:
            spectrum_name = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        intervals = self.intervals
        if not intervals:
            return

        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()

        subject = self.experiment.active_subject

        params = dict()
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['overlap'] = self.ui.spinBoxOverlap.value()
        params['intervals'] = intervals
        params['name'] = spectrum_name

        try:
            self.handler(subject, params)
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self, *args):
        try:
            spectrum_name = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        intervals = self.intervals
        if not intervals:
            return

        fmin = self.ui.spinBoxFmin.value()
        fmax = self.ui.spinBoxFmax.value()

        subject = self.experiment.active_subject

        params = dict()
        params['fmin'] = fmin
        params['fmax'] = fmax
        params['nfft'] = self.ui.spinBoxNfft.value()
        params['overlap'] = self.ui.spinBoxOverlap.value()
        params['intervals'] = intervals
        params['name'] = spectrum_name

        selected_subject_names = self.batching_widget.selected_subjects
        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append((subject,
                                                                 str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        try:
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.initialize_ui()
        self.close()
