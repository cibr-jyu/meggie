# coding: utf-8

"""
"""

import logging

import numpy as np

from PyQt5 import QtWidgets

from meggie.tabs.evoked.dialogs.createEvokedDialogUi import Ui_CreateEvokedDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.datatypes.evoked.evoked import Evoked

from meggie.utilities.decorators import threaded
from meggie.utilities.validators import validate_name
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class CreateEvokedDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, experiment, parent, selected_epochs, default_name):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateEvokedDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.selected_epochs = selected_epochs

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

        self.ui.lineEditName.setText(default_name)

    def experiment_getter(self):
        return self.experiment

    def create_evoked(self, subject, selected_epochs):

        time_arrays = []
        for name in selected_epochs:
            epochs = subject.epochs.get(name)
            if epochs:
                time_arrays.append(epochs.content.times)

        assert_arrays_same(time_arrays)

        evokeds = {}
        for name in selected_epochs:
            try:
                epochs = subject.epochs[name]
            except KeyError:
                raise KeyError('No epoch collection called ' + str(name))

            mne_epochs = epochs.content

            @threaded
            def average():
                return mne_epochs.average()

            mne_evoked = average(do_meanwhile=self.parent.update_ui)

            mne_evoked.comment = name
            evokeds[name] = mne_evoked

        evoked_name = validate_name(self.ui.lineEditName.text())

        params = {'conditions': selected_epochs}

        evoked_directory = subject.evoked_directory
        evoked = Evoked(evoked_name, evoked_directory, params, content=evokeds)
        evoked.save_content()
        subject.add(evoked, 'evoked')

    def accept(self):
        subject = self.experiment.active_subject
        selected_epochs = self.selected_epochs

        try:
            self.create_evoked(subject, selected_epochs)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.experiment.save_experiment_settings()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished.')

        self.close()


    def acceptBatch(self):
        selected_epochs = self.selected_epochs
        experiment = self.experiment

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.create_evoked(subject, selected_epochs)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception(str(exc))

        self.batching_widget.cleanup()
        self.experiment.save_experiment_settings()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished.')

        self.close()
