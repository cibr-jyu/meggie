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
import messageBoxes

from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import QString
from eventSelectionDialogUi import Ui_EventSelectionDialog
from epochDialogMain import EpochDialog

from epochs import Epochs
from events import Events

import mne

# TODO this is for the currently unused check_channels method. 
#import brainRegions

import numpy as np

#from xlrd import XLRDError

from functools import partial

class EventSelectionDialog(QtGui.QDialog):
    
    """
    Class containing the logic for EventSelectionDialog. It is used for
    collecting desired events from continuous data.
    """
    
    #custom signals:
    epoch_params_ready = QtCore.pyqtSignal(dict, QtGui.QListWidget)

    def __init__(self, parent, raw, params = None):
        """Initialize the event selection dialog.
        
        Keyword arguments:
        
        parent -- Set the parent of this dialog
        raw    -- Raw data
        params -- A dictionary containing parameter values to fill the
                  the different fields in the dialog with.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.raw = raw
        self.ui = Ui_EventSelectionDialog()
        self.ui.setupUi(self)
        keys = map(str, parent.experiment.active_subject._event_set.keys())
        self.ui.comboBoxEventID.addItems(keys)
        self.ui.lineEditName.setText('Event')
        self.used_names = []
        if params is not None:
            self.fill_parameters(params)
        
    def add_events(self, events, event_name):
        """Add a list of events or a single event to the ui's eventlist.
        
        Keyword arguments:
        
        events     -- Events to add.
        event_name -- The user-defined name of the events. Default is 'event'.
        """
        for event in events:
            item = QtGui.QListWidgetItem(event_name + ' ' + str(event[0]) +
                                         ', ' + str(event[2]))
                
            item.setData(32, event)
            item.setData(33, event_name)
            self.ui.listWidgetEvents.addItem(item)
        
        if self.used_names.count(event_name) < 1:    
            self.used_names.append(event_name)
        
        self.ui.pushButtonRemove.setEnabled(True)
        
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
        stim_channel = self.parent.experiment.active_subject._stim_channel
        
        collectionName = self.ui.lineEditCollectionName.text()
        collectionName.replace(0, 1, collectionName[0].toUpper())
        if len(self.parent.epochList.ui.listWidgetEpochs.\
            findItems(collectionName, QtCore.Qt.MatchExactly)) > 0:
            message = 'Collection name ' + str(collectionName) + ' exists. ' + \
            'Please change name of the epoch collection.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return None
        
        # QString to string
        collectionName = str(collectionName)
        
        reject = dict()
        if mag:
            reject['mag'] = 1e-12 * self.ui.\
            doubleSpinBoxMagReject_3.value()
        if grad:
            reject['grad'] = 1e-12 * self.ui.\
            doubleSpinBoxGradReject_3.value()
        if eeg:
            reject['eeg'] = eeg = 1e-6 * self.ui.\
            doubleSpinBoxEEGReject_3.value()
        if eog:
            reject['eog'] = eog = 1e-6 * self.ui.\
            doubleSpinBoxEOGReject_3.value()
            
        events = []
        # TODO: what type of data is in slots 32 and 33?
        for i in xrange(self.ui.listWidgetEvents.count()):
            event = self.ui.listWidgetEvents.item(i).data(32).toPyObject()
            event_name = self.ui.listWidgetEvents.item(i).data(33).toPyObject()
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
        
        picks = mne.fiff.pick_types(self.raw.info, meg=meg, eeg=eeg,
                                    stim=stim, eog=eog)
        if len(picks) == 0:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('No picks found with current parameter values')
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
        self.event_id = int(self.ui.comboBoxEventID.currentText())
        e = Events(self.raw, self.parent.experiment.active_subject._stim_channel)
        e.pick(self.event_id)
        print str(e.events)
        return e.events
    
    def fill_parameters(self, params):
        """Fill the fields in the dialog with parameters values from a dict.
        
        Keyword arguments:
        
        params -- A dict containing the parameter values to be used.
        """
        #toPyObject() which is used to convert the data in a QListWidgetItem
        #back in to a dict turns the keys into QStrings for some reason.
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
        
    def on_pushButtonRemove_clicked(self, checked=None):
        """
        Method for removing events from the event list.
        """
        if checked is None: return # Standard workaround
        if len(self.ui.listWidgetEvents.selectedItems()) == 0: return
        
        for item in self.ui.listWidgetEvents.selectedItems():
            row = self.ui.listWidgetEvents.row(item)
            self.ui.listWidgetEvents.takeItem(row)
            
            #If the item was the last one with a certain name, remove the name
            #from the used names -list.
            name = item.data(33).toPyObject()
            if len(self.ui.listWidgetEvents.findItems(name + ' ',
                                                      QtCore.Qt.\
                                                      MatchStartsWith)) == 0:
                self.used_names.remove(name)
            
        if self.ui.listWidgetEvents.currentRow() < 0:
            self.ui.pushButtonRemove.setEnabled(False)
        
    def accept(self):
        """Save the parameters in a dictionary and send it forward.
        
        Collect all the parameters provided for epoch creations in a
        dictionary and send it forward using a QSignal. Show the user an error
        message if no events are selected for epoching.
        
        Emit an epoch_params_ready signal.
        """
        if self.ui.listWidgetEvents.count() == 0:
            self.errorMessage = messageBox.AppForm()
            self.errorMessage.labelException.setText('Cannot create epochs ' + 
                                                   'from empty list.')
            self.errorMessage.show()
            return
        
        param_dict = self.collect_parameter_values()
        if param_dict is None:
            return
        
        if len(param_dict['reject']) == 0:
            self.errorMessage = messageBox.AppForm()
            self.errorMessage.labelException.setText('Picks cannot be empty. ' + 
                                'Select picks by checking the checkboxes.')
            self.errorMessage.show()
            
            return
        
        self.epoch_params_ready.emit(param_dict, self.parent.epochList)
        self.close()
        
    def check_channels(self):
        """
        Method for populating the combobox with channel groups of brain
        regions. Currently not in use.
        """
        if self.ui.comboBoxChannelGroup.currentText() == 'Vertex':
            return ['MEG ' + str(x) for x in brainRegions.vertex]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-temporal':
            return ['MEG ' + str(x) for x in brainRegions.left_temporal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-temporal':
            return ['MEG ' + str(x) for x in brainRegions.right_temporal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-parietal':
            return ['MEG ' + str(x) for x in brainRegions.left_parietal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-parietal':
            return ['MEG ' + str(x) for x in brainRegions.right_parietal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-occipital':
            return ['MEG ' + str(x) for x in brainRegions.left_occipital]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-occipital':
            return ['MEG ' + str(x) for x in brainRegions.right_occipital]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Left-frontal':
            return ['MEG ' + str(x) for x in brainRegions.left_frontal]
        elif self.ui.comboBoxChannelGroup.currentText() == 'Right-frontal':
            return ['MEG ' + str(x) for x in brainRegions.right_frontal]

    def on_pushButtonSaveEvents_clicked(self, checked=None):
        """
        Called when save events button is clicked. Saves all the events in the
        list to an excel-file.
        """
        if checked is None: return # Standard workaround
        events = np.ndarray((self.ui.listWidgetEvents.count(),4), dtype=object)
        for index in xrange(self.ui.listWidgetEvents.count()):
            category = (self.ui.listWidgetEvents.item(index).
                        data(33).toPyObject())
            events[index,0] = str(category)
            event = self.ui.listWidgetEvents.item(index).data(32).toPyObject()
            events[index,1:] = event
        #events = self.create_eventlist()'
        if len(events) > 0:
            print 'Writing events...'
            try:
                self.parent.caller.write_events(events)
            except UnicodeDecodeError, err:
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText('Cannot save events: ' +
                                                       str(err))
                self.messageBox.show()
                print 'Aborting...'
                return
            print 'Done.'
    
    def on_pushButtonReadEvents_clicked(self, checked=None):
        """
        Called when read events button is clicked. Reads events from an 
        excel-file.
        """
        if checked is None: return # Standard workaround
        filename = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                    self.parent.experiment.subject_directory))
        if filename == '':
            return
        self.ui.listWidgetEvents.clear()
        try:
            sheet = self.parent.caller.read_events(filename)
        except XLRDError, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            return

        for row_index in range(sheet.nrows):
            #Check that there are no empty cells in a row
            if not (any([x == '' for x in sheet.row_values(row_index)])):
                item = QtGui.QListWidgetItem(str(sheet.cell(row_index,0).value)
                                             + ' ' + str(int(sheet.cell
                                                             (row_index,1).
                                                             value))
                                             + ', ' + str(int(sheet.cell
                                                              (row_index,3)
                                                              .value)))
                event = map(int, sheet.row_values(row_index)[1:4])
                item.setData(32, event)
                item.setData(33, str(sheet.cell(row_index,0).value))
                self.ui.listWidgetEvents.addItem(item)
            
        self.ui.listWidgetEvents.setCurrentItem(item)
        
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
             
        