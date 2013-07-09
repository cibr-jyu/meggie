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
Created on Apr 30, 2013

@author: Jaakko Leppakangas
Contains the EpochDialog class that holds the logic for epochDialog-window.
"""
import messageBox
from epochDialogUi import Ui_Dialog

from epochs import Epochs

from PyQt4 import QtCore,QtGui

import numpy as np

class EpochDialog(QtGui.QDialog):
    """
    Class containing the logic for epochDialog. Used for creating epochs from
    a set of events.
    """
    index = 1

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def accept(self):
        self.tmin = float(self.ui.doubleSpinBoxTmin.value())
        self.tmax = float(self.ui.doubleSpinBoxTmax.value())
        mag = self.ui.checkBoxMag.checkState() == QtCore.Qt.Checked
        grad = self.ui.checkBoxGrad.checkState() == QtCore.Qt.Checked
        eeg = self.ui.checkBoxEeg.checkState() == QtCore.Qt.Checked
        stim = self.ui.checkBoxStim.checkState() == QtCore.Qt.Checked
        eog = self.ui.checkBoxEog.checkState() == QtCore.Qt.Checked
        stim_channel = self.parent.parent.experiment.stim_channel
        
        reject = dict()
        if mag:
            reject['mag'] = 1e-12 * self.ui.doubleSpinBoxMagReject_3.value()
        if grad:
            reject['grad'] = 1e-12 * self.ui.doubleSpinBoxGradReject_3.value()
        if eeg:
            reject['eeg'] = eeg = 1e-6 * self.ui.doubleSpinBoxEEGReject_3.value()
        if eog:
            reject['eog'] = eog = 1e-6 * self.ui.doubleSpinBoxEOGReject_3.value()

        """
        Reads the given event names as categories.
        """
        events = np.ndarray((self.parent.ui.listWidgetEvents.count(),3), int)
        category = dict()
        for index in xrange(self.parent.ui.listWidgetEvents.count()):
            event = (self.parent.ui.listWidgetEvents.item(index).data(32).
                     toPyObject())
            events[index] = (event)
            category[str(self.parent.ui.listWidgetEvents.item(index).data(33).
                         toPyObject())] = event[2]
        try:
            epochs = Epochs(self.parent.parent.experiment.working_file, events,
                            mag, grad, eeg, stim, eog, reject, category,
                            float(self.tmin), float(self.tmax))
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Could not create epochs: '
                                                   + str(err))
            self.messageBox.exec_()
            return
        
        """
        Add's the epochs to the mainWindow's list.
        """
        item_string = ''
        for key, value in epochs.epochs.event_id.iteritems():
            item_string += key + '=' + str(value) + ' ' 
        item = QtGui.QListWidgetItem(item_string)
        item.setData(32, epochs)
        self.parent.parent.epochList.addItem(item)
        self.parent.parent.epochList.setCurrentItem(item)
        self.close()
        #return epochs