""" Handles the logic of simple reusable dialogs
"""

import logging

import numpy as np

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.simpleDialogUi import Ui_SimpleDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.validators import validate_name
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class SimpleDialog(QtWidgets.QDialog):
    """ Contains logic for simple reusable dialog.
    """

    def __init__(self, experiment, parent, default_name, handler, 
                 batching=True, title='Simple dialog'):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_SimpleDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment
        self.handler = handler

        self.setWindowTitle('Meggie - ' + title)

        if batching:
            self.batching_widget = BatchingWidget(
                experiment_getter=self._experiment_getter,
                parent=self,
                container=self.ui.groupBoxBatching,
                geometry=self.ui.batchingWidgetPlaceholder.geometry())
            self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)
        else:
            self.ui.groupBoxBatching.hide()
            self.ui.pushButtonBatch.hide()

        self.ui.lineEditName.setText(default_name)

    def _experiment_getter(self):
        return self.experiment

    def accept(self):
        subject = self.experiment.active_subject

        try:
            evoked_name = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self,  exc)
            return

        try:
            params = {'name': evoked_name}
            self.handler(subject, params)
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):

        experiment = self.experiment

        try:
            evoked_name = validate_name(self.ui.lineEditName.text())
        except Exception as exc:
            exc_messagebox(self,  exc)
            return

        selected_subject_names = self.batching_widget.selected_subjects

        params = {'name': evoked_name}

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        try:
            self.experiment.save_experiment_settings()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.initialize_ui()
        self.close()
