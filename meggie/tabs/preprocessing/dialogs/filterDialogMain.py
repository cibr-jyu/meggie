# coding: utf-8
"""
"""

import logging

from copy import deepcopy

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.ui.preprocessing.filterDialogUi import Ui_DialogFilter
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget

from meggie.code_meggie.preprocessing.filter import filter_data

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox


class FilterDialog(QtWidgets.QDialog):
    """
    Class containing the logic for filterDialog. It collects the parameters
    needed for filtering and shows the preview for the filter if required.
    """

    def __init__(self, parent, experiment):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogFilter()
        self.ui.setupUi(self)

        self.experiment = experiment

        self.filterParameterDictionary = None
        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.scrollAreaWidgetContents,
            geometry=self.ui.widget.geometry())

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
            message = 'Please select filter(s) to preview'
            messagebox(self.parent, message)
            return

        subject = self.experiment.active_subject
        info = subject.get_working_file().info

        # mne-python's filter_data takes filter_length in human-readable format
        params = deepcopy(params)
        params['length'] = params['length'] + 's'
        params['bandstop_length'] = params['bandstop_length'] + 's'

        try:
            raw = filter_data(self.experiment,
                              params,
                              subject,
                              preview=True,
                              do_meanwhile=self.parent.update_ui)
            raw.plot(block=True)
        except BaseException:
            pass

    def accept(self):
        """
        Get the parameters dictionary and relay it to filter_data to
        actually do the filtering.
        """
        subject = self.experiment.active_subject
        params = self.collect_parameter_values()
        if not params:
            message = 'Please select some filters first'
            messagebox(self.parent, message)
            return

        info = subject.get_working_file().info

        try:
            self.filter(subject, params)
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            logging.getLogger('ui_logger').exception(str(exc))

        self.parent.parent.initialize_ui()
        self.close()

    def acceptBatch(self):
        """
        """
        recently_active_subject = self.experiment.active_subject.subject_name

        subject_names = self.batching_widget.selected_subjects
        params = self.collect_parameter_values()
        if not params:
            message = 'Please select some filters first'
            messagebox(self.parent, message)
            return

        for name, subject in self.experiment.subjects.items():
            if name in subject_names:
                try:
                    self.experiment.activate_subject(name)
                    info = subject.get_working_file().info
                    self.filter(subject, params)
                except Exception as exc:
                    logging.getLogger('ui_logger').exception(str(exc))
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))

        self.experiment.activate_subject(recently_active_subject)
        self.batching_widget.cleanup()

        self.parent.parent.initialize_ui()
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
        """Calls filter_data for filtering the given
        subject and passes errors to accept method.

        Keyword arguments:
        subject               -- Subject object
        """
        # mne-python wants the lengths to be human-readable values
        params = deepcopy(params)
        params['length'] = params['length'] + 's'
        params['bandstop_length'] = params['bandstop_length'] + 's'

        filter_data(self.experiment,
                    params, subject,
                    do_meanwhile=self.parent.update_ui)
