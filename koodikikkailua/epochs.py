#!/usr/bin/env python
# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne

class Epochs(object):
    """
    classdocs
    """


    def __init__(self, raw, events, p, tmin=-0.2, tmax=0.5, event_id=0):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        events        -- Array of events
        tmin          -- Start time before event (default -0.2)
        tmax          -- End time after the event (default 0.5)
        event_id      -- The id of the event (default 0)
        """
        if events is None:
            raise Exception('No events given.')
        if isinstance(raw, mne.fiff.raw.Raw):
            self.epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=p)
            
        else:
            raise TypeError('Not a Raw object.')
        
    def average(self):
        """
        Average epochs.
        """
        self.evoked = self.epochs.average()
        return self.evoked