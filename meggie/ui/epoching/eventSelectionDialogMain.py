# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 19, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Atte Rautio
Contains the EventSelectionDialog-class that holds the logic for
EventSelectionDialog-window.
"""

import numpy as np
import mne

from xlrd import XLRDError
from PyQt4 import QtCore,QtGui
from copy import deepcopy

from meggie.code_meggie.general.wrapper import wrap_mne_call
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.general.caller import Caller
from meggie.code_meggie.epoching.events import Events
from meggie.code_meggie.general import fileManager

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.epoching.eventSelectionDialogUi import Ui_EventSelectionDialog
from meggie.ui.epoching.fixedLengthEpochDialogMain import FixedLengthEpochDialog
from meggie.ui.widgets.batchingWidgetMain import BatchingWidget


class EventSelectionDialog(QtGui.QDialog):
    """
    Class containing the logic for EventSelectionDialog. It is used for
    collecting desired events from continuous data.
    """
    caller = Caller.Instance()

    def __init__(self, parent): #, params = None):
        """Initialize the event selection dialog.

        Keyword arguments:

        parent -- Set the parent of this dialog
        params -- A dictionary containing parameter values to fill the
                  the different fields in the dialog with.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_EventSelectionDialog()
        self.ui.setupUi(self)
        self.fixedLengthDialog = None
        self.used_names = []
        ch_names = self.caller.experiment.active_subject.get_working_file().ch_names
        stim_channels = [x for x in ch_names if x.startswith('STI')]

        active = 0
        for idx, channel in enumerate(stim_channels):
            self.ui.comboBoxStimChannel.addItem(channel)
            if channel == self.caller.experiment.active_subject.find_stim_channel():
                active = idx
        self.ui.comboBoxStimChannel.setCurrentIndex(active)
        
        self.batching_widget = BatchingWidget(self, self.ui.scrollAreaWidgetContents)
        for name in self.caller.experiment.subjects:
            self.batching_widget.data[name] = {}
            self.batching_widget.data[name]['events'] = []
            self.batching_widget.data[name]['fixed_length_events'] = [] 

    def update_events(self, subject):
        """Add a list of events or a single event to the ui's eventlist.
        """
        self.ui.listWidgetEvents.clear()
        subject_name = subject.subject_name

        if 'events' in self.batching_widget.data[subject_name]:
            events = self.batching_widget.data[subject_name]['events']
            for event in events:
                item = QtGui.QListWidgetItem(
                    '%s, %s, %s' % (
                    'ID ' + str(event['event_id']),
                    'mask=' + str(event['mask']),
                    'stim=' + str(event['stim'])
                ))
                self.ui.listWidgetEvents.addItem(item)

        if 'fixed_length_events' in self.batching_widget.data[subject_name]:
            fixed_length_events = self.batching_widget.data[subject_name]['fixed_length_events']
            for idx, event in enumerate(fixed_length_events):
                item = QtGui.QListWidgetItem(
                    '%s, %s, %s, %s' % (
                    'Fixed ' + str(idx + 1),
                    'start=' + str(event['tmin']), 
                    'end=' + str(event['tmax']),
                    'interval=' + str(event['interval'])
                )) 
                self.ui.listWidgetEvents.addItem(item)

    def selection_changed(self, subject_name, params_dict):
        """
        """
        self.ui.comboBoxStimChannel.clear()
        subject = self.caller.experiment.subjects.get(subject_name)
	
	# Empty params_dict includes 'events' and 'fixed_length_events' keys.
	if len(params_dict) > 2:
	    dic = params_dict
	else:
	    dic = self.get_default_values(subject)
	    
	rejection = dic['reject']
	
	if 'grad' in rejection.keys():
	    self.ui.checkBoxGrad.setChecked(True)
	    self.ui.doubleSpinBoxGradReject_3.setValue(rejection['grad'])
	else:
	    self.ui.checkBoxGrad.setChecked(False)

	if 'mag' in rejection.keys():
	    self.ui.checkBoxMag.setChecked(True)
	    self.ui.doubleSpinBoxMagReject_3.setValue(rejection['mag'])
	else:
	    self.ui.checkBoxMag.setChecked(False)

	if 'eeg' in rejection.keys():
	    self.ui.checkBoxEeg.setChecked(True)
	    self.ui.doubleSpinBoxEEGReject_3.setValue(rejection['eeg'])
	else:
	    self.ui.checkBoxEeg.setChecked(False)

	if 'eog' in rejection.keys():
	    self.ui.checkBoxEog.setChecked(True)
	    self.ui.doubleSpinBoxEOGReject_3.setValue(rejection['eog'])
	else:
	    self.ui.checkBoxEog.setChecked(False)

        raw = subject.get_working_file(preload=False)
        ch_names = raw.ch_names

	if len(ch_names) == 0:
	    pass

	stim_channels = [x for x in ch_names if x.startswith('STI')]

	active = 0
	for idx, channel in enumerate(stim_channels):
	    self.ui.comboBoxStimChannel.addItem(channel)
	    if channel == dic['stim']:
		active = idx

	self.ui.comboBoxStimChannel.setCurrentIndex(active)
	
	if 'event_id' in dic.keys():
	    self.ui.spinBoxEventID.setValue(dic['event_id'])
	else:
	    self.ui.spinBoxEventID.setValue(1)
	
	self.ui.lineEditCollectionName.setText(dic['collection_name'])
	self.ui.doubleSpinBoxTmin.setValue(dic['tmin'])
	self.ui.doubleSpinBoxTmax.setValue(dic['tmax'])
	self.update_events(subject)

    def get_selected_subject(self):
        item = None

        if self.batching_widget.ui.checkBoxBatch.checkState():
            item = self.batching_widget.ui.listWidgetSubjects.currentItem()

        if item is None:
            subject_name = self.caller.experiment.active_subject.subject_name
        else:
            subject_name = str(item.text())

        return self.caller.experiment.subjects[subject_name]
    
    def get_default_values(self, subject):
        stim_channel = subject.find_stim_channel
        rejections = {
            'grad': 3000.00,
            'mag': 4000.00
        }
        return {
            'collection_name': 'Epochs',
            'tmin': -0.200,
            'tmax': 0.500,
            'include_stim': True,
            'event_id': 1,
            'stim': stim_channel,
            'mask': 0,
            'reject': rejections
        }

    def collect_parameter_values(self):
        """Collect the parameter values for epoch creation from the ui.

        Collect the parameter values for epoch creation from the ui and return
        them in a dictionary.
        """
        tmin = float(self.ui.doubleSpinBoxTmin.value())
        tmax = float(self.ui.doubleSpinBoxTmax.value())

        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked

        collection_name = str(self.ui.lineEditCollectionName.text())

        reject = dict()
        if mag:
            value = self.ui.doubleSpinBoxMagReject_3.value()
            if value != -1:
                reject['mag'] = value # 1e-15 * value
        if grad:
            value = self.ui.doubleSpinBoxGradReject_3.value()
            if value != -1:
                reject['grad'] = value # 1e-13 * value
        if eeg:
            value = self.ui.doubleSpinBoxEEGReject_3.value()
            if value != -1:
                reject['eeg'] = value # 1e-6 * value
        if eog:
            value = self.ui.doubleSpinBoxEOGReject_3.value()
            if value != -1:
                reject['eog'] = value # 1e-6 * value

        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        else: 
            meg = False

        subject = self.get_selected_subject()

        info = subject.get_working_file(preload=False).info

        picks = mne.pick_types(info, meg=meg, eeg=eeg, stim=stim, eog=eog)
        if len(picks) == 0:
            message = 'No picks found with current parameter values' 
            messagebox(self.parent, message)
            return

        events = deepcopy(self.batching_widget.data[subject.subject_name]['events'])  # noqa
        fle = deepcopy(self.batching_widget.data[subject.subject_name]['fixed_length_events'])  # noqa
        param_dict = {'mag' : mag, 'grad' : grad,
                      'eeg' : eeg, 'stim' : stim, 'eog' : eog,
                      'reject' : reject, 'tmin' : float(tmin),
                      'tmax' : float(tmax), 'collection_name' : collection_name,
                      'events' : events, 'fixed_length_events' : fle}
        return param_dict

    def create_eventlist(self, subject, event_params):
        """
        """
        raw = subject.get_working_file(temporary=True)
        e = Events(raw, event_params['stim'], event_params['mask'])
        mask = np.bitwise_not(event_params['mask'])
        events = e.pick(np.bitwise_and(event_params['event_id'], mask))
        return events

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Method for adding events to the event list.
        """
        if checked is None:
            return

        event_params = {
            'stim': str(self.ui.comboBoxStimChannel.currentText()),
            'mask': self.ui.spinBoxMask.value(),
            'event_id': self.ui.spinBoxEventID.value(),
        }
        
        subject = self.get_selected_subject()
        events = self.create_eventlist(subject, event_params)
        if len(events) != 0:
            self.batching_widget.data[subject.subject_name]['events'].append(event_params)
            self.update_events(subject)

    def accept(self):
        """
        """
        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            messagebox(self.parent, message)
            return

        param_dict = self.collect_parameter_values()
        
        epochs = self.parent.caller.experiment.active_subject.epochs
        if param_dict['collection_name'] in epochs:
            header = 'Epoch collection name exists. '
            message = ''.join([
                'Are you sure you want to overwrite the ',
                'collection?'
            ])
            reply = QtGui.QMessageBox.question(self.parent, header, message,                
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return
        
        self.batching_widget.data[self.caller.experiment.active_subject.subject_name] = param_dict
        try:
            self.calculate_epochs(self.caller.experiment.active_subject)
        except Exception as e:
            self.batching_widget.failed_subjects.append((
                self.caller.experiment.active_subject,
                str(e)
            ))
        
        # if not self.calculate_epochs(self.caller.experiment.active_subject):
        #     self.batching_widget.failed_subjects.append(
        #         self.caller.experiment.active_subject)

        self.batching_widget.cleanup()
        self.parent._initialize_ui()
        self.caller.experiment.save_experiment_settings()
        self.close()

    def acceptBatch(self):

        found = False
        for name, subject_data in self.batching_widget.data.items():
            for epoch_name in self.caller.experiment.subjects[name].epochs:
                if epoch_name == subject_data['collection_name']:
                    found = True
                    break

        if found:
            header = 'Collection name exists in experiment within one or more subjects. '
            message = ''.join([
                'Are you sure you want to overwrite the ',
                'collection?'
            ])
            reply = QtGui.QMessageBox.question(self.parent, header, message,                
                QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return 
            
        recently_active_subject = self.caller.experiment.active_subject.subject_name
        subject_names = []
        for i in range(self.batching_widget.ui.listWidgetSubjects.count()):
            item = self.batching_widget.ui.listWidgetSubjects.item(i)
            if item.checkState() == QtCore.Qt.Checked:
                subject_names.append(item.text())

        # In case of batch process:
        # 1. Calculation is first done for the active subject to prevent an
        #    excessive reading of a raw file.
        if recently_active_subject in subject_names:
            try:
                self.calculate_epochs(self.caller.experiment.active_subject)
            except Exception as e:
                self.batching_widget.failed_subjects.append((
                    self.caller.experiment.active_subject, str(e)))                
        
        # 2. Calculation is done for the rest of the subjects.
        for name, subject in self.caller.experiment.subjects.items():
            if name in subject_names:
                if name == recently_active_subject:
                    continue
                self.caller.activate_subject(name)
                
                try:
                    self.calculate_epochs(subject)
                except Exception as e:
                    self.batching_widget.failed_subjects.append((subject, 
                                                                 str(e)))
        self.caller.activate_subject(recently_active_subject)
        self.batching_widget.cleanup()
        self.parent._initialize_ui()
        self.caller.experiment.save_experiment_settings()
        self.close()

    def on_pushButtonFixedLength_clicked(self, checked=None):
        """Opens a dialog for creating fixed length events."""
        if checked is None:
            return
        if self.fixedLengthDialog is None:
            self.fixedLengthDialog = FixedLengthEpochDialog(self)
        self.fixedLengthDialog.show()

    def calculate_epochs(self, subject):
        self.caller.create_epochs(
            self.batching_widget.data[subject.subject_name], subject)

