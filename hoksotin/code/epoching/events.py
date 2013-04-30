# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne

class Events(object):

    def __init__(self, raw, stim_ch):
        """
        Constructor
        
        Keyword arguments:
        raw           -- A raw object
        stim_ch       -- Name of the stimulus channel
        """
        print raw.info.get('filename')
        self._events = mne.find_events(raw, stim_channel=stim_ch) #, stim_channel=stim_ch)
        #if os.path.isfile(eveFile):
        #    self.events = mne.read_events(eveFile)
        
    @property    
    def events(self):
        return self._events
