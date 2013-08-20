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
Created on July 19, 2013

@author: Janne Pesonen
Contains the EpochParamsWidget-class used for listing epoch parameters.
"""
from PyQt4 import QtCore,QtGui

from epochParamsWidgetUi import Ui_Form

class EpochParamsWidget(QtGui.QWidget):
    """
    Creates a list that shows parameters of chosen epoch collection.
    """


    def __init__(self, parent):
        """
        Constructor 
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        
    def set_parameters(self, item):
        """
        Sets the parameters of the currently chosen epochs on epochWidget.
        Asks item for epoch parameters.
        
        Keyword arguments:
        item = current item on the epochs widget.
        """
        epochs = item.data(32).toPyObject()
        parameters = ''
        
        # Dictionary stores numbers of different events.
        event_counts = dict()
        
        # Adds items to dictionary for corresponding events.
        for value in epochs.event_id.values():
            event_counts[str(value)] = 0
        
        # Adds number of events to corresponding event.
        for event in epochs.events:
            for key in event_counts.keys():
                if event[2] == int(key):
                    event_counts[key] += 1
        
        # Adds event names, ids and event counts on mainWindows parameters
        # list.
        for key,value in epochs.event_id.items():
            parameters += key + ': ID ' + str(value) + ', ' + \
            str(event_counts[str(value)]) + ' events\n'
        
        # Adds rejection parameters.
        for key,value in epochs.reject.items():
            #parameters += key + ' = ' + str(value) + '\n'
            if key == 'mag':
                parameters += key + ': ' + str(value / 1e-12) + ' fT' + '\n'
            if key == 'grad':
                parameters += key + ': ' + str(value / 1e-12) + ' fT/cm' + '\n'
            if key == 'eeg':
                parameters += key + ': ' + str(value / 1e-6) + 'uV' + '\n'
            if key == 'eog':
                parameters += key + ': ' + str(value / 1e-6) + 'uV' + '\n'
        
        parameters += 'Start time: ' + str(epochs.tmin) + ' s\n'
        parameters += 'End time: ' + str(epochs.tmax) + ' s\n'
        
        """
        # Dictionary stores all parameter data.
        for key,value in epochs.reject.items():
            if key == 'mag':
                event_counts[key] = value / 1e-12    # str(value / 1e-12)?
            if key == 'grad':
                event_counts[key] = value / 1e-12
            if key == 'eeg':
                event_counts[key] = value / 1e-6
            if key == 'eog':
                event_counts[key] = value / 1e-6
                
        return event_counts
        """
        return parameters
        
        
        
    def show_parameters(self, item):
        """
        Sets parameters for the currently chosen epochs.
        
        Keyword arguments:
        item = epochWidget item that is currently chosen,
               includes .fif and .param files
        """
        
        # Set default/empty values for epoch parameters.
        self.ui.labelTmin.clear()
        self.ui.labelTmax.clear()
        params = item.data(33).toPyObject()
        
        
        self.ui.labelGradReject.setText('Grad: None')
        self.ui.labelMagReject.setText('Mag: None')
        self.ui.labelEegReject.setText('EEG: None')
        self.ui.labelStimReject.setText('Stim: None')
        self.ui.labelEogReject.setText('EOG: None')
        self.ui.textBrowserEvents.setText('')
        
        # Set parameters from currently chosen epochs.
        
       
        epochs = item.data(32).toPyObject()
        
        # Dictionary stores numbers of different events.
        event_counts = dict()
        
        # Adds items to dictionary for corresponding events.
        for value in epochs.event_id.values():
            event_counts[str(value)] = 0
        
        # Adds number of events to corresponding event.
        for event in epochs.events:
            for key in event_counts.keys():
                if event[2] == int(key):
                    event_counts[key] += 1
        
        """
        categories = 'Events: '
        for key in params[QtCore.QString(u'category')]:
            categories += key + ' '
        """
        categories = ''
        # Adds event names, ids and event counts on mainWindows parameters
        # list.
        for key,value in epochs.event_id.items():
            categories += key + ': ID ' + str(value) + ', ' + \
            str(event_counts[str(value)]) + ' events\n'
        
        self.ui.textBrowserEvents.setText(categories)
        self.ui.labelTmin.setText('Start time: ' + str(params[QtCore.QString('tmin')]) + ' s')
        self.ui.labelTmax.setText('End time: ' + str(params[QtCore.QString('tmax')]) + ' s')
        reject_params = params[QtCore.QString(u'reject')].keys()
        if QtCore.QString(u'mag') in reject_params:
            self.ui.labelMagReject.setText('Mag: ' + str(params[QtCore.QString(u'reject')][QtCore.QString(u'mag')] / 1e-12) + ' fT')
        if QtCore.QString(u'grad') in reject_params:
            self.ui.labelGradReject.setText('Grad: ' + str(params[QtCore.QString(u'reject')][QtCore.QString(u'grad')] / 1e-12) + ' fT/cm')
        if QtCore.QString(u'eeg') in reject_params:
            self.ui.labelEegReject.setText('EEG: ' + str(params[QtCore.QString(u'reject')][QtCore.QString(u'eeg')] / 1e-6) + 'uV')
        if QtCore.QString(u'stim') in reject_params:
            self.ui.checkBoxStim.setChecked(True)
            self.ui.labelStimReject.setText('Stim: Yes')
        if QtCore.QString(u'eog') in reject_params:
            self.ui.labelEogReject.setText('EOG: ' + str(params[QtCore.QString(u'reject')][QtCore.QString(u'eog')] / 1e-6) + 'uV')    
        
    def clear_parameters(self):
        self.ui.labelTmin.setText('Start time:')
        self.ui.labelTmax.setText('End time:')
        self.ui.labelGradReject.setText('Grad:')   #setText('Grad: None')
        self.ui.labelMagReject.setText('Mag:')   #setText('Mag: None')
        self.ui.labelEegReject.setText('EEG:')   #setText('EEG: None')
        self.ui.labelStimReject.setText('Stim:')   #setText('EEG: None')
        self.ui.labelEogReject.setText('EOG')   #setText('EOG: None')
        self.ui.textBrowserEvents.clear()   #setText('')
        