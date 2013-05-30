# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppakangas
"""
import mne

class Events(object):
    """
    Class for getting events from the raw file, by type if need be.
    """

    def __init__(self, raw, stim_ch):
        """
        Constructor    
        Keyword arguments:
        raw           -- A raw object
        stim_ch       -- Name of the stimulus channel
        """
        print raw.info.get('filename')
        self._events = mne.find_events(raw, stim_channel=stim_ch)
        
    @property    
    def events(self):
        """
        Property for events.
        """
        return self._events
    
    def pick(self, event_id):
        """
        Method for picking events with selected id.
        Keyword arguments:
        event_id      -- Id of the event.
        Raises an exception if the events haven't been initialized.
        """
        if self._events is None:
            raise Exception('No events found.')
        self._events = mne.pick_events(self._events, include=event_id)
