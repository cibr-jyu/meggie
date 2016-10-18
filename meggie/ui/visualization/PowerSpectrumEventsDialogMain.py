'''
Created on 17.10.2016

@author: jaolpeso
'''
from PyQt4 import QtGui

import mne

from meggie.ui.visualization.powerSpectrumEventsUi import Ui_Advanced 
from meggie.ui.utils.messaging import exc_messagebox

class PowerSpectrumEvents(QtGui.QDialog):
    
    def __init__(self, parent):
        """
        Init method for the dialog.
        Constructs a set of time series from the given parameters.
        Parameters:
        parent     - The parent window for this dialog.
        """
        QtGui.QDialog.__init__(self)
        self.intervals = []
        self.ui = Ui_Advanced()
        self.ui.setupUi(self)
        self.parent = parent
        
    def accept(self):
        try:
            event_min = int(self.ui.lineEditStart.text())
            event_max = int(self.ui.lineEditEnd.text())
            group = int(self.ui.comboBoxAvgGroup.currentText())
        except:
            exc_messagebox(self, "Please check your inputs")
            return
        
        raw = self.parent.caller.experiment.active_subject.get_working_file()
        
        triggers = mne.find_events(raw)
        
        min_triggers = [trigger for trigger in triggers if trigger[2] == event_min]
        max_triggers = [trigger for trigger in triggers if trigger[2] == event_max]
        
        if len(min_triggers) != len(max_triggers):
            exc_messagebox(self, "Amount of start events should equal to amount of end events")
            return
        
        if len(min_triggers) == 0:
            exc_messagebox(self, 'No start events found')
            return
            
        if len(max_triggers) == 0:
            exc_messagebox(self, 'No end events found')
            return

        intervals = []
        
        for idx in range(len(min_triggers)):
            min_trigger_seconds = (min_triggers[idx][0] - raw.first_samp) / raw.info['sfreq']
            max_trigger_seconds = (max_triggers[idx][0] - raw.first_samp) / raw.info['sfreq']
            
            if max_trigger_seconds < min_trigger_seconds:
                exc_messagebox(self, "Selected events seem not be valid. Start and end events need to alternate.")
                return
            
            intervals.append((group, min_trigger_seconds, max_trigger_seconds))

        self.parent.add_intervals(intervals)