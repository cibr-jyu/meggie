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
Created on May 2, 2013

@author: Jaakko Leppakangas, Atte Rautio
Contains the EpochWidget-class used for listing epoch collections.
"""
from PyQt4 import QtCore,QtGui

from epochParamsWidgetUi import Ui_Form

class EpochParamsWidget(QtGui.QWidget):
    """
    Creates a widget that shows a list of epoch collections.
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
        
        Keyword arguments:
        item = item to be set as the current item.
        """
        epochs = item.data(32).toPyObject()
        parameters = ''
        
        # Dictionary stores numbers of different events.
        event_counts = dict()
        
        # Adds items to dictionary for corresponding events.
        for key,value in epochs.event_id.items():
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
        self.ui.textEditEpochParams.setText(parameters)
        