'''
Created on Mar 21, 2013

@author: jaeilepp
'''
import mne
import pylab as pl

import epochs
import events

class CreateEpochs(object):
    """
    Creates Epochs from the raw data.
    
    Parameters:
    
    raw            Raw object.
    event_id       The event from which epochs are created.
    stim_channel   The channel in the raw data containing the events.
    tmin           Start time before event.
    tmax           End time after event.
    reject         Dictionary containing the channels to be rejected.
    meg            If true, include meg channels.
    eeg            If true, include eeg channels.
    stim           If true, include stimulus channels.
    eog            If true, include eog channels.    
    """


    def __init__(self, raw, event_id, stim_channel, tmin, tmax, reject,
                 meg, eeg, stim, eog):
        '''
        Constructor
        '''
        events = events.Events(raw, stim_channel)
        picks = mne.fiff.pick_types(raw.info, meg=meg, eeg=eeg, stim=stim,
                                    eog=eog)
        e = epochs.Epochs(raw, events.events, picks, float(tmin), float(tmax),
                          int(event_id))
        
        evoked = e.average()
        evoked.plot()