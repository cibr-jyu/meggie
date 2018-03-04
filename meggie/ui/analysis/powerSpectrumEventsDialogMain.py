'''
Created on 17.10.2016

@author: jaolpeso, erpipehe
'''
import logging

from PyQt4 import QtGui

from meggie.ui.analysis.powerSpectrumEventsUi import Ui_Advanced 
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.epoching.bitSelectionDialogMain import BitSelectionDialog

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
            event_end = self.ui.lineEditEnd.text()
            group = int(self.ui.comboBoxAvgGroup.currentText())

            if not event_min or not event_end:
                raise Exception("No min and end events set")
        except:
            exc_messagebox(self, "Please check your inputs")
            return

        raw = self.parent.experiment.active_subject.get_working_file()
        
        def find_triggers(event_code):
            try:
                id_, mask = map(int, event_code.split('|'))
            except ValueError:
                id_, mask = int(event_code), 0

            subject = self.parent.experiment.active_subject
            triggers = Events(self.parent.experiment, raw,
                              stim_ch=subject.find_stim_channel(),
                              mask=mask, id_=id_).events

            return triggers
        
        logging.getLogger('ui_logger').debug("Finding min triggers")
        min_triggers = find_triggers(event_min)
        logging.getLogger('ui_logger').debug("Finding end triggers")
        end_triggers = find_triggers(event_end)
        
        if len(min_triggers) == 0:
            exc_messagebox(self, 'No start events found')
            return
            
        if len(end_triggers) == 0:
            exc_messagebox(self, 'No end events found')
            return

        intervals = []
        
        for idx in range(len(min_triggers)):
            min_trigger_seconds = (min_triggers[idx][0] - raw.first_samp) / raw.info['sfreq']

            
            try:
                next_end_trigger = [trigger for trigger in end_triggers 
                                    if trigger[0] > min_triggers[idx][0]][0][0]
            except IndexError:
                exc_messagebox(self, "One of the found start triggers" 
                                     "didn't have corresponding end trigger")
                return
            
            end_trigger_seconds = (next_end_trigger - raw.first_samp) / raw.info['sfreq']
            
            if end_trigger_seconds < min_trigger_seconds:
                exc_messagebox(self, "Selected events seem not be valid. Start and end events need to alternate.")
                return
            
            intervals.append((group, min_trigger_seconds, end_trigger_seconds))

        self.parent.add_intervals(intervals)
