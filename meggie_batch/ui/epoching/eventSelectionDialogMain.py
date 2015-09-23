# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
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
from xlrd import XLRDError
from PyQt4 import QtCore,QtGui
import mne

from eventSelectionDialogUi import Ui_EventSelectionDialog
from groupEpochingDialogMain import GroupEpochingDialog
from fixedLengthEpochDialogMain import FixedLengthEpochDialog
from code_meggie.general.caller import Caller
from code_meggie.epoching.events import Events
from code_meggie.general import fileManager
from ui.general import messageBoxes


class EventSelectionDialog(QtGui.QDialog):
    """
    Class containing the logic for EventSelectionDialog. It is used for
    collecting desired events from continuous data.
    """
    caller = Caller.Instance()
    #custom signals:
    epoch_params_ready = QtCore.pyqtSignal(dict)

    def __init__(self, parent, params = None):
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
        self.ui.lineEditName.setText('Event')
        self.used_names = []
        if params is not None:
            self.fill_parameters(params)

    def initialize(self, epochs_name):
        """
        Method for initializing the dialog. Used for modifying existing epoch
        collection.
        Keyword arguments
        epoch_name -- Name of the epoch collection.
        """
        epochs = self.caller.experiment.active_subject.get_epochs(epochs_name)
        self.ui.lineEditCollectionName.setText(epochs_name)
        self.ui.doubleSpinBoxTmin.setValue(epochs.tmin)
        self.ui.doubleSpinBoxTmax.setValue(epochs.tmax)
        event_name = epochs.event_id.keys()[0]
        self.ui.lineEditName.setText(event_name)
        event_id = epochs.event_id.values()[0]
        self.ui.spinBoxEventID.setValue(event_id)
        events = list()
        for event in epochs.events:
            events.append([int(event[0]), int(event[1]), int(event[2])])
        self.add_events(events, event_name)

    def add_events(self, events, event_name):
        """Add a list of events or a single event to the ui's eventlist.

        Keyword arguments:

        events     -- Events to add.
        event_name -- The user-defined name of the events. Default is 'event'.
        """
        for event in events:
            time = self.caller.index_as_time(event[0])
            item = CustomListItem('%0.3fs, %s %s, %s' % (time, event_name,
                                                         event[0], event[2]))

            item.setData(32, event)
            item.setData(33, event_name)
            self.ui.listWidgetEvents.addItem(item)

        self.ui.listWidgetEvents.sortItems()
        if self.used_names.count(event_name) < 1:    
            self.used_names.append(event_name)

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
        #stim_channel = self.caller.experiment.active_subject._stim_channel

        collectionName = str(self.ui.lineEditCollectionName.text())
        if len(self.parent.epochList.ui.listWidgetEpochs.\
            findItems(collectionName, QtCore.Qt.MatchExactly)) > 0:
            msg = ('Collection name %s exists. Overwrite existing epochs?' %
                   collectionName)
            reply = QtGui.QMessageBox.question(self, 'Collection exists', msg,
                                               QtGui.QMessageBox.Yes |
                                               QtGui.QMessageBox.No,
                                               QtGui.QMessageBox.No)
            if reply == QtGui.QMessageBox.No:
                return None

        reject = dict()
        if mag:
            reject['mag'] = 1e-15 * self.ui.doubleSpinBoxMagReject_3.value()
        if grad:
            reject['grad'] = 1e-13 * self.ui.doubleSpinBoxGradReject_3.value()
        if eeg:
            reject['eeg'] = 1e-6 * self.ui.doubleSpinBoxEEGReject_3.value()
        if eog:
            reject['eog'] = 1e-6 * self.ui.doubleSpinBoxEOGReject_3.value()

        events = list()
        for i in xrange(self.ui.listWidgetEvents.count()):
            event = self.ui.listWidgetEvents.item(i).data(32)
            event_name = self.ui.listWidgetEvents.item(i).data(33)
            event_tup = (event, event_name)
            events.append(event_tup)

        #Check if any picks are found with current parameter values.

        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        else: meg = False
        info = self.caller.experiment.active_subject.working_file.info
        picks = mne.pick_types(info, meg=meg, eeg=eeg, stim=stim, eog=eog)
        if len(picks) == 0:
            message = 'No picks found with current parameter values' 
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return

        #Create a dictionary containing all the parameters
        #Note: Raw is not collected here.
        param_dict = {'events' : events, 'mag' : mag, 'grad' : grad,
                      'eeg' : eeg, 'stim' : stim, 'eog' : eog,
                      'reject' : reject, 'tmin' : float(tmin),
                      'tmax' : float(tmax), 'collectionName' : collectionName}
        return param_dict

    def create_eventlist(self):
        """
        Pick desired events from the raw data.
        """
        event_id = self.ui.spinBoxEventID.value()
        mask = self.ui.spinBoxMask.value()
        e = Events(self.caller.experiment.active_subject.working_file,
                   self.caller.experiment.active_subject.stim_channel, mask)
        mask = np.bitwise_not(mask)
        events = e.pick(np.bitwise_and(event_id, mask))
        print str(events)
        return events

    def fill_parameters(self, params):
        """Fill the fields in the dialog with parameters values from a dict.

        Keyword arguments:

        params -- A dict containing the parameter values to be used.
        """
        params_str = dict((str(key), value) for
                          key, value in params.iteritems())
        for item in params_str['events']:
            events = []
            events.append(item[0])
            event_name = item[1]
            self.add_events(events, event_name)

        if params_str['mag'] is True:
            self.ui.checkBoxMag.setChecked(True)
        else:
            self.ui.checkBoxMag.setChecked(False)

        if params_str['grad'] is True:
            self.ui.checkBoxGrad.setChecked(True)
        else:
            self.ui.checkBoxGrad.setChecked(False)

        if params_str['eeg'] is True:
            self.ui.checkBoxEeg.setChecked(True)
        else:
            self.ui.checkBoxEeg.setChecked(False)

        if params_str['stim'] is True:
            self.ui.checkBoxStim.setChecked(True)
        else:
            self.ui.checkBoxStim.setChecked(False)

        if params_str['eog'] is True:
            self.ui.checkBoxEog.setChecked(True)
        else:
            self.ui.checkBoxEog.setChecked(False)

        reject = params_str['reject']
        if reject.has_key('mag'):
            self.ui.doubleSpinBoxMagReject_3.setValue(reject['mag'])

        if reject.has_key('grad'):
            self.ui.doubleSpinBoxGradReject_3.setValue(reject['grad'])

        if reject.has_key('eeg'):
            self.ui.doubleSpinBoxEegReject_3.setValue(reject['eeg'])

        if reject.has_key('eog'):
            self.ui.doubleSpinBoxEogReject_3.setValue(reject['eog'])

        self.ui.doubleSpinBoxTmin.setValue(params_str['tmin'])
        self.ui.doubleSpinBoxTmax.setValue(params_str['tmax'])
        self.ui.lineEditCollectionName.setText(params_str['collectionName'])

    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Method for adding events to the event list.
        """
        if checked is None: return
        name = self.set_event_name(self.ui.lineEditName.text())
        events = self.create_eventlist()
        self.add_events(events, name)
        self.ui.lineEditName.setText('Event')

    def accept(self):
        """Save the parameters in a dictionary and send it forward.

        Collect all the parameters provided for epoch creations in a
        dictionary and send it forward using a QSignal. Show the user an error
        message if no events are selected for epoching.

        Emit an epoch_params_ready signal.
        """
        if self.ui.listWidgetEvents.count() == 0:
            message = 'Cannot create epochs from empty list.'
            self.errorMessage = messageBoxes.shortMessageBox(message)
            self.errorMessage.show()
            return
        QtGui.QApplication.setOverrideCursor(QtGui.
                                             QCursor(QtCore.Qt.WaitCursor))
        param_dict = self.collect_parameter_values()
        if param_dict is None:
            QtGui.QApplication.restoreOverrideCursor()
            return

        if len(param_dict['reject']) == 0:
            QtGui.QApplication.restoreOverrideCursor()
            message = 'Picks cannot be empty. Select picks by checking the ' +\
                      ' checkboxes.'
            self.errorMessage = messageBoxes.shortMessageBox(message)
            self.errorMessage.show()
            return

        self.epoch_params_ready.emit(param_dict)
        QtGui.QApplication.restoreOverrideCursor()
        self.close()

    def on_pushButtonSaveEvents_clicked(self, checked=None):
        """
        Called when save events button is clicked. Saves all the events in the
        list to an excel-file.
        """
        if checked is None: return # Standard workaround
        events = np.ndarray((self.ui.listWidgetEvents.count(),4), dtype=object)
        for index in xrange(self.ui.listWidgetEvents.count()):
            category = (self.ui.listWidgetEvents.item(index).
                        data(33))
            events[index,0] = str(category)
            event = self.ui.listWidgetEvents.item(index).data(32)
            events[index,1:] = event
        #events = self.create_eventlist()'
        if len(events) > 0:
            try:
                activeSubject = self.caller._experiment._active_subject
                fileManager.write_events(events, activeSubject)
            except UnicodeDecodeError, err:
                message = 'Cannot save events: ' + str(err)
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                print 'Aborting...'
                return

    def on_pushButtonReadEvents_clicked(self, checked=None):
        """
        Called when read events button is clicked. Reads events from an 
        excel-file.
        """
        if checked is None: return # Standard workaround
        title = 'Read events from xls. Format: name|sample|old id|new id.'
        filename = str(QtGui.QFileDialog.getOpenFileName(self, title,
                                                         self.caller.\
                                                         experiment.\
                                                         active_subject.\
                                                         subject_path))
        if filename == '':
            return
        self.ui.listWidgetEvents.clear()
        try:
            sheet = fileManager.read_events(filename)
        except XLRDError, err:
            self.messageBox = messageBoxes.shortMessageBox(str(err))
            self.messageBox.show()
            return

        for row_index in range(sheet.nrows):
            #Check that there are no empty cells in a row
            if not (any([x == '' for x in sheet.row_values(row_index)])):
                item = CustomListItem(str(sheet.cell(row_index,0).value) +
                                      ' ' + str(int(sheet.cell(row_index, 1).
                                                    value)) + ', ' +
                                      str(int(sheet.cell(row_index, 3).value)))
                event = map(int, sheet.row_values(row_index)[1:4])
                print event
                item.setData(32, event)
                item.setData(33, str(sheet.cell(row_index,0).value))
                self.ui.listWidgetEvents.addItem(item)

        self.ui.listWidgetEvents.setCurrentItem(item)

    def on_pushButtonBatching_clicked(self, checked=None):
        """
        Opens a dialog for batch processing epochs.
        """
        if checked is None: return
        batchDialog = GroupEpochingDialog()
        batchDialog.exec_()

    def on_pushButtonFixedLength_clicked(self, checked=None):
        """Opens a dialog for creating fixed length events."""
        if checked is None:
            return
        if self.fixedLengthDialog is None:
            self.fixedLengthDialog = FixedLengthEpochDialog(self)
        self.fixedLengthDialog.fixed_events_ready.connect(self.
                                                          on_fixedEventsCreated)
        self.fixedLengthDialog.show()

    @QtCore.pyqtSlot(list, str)
    def on_fixedEventsCreated(self, events, name):
        """
        """
        self.add_events(events, name)

    def on_pushButtonClear_clicked(self, checked=None):
        """
        Method for clearing the event list.
        """
        for row in range(self.ui.listWidgetEvents.count()):
            item = self.ui.listWidgetEvents.item(row)
            if item.data(33) in self.used_names:
                self.used_names.remove(item.data(33))
        self.ui.listWidgetEvents.clear()

    def set_event_name(self, name, suffix = 1):
        """Set the event name to name. If name exists, add suffix to it

        Keyword arguments:

        name   -- The name to be set.
        Suffix -- The suffix that is added to the name when greater than 1.

        Return the name that was set.
        """
        if suffix == 1 and self.used_names.count(name) == 0:
            return name

        elif suffix == 1 and self.used_names.count(name) > 0:
            suffix += 1
            name = self.set_event_name(name, suffix)
            return name

        elif suffix > 1 and self.used_names.count(name + str(suffix)) == 0:
            name = name + str(suffix)
            return name

        elif suffix > 1 and self.used_names.count(name + str(suffix)) > 0:
            suffix += 1
            name = self.set_event_name(name, suffix)
            return name


class CustomListItem(QtGui.QListWidgetItem):
    """Custom list widget item for enabling sorting by sample."""
    def __lt__(self, other):
        return self.data(32)[0] < other.data(32)[0]  # sample comparison
