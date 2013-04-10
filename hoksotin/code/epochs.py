# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne

import eventList

class Epochs(object):
    """
    A class for epochs created from the MEG data.
    """


    def __init__(self, raw, stim_channel, mag, grad, eeg, stim,
                 eog, reject, tmin=-0.2, tmax=0.5, event_id=0):
        """
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        events        -- Array of events
        tmin          -- Start time before event (default -0.2)
        tmax          -- End time after the event (default 0.5)
        event_id      -- The id of the event (default 0)
        Raises TypeError if the raw object isn't of type mne.fiff.Raw.
        Raises Exception if no stimulus channel given or picks are empty.
        """
        if stim_channel is None:
            raise Exception('No stimulus channel found.')
        if mag and grad:
            meg = True
        elif mag:
            meg = 'mag'
        elif grad:
            meg = 'grad'
        if isinstance(raw, mne.fiff.raw.Raw):
            events = eventList.Events(raw, stim_channel)
            picks = mne.fiff.pick_types(raw.info, meg=meg, eeg=eeg,
                                        stim=stim, eog=eog)
            if picks is None:
                raise Exception('Picks cannot be empty.')
            self.epochs = mne.Epochs(raw, events.events, event_id,
                                     tmin, tmax, picks=picks)
        else:
            raise TypeError('Not a Raw object.')
        
    def average(self):
        """
        Average epochs. Returns evoked data.
        Raises an exception if cannot find any epochs.
        """
        if self.epochs is None:
            raise Exception('No epochs found.')
        self.evoked = self.epochs.average()
        return self.evoked