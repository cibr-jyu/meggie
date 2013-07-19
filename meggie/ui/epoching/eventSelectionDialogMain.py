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
import messageBox

from PyQt4 import QtCore,QtGui
from eventSelectionDialogUi import Ui_EventSelectionDialog
from epochDialogMain import EpochDialog

from epochs import Epochs
from events import Events

# TODO this is for the currently unused check_channels method. 
#import brainRegions

import numpy as np

from xlrd import XLRDError

class EventSelectionDialog(QtGui.QDialog):
    """
    Class containing the logic for EventSelectionDialog. It is used for
    collecting desired events from continuous data.
    """
    index = 1

    def __init__(self, parent):
        """
        Initializes the event selection dialog.
        """
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_EventSelectionDialog()
        self.ui.setupUi(self)
        keys = map(str, parent.experiment.event_set.keys())
        self.ui.comboBoxEventID.addItems(keys)
        self.ui.lineEditName.setText('Event' + str(self.__class__.index))
        
    def create_eventlist(self):
        """
        Picks desired events from the raw data.
        """
        self.event_id = int(self.ui.comboBoxEventID.currentText())
        e = Events(self.parent.experiment.raw_data, 
                   self.parent.experiment.stim_channel)
        e.pick(self.event_id)
        return e.events
        
    def on_pushButtonAdd_clicked(self, checked=None):
        """
        Method for adding events to the event list.
        """
        if checked is None: return
        events = self.create_eventlist()
        print events
        self.__class__.index += 1
        
        """
        Adds the events to the list.
        """
        if isinstance(events, np.ndarray):
            for event in events:
                item = QtGui.QListWidgetItem(self.ui.lineEditName.text() +
                                             ' ' + str(event[0]) + ', ' +
                                             str(event[2]))
                item.setData(32, event)
                item.setData(33, self.ui.lineEditName.text())
                self.ui.listWidgetEvents.addItem(item)
            self.ui.listWidgetEvents.setCurrentItem(item)
            self.ui.lineEditName.setText('Event' + str(self.__class__.index))
            self.ui.pushButtonRemove.setEnabled(True)
        
    def on_pushButtonRemove_clicked(self, checked=None):
        """
        Method for removing events from the event list.
        """
        if checked is None: return # Standard workaround
        row = self.ui.listWidgetEvents.currentRow()
        self.ui.listWidgetEvents.takeItem(row)
        if self.ui.listWidgetEvents.currentRow() < 0:
            self.ui.pushButtonRemove.setEnabled(False)
        
    def accept(self):
        """
        Called when the OK button is pressed. Opens the epoching dialog
        (epochDialog).
        """
        if self.ui.listWidgetEvents.count() == 0:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Cannot create epochs ' + 
                                                   'from empty list.')
            self.messageBox.show()
            return
        
        self.close()
        self.epochDialog = EpochDialog(self, self.ui.\
                                       lineEditCollectionName.text())
        epochs = self.epochDialog.exec_()
        
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
        