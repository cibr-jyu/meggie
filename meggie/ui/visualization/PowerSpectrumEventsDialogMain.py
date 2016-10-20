'''
Created on 17.10.2016

@author: jaolpeso
'''
from PyQt4 import QtGui

import mne

from meggie.ui.visualization.powerSpectrumEventsUi import Ui_Advanced 
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.general.bitSelectionDialogMain import BitSelectionDialog

class PowerSpectrumEvents(QtGui.QDialog):
    
    def __init__(self, parent):
        """
        Init method for the dialog.
        Parameters:
        parent     - The parent window for this dialog.
        """
        QtGui.QDialog.__init__(self)
        self.intervals = []
        self.ui = Ui_Advanced()
        self.ui.setupUi(self)
        self.parent = parent
        
    def on_pushButtonMaskStart_clicked(self, checked=None):
        if checked is None:
            return
        self.bitDialog = BitSelectionDialog(self, self.ui.lineEditStart)
        self.bitDialog.show()

    def on_pushButtonMaskEnd_clicked(self, checked=None):
        if checked is None:
            return
        self.bitDialog = BitSelectionDialog(self, self.ui.lineEditEnd)
        self.bitDialog.show()
        
    def accept(self):
        try:
            event_min = self.ui.lineEditStart.text()
            event_max = self.ui.lineEditEnd.text()
            group = int(self.ui.comboBoxAvgGroup.currentText())
        except:
            exc_messagebox(self, "Please check your inputs")
            return
        
        raw = self.parent.caller.experiment.active_subject.get_working_file()
        
        def find_triggers(event_code):
            try:
                id_, mask = event_code.split('|')
            except ValueError:
                id_, mask = event_code, 0
            from meggie.code_meggie.utils.debug import debug_trace; debug_trace()
            triggers = mne.find_events(raw, mask=int(mask))
            triggers = [trigger for trigger in triggers if trigger[2] == id_]
        
        min_triggers = find_triggers(event_min)
        max_triggers = find_triggers(event_max)
        
        # triggers = mne.find_events(raw)
        
        # min_triggers = [trigger for trigger in triggers if trigger[2] == event_min]
        # max_triggers = [trigger for trigger in triggers if trigger[2] == event_max]
        
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