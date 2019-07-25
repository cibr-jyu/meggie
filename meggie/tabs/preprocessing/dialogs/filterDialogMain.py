# coding: utf-8
"""
"""

import logging

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.tabs.preprocessing.dialogs.filterDialogUi import Ui_DialogFilter
from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget
from meggie.utilities.compare import compare_raws

from meggie.tabs.preprocessing.controller.filter import filter_data

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox


class FilterDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent, experiment):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_DialogFilter()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def on_pushButtonPreview_clicked(self, checked=None):
        """
        Draws the preview.
        """
        if checked is None:
            return

        params = self.collect_parameter_values()
        if not params:
            message = 'No filter(s) selected.'
            messagebox(self.parent, message)
            return

        subject = self.experiment.active_subject

        # mne-python's filter_data takes filter_length in human-readable format
        params = deepcopy(params)
        params['length'] = params['length'] + 's'
        params['bandstop_length'] = params['bandstop_length'] + 's'

        try:
            raw_to = filter_data(params,
                                 subject,
                                 preview=True,
                                 do_meanwhile=self.parent.update_ui)
            raw_from = subject.get_raw()
            compare_raws(raw_from, raw_to)
        except Exception as exc:
            exc_messagebox(self.parent, exc)

    def accept(self):
        """
        Get the parameters dictionary and relay it to filter_data to
        actually do the filtering.
        """
        subject = self.experiment.active_subject
        params = self.collect_parameter_values()
        if not params:
            message = 'No filter(s) selected'
            messagebox(self.parent, message)
            return

        try:
            self.filter(subject, params)
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            logging.getLogger('ui_logger').exception(str(exc))

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):
        """
        """
        subject_names = self.batching_widget.selected_subjects
        params = self.collect_parameter_values()
        if not params:
            message = 'No filter(s) selected'
            messagebox(self.parent, message)
            return

        for name, subject in self.experiment.subjects.items():
            if name in subject_names:
                try:
                    self.filter(subject, params)
                except Exception as exc:
                    logging.getLogger('ui_logger').exception(str(exc))
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))

        self.batching_widget.cleanup()

        self.parent.initialize_ui()
        self.close()

    def collect_parameter_values(self):
        """
        Gets the filtering parameters from the UI fields and performs
        rudimentary sanity checks on them.
        """
        is_empty = True
        dictionary = {}

        length = str(self.ui.doubleSpinBoxLength.value())
        dictionary['length'] = length

        dictionary['trans_bw'] = self.ui.doubleSpinBoxTransBandwidth.value()

        dictionary['lowpass'] = self.ui.checkBoxLowpass.isChecked()
        if dictionary['lowpass']:
            is_empty = False
            dictionary['low_cutoff_freq'] = \
                self.ui.doubleSpinBoxLowpassCutoff.value()

        dictionary['highpass'] = self.ui.checkBoxHighpass.isChecked()
        if dictionary['highpass']:
            is_empty = False
            dictionary['high_cutoff_freq'] = \
                self.ui.doubleSpinBoxHighpassCutoff.value()

        dictionary['bandstop1'] = self.ui.checkBoxBandstop.isChecked()
        if dictionary['bandstop1']:
            is_empty = False
            dictionary['bandstop1_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq.value()

        dictionary['bandstop2'] = self.ui.checkBoxBandstop2.isChecked()
        if dictionary['bandstop2']:
            is_empty = False
            dictionary['bandstop2_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq2.value()

        dictionary['bandstop_bw'] = self.ui.doubleSpinBoxBandstopWidth.value()
        dictionary['bandstop_transbw'] = self.ui.doubleSpinBoxNotchTransBw.value()  # noqa

        length = str(self.ui.doubleSpinBoxBandStopLength.value())
        dictionary['bandstop_length'] = length

        return dictionary

    def filter(self, subject, params):
        """
        """
        # mne-python wants the lengths to be human-readable values
        params = deepcopy(params)
        params['length'] = params['length'] + 's'
        params['bandstop_length'] = params['bandstop_length'] + 's'

        filter_data(params, subject,
                    do_meanwhile=self.parent.update_ui)
