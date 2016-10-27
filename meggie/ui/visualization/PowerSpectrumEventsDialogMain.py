'''
Created on 17.10.2016

@author: jaolpeso
'''
from PyQt4 import QtGui

import mne

from meggie.ui.visualization.powerSpectrumEventsUi import Ui_Advanced 
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.general.bitSelectionDialogMain import BitSelectionDialog

from meggie.code_meggie.epoching.events import Events

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

            if not event_min or not event_max:
                raise Exception("No min and max events set")
        except:
            exc_messagebox(self, "Please check your inputs")
            return

        raw = self.parent.caller.experiment.active_subject.get_working_file()
        
        def should_take(id_, mask, event):
            """ check if event has same non-masked bits as id_
            """
            id_bin = '{0:016b}'.format(id_)
            mask_bin = '{0:016b}'.format(mask)
            event_bin = '{0:016b}'.format(event[2])
            
            take_event = True
            for i in range(len(mask_bin)):
                if int(mask_bin[i]) == 1:
                    continue
                if int(id_bin[i]) != int(event_bin[i]):
                    take_event = False
                    break
                
            return take_event
            
        
        def find_triggers(event_code):
            try:
                id_, mask = map(int, event_code.split('|'))
            except ValueError:
                id_, mask = int(event_code), 0

            triggers = mne.find_events(raw)
            triggers = Events(raw).events
            triggers = filter(
                lambda trigger: should_take(id_, mask, trigger), triggers)
            return triggers
        
        min_triggers = find_triggers(event_min)
        max_triggers = find_triggers(event_max)
        
        if len(min_triggers) == 0:
            exc_messagebox(self, 'No start events found')
            return
            
        if len(max_triggers) == 0:
            exc_messagebox(self, 'No end events found')
            return

        intervals = []
        
        for idx in range(len(min_triggers)):
            min_trigger_seconds = (min_triggers[idx][0] - raw.first_samp) / raw.info['sfreq']

            
            try:
                next_max_trigger = [trigger for trigger in max_triggers 
                                    if trigger[0] > min_triggers[idx][0]][0][0]
            except IndexError:
                exc_messagebox(self, "One of the found start triggers" 
                                     "didn't have corresponding end trigger")
                return
            
            max_trigger_seconds = (next_max_trigger - raw.first_samp) / raw.info['sfreq']
            
            if max_trigger_seconds < min_trigger_seconds:
                exc_messagebox(self, "Selected events seem not be valid. Start and end events need to alternate.")
                return
            
            intervals.append((group, min_trigger_seconds, max_trigger_seconds))

        self.parent.add_intervals(intervals)
