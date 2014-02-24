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
        

        
        
        
    def show_parameters(self, item):
        """
        Sets parameters from the currently chosen epochs.
        
        Keyword arguments:
        item = epochWidget item that is currently chosen,
               includes .fif and .param files
        """
        
        # Set default/empty values for epoch parameters.
        self.ui.labelTmin.clear()
        self.ui.labelTmax.clear()
        self.ui.labelGradReject.setText('Grad: None')
        self.ui.labelMagReject.setText('Mag: None')
        self.ui.labelEegReject.setText('EEG: None')
        self.ui.labelStimReject.setText('Stim: None')
        self.ui.labelEogReject.setText('EOG: None')
        self.ui.textBrowserEvents.setText('')

        params = item.data(33).toPyObject()
        if params is None: return
       
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
        
        categories = ''
        # Adds event names, ids and event counts on mainWindows parameters
        # list.
        for key,value in epochs.event_id.items():
            categories += key + ': ID ' + str(value) + ', ' + \
            str(event_counts[str(value)]) + ' events\n'
        
        self.ui.textBrowserEvents.setText(categories)
        self.ui.labelTmin.setText('Start time: ' + 
                                  str(params[QtCore.QString('tmin')]) + ' s')
        self.ui.labelTmax.setText('End time: ' + 
                                  str(params[QtCore.QString('tmax')]) + ' s')

        # Creates dictionary of strings instead of qstrings for rejections.
        params_rejections_str = dict((str(key), value) for
                          key, value in params[QtCore.QString(u'reject')].\
                          iteritems())
        if 'mag' in params_rejections_str:
            self.ui.labelMagReject.setText('Mag: ' + 
                                           str(params_rejections_str['mag']\
                                                 / 1e-12) + ' fT')
        if 'grad' in params_rejections_str:
            self.ui.labelGradReject.setText('Grad: ' + 
                                            str(params_rejections_str['grad']\
                                                 / 1e-12) + ' fT/cm')
        if 'eeg' in params_rejections_str:
            self.ui.labelEegReject.setText('EEG: ' + 
                                           str(params_rejections_str['eeg']\
                                                / 1e-6) + 'uV')
        if 'stim' in params_rejections_str:
            #self.ui.checkBoxStim.setChecked(True)
            self.ui.labelStimReject.setText('Stim: Yes')
        if 'eog' in params_rejections_str:
            self.ui.labelEogReject.setText('EOG: ' + 
                                           str(params_rejections_str['eog']\
                                                / 1e-6) + 'uV')    
        
        filename_full_path = str(params[QtCore.QString(u'raw')])
        filename_list = filename_full_path.split('/')
        filename = filename_list[len(filename_list) - 1]
        self.ui.textBrowserWorkingFile.setText(filename)
        #self.ui.textBrowserWorkingFile.setText(params[QtCore.QString(u'raw')])
        
        
    def clear_parameters(self):
        self.ui.labelTmin.setText('Start time:')
        self.ui.labelTmax.setText('End time:')
        self.ui.labelGradReject.setText('Grad:')   #setText('Grad: None')
        self.ui.labelMagReject.setText('Mag:')   #setText('Mag: None')
        self.ui.labelEegReject.setText('EEG:')   #setText('EEG: None')
        self.ui.labelStimReject.setText('Stim:')   #setText('EEG: None')
        self.ui.labelEogReject.setText('EOG')   #setText('EOG: None')
        self.ui.textBrowserEvents.clear()   #setText('')
        self.ui.textBrowserWorkingFile.clear()