# coding: utf-8

"""
"""

import logging

from copy import deepcopy

from PyQt5 import QtWidgets

import numpy as np

from meggie.tabs.epochs.dialogs.createEpochsFromEventsDialogUi import Ui_CreateEpochsFromEventsDialog

from meggie.tabs.epochs.controller.epoching import create_epochs_from_events

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget
from meggie.utilities.dialogs.bitSelectionDialogMain import BitSelectionDialog

from meggie.utilities.decorators import threaded
from meggie.utilities.validators import validate_name
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class CreateEpochsFromEventsDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, experiment, parent):
        """Initialize the event selection dialog.

        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateEpochsFromEventsDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.events = []

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def update_events(self):
        """ update event list on UI based on self.events
        """
        self.ui.listWidgetEvents.clear()

        events = self.events

        for event in events:
            item = QtWidgets.QListWidgetItem(
                '%s, %s' % (
                    'ID ' + str(event['event_id']),
                    'mask=' + str(event['mask'])
                ))
            self.ui.listWidgetEvents.addItem(item)

    def collect_parameter_values(self):
        """Collect the parameter values for epoch creation from the ui.
        """
        tmin = float(self.ui.doubleSpinBoxTmin.value())
        tmax = float(self.ui.doubleSpinBoxTmax.value())
        bstart = float(self.ui.doubleSpinBoxBaselineStart.value())
        bend = float(self.ui.doubleSpinBoxBaselineEnd.value())

        mag = self.ui.checkBoxMag.isChecked()
        grad = self.ui.checkBoxGrad.isChecked()
        eeg = self.ui.checkBoxEeg.isChecked()

        collection_name = validate_name(
            str(self.ui.lineEditCollectionName.text()))

        reject = dict()
        if mag:
            reject['mag'] = self.ui.doubleSpinBoxMagReject.value()
        if grad:
            reject['grad'] = self.ui.doubleSpinBoxGradReject.value()
        if eeg:
            reject['eeg'] = self.ui.doubleSpinBoxEEGReject.value()

        params = {'mag': mag, 'grad': grad, 'eeg': eeg,
                  'reject': reject,
                  'tmin': float(tmin), 'tmax': float(tmax),
                  'bstart': float(bstart), 'bend': float(bend),
                  'collection_name': collection_name,
                  'events': self.events}
        return params

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        event_params = {
            'mask': self.ui.spinBoxMask.value(),
            'event_id': self.ui.spinBoxEventID.value(),
        }

        if event_params not in self.events:
            self.events.append(event_params)
            self.update_events()

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return

        self.events = []
        self.update_events()

    def accept(self):
        """
        """
        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            messagebox(self.parent, message)
            return

        try:
            params = self.collect_parameter_values()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        subject = self.experiment.active_subject

        if params['collection_name'] in subject.epochs:
            message = 'Epoch collection with the name exists.'
            messagebox(self.parent, message)
            return

        try:
            self.calculate_epochs(subject, params)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.experiment.save_experiment_settings()
        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):
        """
        """
        experiment = self.experiment

        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            messagebox(self.parent, message)
            return

        try:
            params = self.collect_parameter_values()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        selected_subject_names = self.batching_widget.selected_subjects
        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    self.calculate_epochs(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append((subject,
                                                                 str(exc)))
                    logging.getLogger('ui_logger').error(
                        'Params: ' + str(params))
                    logging.getLogger('ui_logger').exception(str(exc))

        self.batching_widget.cleanup()
        self.experiment.save_experiment_settings()
        self.parent.initialize_ui()
        self.close()

    def on_pushButtonEdit_clicked(self, checked=None):
        if checked is None:
            return

        self.bitDialog = BitSelectionDialog(self,
                                            self.ui.spinBoxMask, self.ui.spinBoxEventID)

        self.bitDialog.show()

    def on_pushButtonHelp_clicked(self, checked=None):
        if checked is None:
            return

        help_message = (
            "Events are found in a following way. If only event "
            "id is set, events with exactly the same binary representation as "
            "event id are included in the final event list. If also mask is "
            "set, event list will also include events where binary digits in "
            "the places specified by the mask are not the same as in the "
            "event id, or in other words, only events where the digits we "
            "are interested in are the same as in the list of all events, "
            "are included. Binary representations are assumed to be 16 digits "
            "long. \n\nFor example event id of 0000010000010000 = 1040 and "
            "mask of 0000000000000011 = 3 would mean that first (rightmost) "
            "two digits can be 1 or 0, but anything else must be exactly as "
            "in the event id. Thus events with following id's would be allowed:"
            "\n\n0000010000010000 = 1040\n0000010000010001 = 1041\n"
            "0000010000010010 = 1042\n0000010000010011 = 1043")

        messagebox(self.parent, help_message, 'Mask help')

    def calculate_epochs(self, subject, params):
        experiment = self.experiment

        @threaded
        def create(*args, **kwargs):
            create_epochs_from_events(params, subject)

        create(do_meanwhile=self.parent.update_ui)
