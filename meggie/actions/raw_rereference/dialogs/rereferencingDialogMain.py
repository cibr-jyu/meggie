""" Contains a class for logic of the rereferencing dialog.
"""
import logging

import numpy as np
import mne

from PyQt5 import QtWidgets

from meggie.actions.raw_rereference.dialogs.rereferencingDialogUi import Ui_rereferencingDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget
from meggie.utilities.messaging import exc_messagebox


class RereferencingDialog(QtWidgets.QDialog):
    """ Contains logic for the rereferencing dialog.
    """
    def __init__(self, parent, experiment, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_rereferencingDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.parent = parent
        self.handler = handler

        subject = self.experiment.active_subject
        raw = subject.get_raw()
        sfreq = raw.info['sfreq']

        # fill the combobox
        picks = mne.pick_types(raw.info, eeg=True, meg=False, eog=True)
        ch_names = [ch_name for ch_idx, ch_name in
                    enumerate(raw.info['ch_names']) if ch_idx in picks]

        self.ui.listWidgetChannels.clear()
        for ch_name in ch_names:
            self.ui.listWidgetChannels.addItem(ch_name)

        self.batching_widget = BatchingWidget(
            experiment_getter=self._experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def _experiment_getter(self):
        return self.experiment

    def accept(self):
        experiment = self.experiment
        subject = experiment.active_subject

        if self.ui.radioButtonUseAverage.isChecked():
            selection = "average"
        else:
            selection = [
                item.text() for item in
                self.ui.listWidgetChannels.selectedItems()
            ]

        try:
            params = {'selection': selection}
            self.handler(subject, params)
            experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            return

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):
        experiment = self.experiment

        if self.ui.radioButtonUseAverage.isChecked():
            selection = "average"
        else:
            selection = [
                item.text() for item in
                self.ui.listWidgetChannels.selectedItems()
            ]

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    params = {'selection': selection}
                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        try:
            experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self.parent, exc)

        self.parent.initialize_ui()

        self.close()

