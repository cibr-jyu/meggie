# coding: utf-8

"""
"""

import numpy as np
import logging
import traceback

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from copy import deepcopy

from meggie.code_meggie.structures.events import Events
from meggie.code_meggie.general import fileManager

from meggie.code_meggie.analysis.epoching import create_epochs

from meggie.ui.utils.decorators import threaded
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.epoching.eventSelectionDialogUi import Ui_EventSelectionDialog
from meggie.ui.epoching.fixedLengthEpochDialogMain import FixedLengthEpochDialog
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget
from meggie.ui.epoching.bitSelectionDialogMain import BitSelectionDialog

from meggie.code_meggie.utils.units import get_scaling
from meggie.code_meggie.utils.validators import validate_name

class EventSelectionDialog(QtWidgets.QDialog):
    """
    Class containing the logic for EventSelectionDialog. It is used for
    collecting desired events from continuous data.
    """

    def __init__(self, parent, experiment):
        """Initialize the event selection dialog.

        Keyword arguments:

        parent -- Set the parent of this dialog
        params -- A dictionary containing parameter values to fill the
                  the different fields in the dialog with.
        """
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.experiment = experiment
        self.ui = Ui_EventSelectionDialog()
        self.ui.setupUi(self)
        self.used_names = []
        
        self.event_data = {
            'events': [],
            'fixed_length_events': []
        }
        
        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter, 
            parent=self, 
            container=self.ui.scrollAreaWidgetContents,
            geometry=self.ui.widgetBatchContainer.geometry())


    def experiment_getter(self):
        return self.experiment

    def update_events(self):
        """Add a list of events or a single event to the ui's eventlist.
        """
        self.ui.listWidgetEvents.clear()
 
        event_data = self.event_data
        
        if 'events' in event_data:
            events = event_data['events']
            for event in events:
                item = QtWidgets.QListWidgetItem(
                    '%s, %s' % (
                    'ID ' + str(event['event_id']),
                    'mask=' + str(event['mask'])
                ))
                self.ui.listWidgetEvents.addItem(item)
 
        if 'fixed_length_events' in event_data:
            fixed_length_events = event_data['fixed_length_events']
            for idx, event in enumerate(fixed_length_events):
                item = QtWidgets.QListWidgetItem(
                    '%s, %s, %s, %s' % (
                    'Fixed ' + str(idx + 1),
                    'start=' + str(event['tmin']), 
                    'end=' + str(event['tmax']),
                    'interval=' + str(event['interval'])
                ))
                self.ui.listWidgetEvents.addItem(item)

    def collect_parameter_values(self):
        """Collect the parameter values for epoch creation from the ui.

        Collect the parameter values for epoch creation from the ui and return
        them in a dictionary.
        """
        tmin = float(self.ui.doubleSpinBoxTmin.value())
        tmax = float(self.ui.doubleSpinBoxTmax.value())
        bstart = float(self.ui.doubleSpinBoxBaselineStart.value())
        bend = float(self.ui.doubleSpinBoxBaselineEnd.value())

        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked

        collection_name = validate_name(
            str(self.ui.lineEditCollectionName.text()))

        reject = dict()
        if mag:
            value = self.ui.doubleSpinBoxMagReject_3.value()
            if value != -1:
                reject['mag'] = value
        if grad:
            value = self.ui.doubleSpinBoxGradReject_3.value()
            if value != -1:
                reject['grad'] = value
        if eeg:
            value = self.ui.doubleSpinBoxEEGReject_3.value()
            if value != -1:
                reject['eeg'] = value
        if eog:
            value = self.ui.doubleSpinBoxEOGReject_3.value()
            if value != -1:
                reject['eog'] = value

        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        else: 
            meg = False

        subject = self.experiment.active_subject

        info = subject.get_working_file(preload=False).info

        events = deepcopy(self.event_data['events'])
        fle = deepcopy(self.event_data['fixed_length_events'])
        
        param_dict = {'mag' : mag, 'grad' : grad,
                      'eeg' : eeg, 'eog' : eog,
                      'reject' : reject, 
                      'tmin' : float(tmin), 'tmax' : float(tmax), 
                      'bstart' : float(bstart), 'bend' : float(bend), 
                      'collection_name' : collection_name,
                      'events' : events, 'fixed_length_events' : fle}
        return param_dict

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Method for adding events to the event list.
        """
        if checked is None:
            return

        event_params = {
            'mask': int(self.ui.lineEditMask.text()),
            'event_id': self.ui.spinBoxEventID.value(),
        }
        
        if event_params not in self.event_data['events']:
            self.event_data['events'].append(event_params)
            self.update_events()

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return
        
        self.ui.listWidgetEvents.clear()
        self.event_data['events'] = []
        self.event_data['fixed_length_events'] = []
        
    def accept(self):
        """
        """
        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            messagebox(self.parent, message)
            return

        try:
            param_dict = self.collect_parameter_values()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        epochs = self.experiment.active_subject.epochs
        if param_dict['collection_name'] in epochs:
            header = 'Epoch collection name exists. '
            message = ''.join([
                'Are you sure you want to overwrite the ',
                'collection?'
            ])
            reply = QtWidgets.QMessageBox.question(self.parent, header, message,                      QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

            if reply == QtWidgets.QMessageBox.No:
                return

        subject_name = self.experiment.active_subject.subject_name
        
        try:
            self.calculate_epochs(self.experiment.active_subject, param_dict)
        except Exception as e:
            messagebox(self.parent, 'Calculation failed: ' + str(e))
            logging.getLogger('ui_logger').error('Params: ' + str(param_dict))
            logging.getLogger('ui_logger').exception(str(e))
            return
        
        self.experiment.save_experiment_settings()

        # reinitialize main window as epochs are shown in many tabs
        self.parent.parent.initialize_ui()

        self.close()

    def acceptBatch(self):

        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            messagebox(self.parent, message)
            return

        try:
            param_dict = self.collect_parameter_values()
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        selected_subject_names = self.batching_widget.selected_subjects

        found = False
        for subject_name in selected_subject_names:
            subject = self.experiment.subjects[subject_name]
            for epoch_name in subject.epochs:
                if epoch_name == param_dict['collection_name']:
                    found = True
                    break

        if found:
            header = 'Collection name exists in experiment within one or more subjects. '
            message = 'Do you want to continue?'
            reply = QtWidgets.QMessageBox.question(self.parent, header, message,                
                QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.No:
                return 

        epoch_info = []

        experiment = self.experiment
        recently_active_subject = experiment.active_subject.subject_name

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    experiment.activate_subject(name)
                    events_str = self.calculate_epochs(subject, param_dict)
                    epoch_info.append(events_str)
                except Exception as e:
                    self.batching_widget.failed_subjects.append((subject, 
                                                                 str(e)))
                    logging.getLogger('ui_logger').error('Params: ' + str(param_dict))
                    logging.getLogger('ui_logger').exception(str(e))

        experiment.activate_subject(recently_active_subject)

        self.batching_widget.cleanup()
        self.experiment.save_experiment_settings()

        # reinitialize main window as epochs are shown in many tabs
        self.parent.parent.initialize_ui()
        
        if len(epoch_info) > 0:
            for info in epoch_info:
                logging.getLogger('ui_logger').info(info)
        self.close()

    def on_pushButtonFixedLength_clicked(self, checked=None):
        """Opens a dialog for creating fixed length events."""
        if checked is None:
            return
        if self.fixedLengthDialog is None:
            self.fixedLengthDialog = FixedLengthEpochDialog(self, self.experiment)
        self.fixedLengthDialog.show()

    def on_pushButtonEdit_clicked(self, checked=None):
        if checked is None:
            return
        self.bitDialog = BitSelectionDialog(self, self.ui.lineEditMask, self.ui.spinBoxEventID)
        self.bitDialog.show()

    def on_pushButtonHelp_clicked(self, checked=None):
        if checked is None:
            return
        help_message = ("Events are found in a following way. If only event " 
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

    def calculate_epochs(self, subject, param_dict):
        experiment = self.experiment

        @threaded
        def create(*args, **kwargs):
            events_str = create_epochs(experiment,
                param_dict, subject)
            return events_str

        events_str = create(do_meanwhile=self.parent.update_ui)

        return events_str
