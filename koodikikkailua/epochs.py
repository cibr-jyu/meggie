#!/usr/bin/env python
# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne

import eventList

class Epochs(object):
    """
    classdocs
    """


    def __init__(self, raw, stim_channel, meg, eeg, stim, eog, reject, tmin=-0.2, tmax=0.5, event_id=0):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        events        -- Array of events
        tmin          -- Start time before event (default -0.2)
        tmax          -- End time after the event (default 0.5)
        event_id      -- The id of the event (default 0)
        """
        if isinstance(raw, mne.fiff.raw.Raw):
            events = eventList.Events(raw, stim_channel)
            picks = mne.fiff.pick_types(raw.info, meg=meg, eeg=eeg,
                                        stim=stim, eog=eog)
            #self.e = epochs.Epochs(raw, events.events, picks, float(tmin),
            #                       float(tmax), int(event_id))
            self.epochs = mne.Epochs(raw, events.events, event_id, tmin, tmax, picks=picks)
            #self.logger = Logger()
        else:
            raise TypeError('Not a Raw object.')
        
    def average(self):
        """
        Average epochs.
        """
        self.evoked = self.epochs.average()
        return self.evoked