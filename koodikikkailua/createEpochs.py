'''
Created on Mar 21, 2013

@author: jaeilepp
'''
import mne
import pylab as pl

import epochs
import eventList

class CreateEpochs(object):
    '''
    classdocs
    '''


    def __init__(self, raw, event_id, stim_channel, tmin, tmax, reject,
                 meg, eeg, stim, eog):
        '''
        Constructor
        '''
        events = eventList.Events(raw, stim_channel)
        picks = mne.fiff.pick_types(raw.info, meg=meg, eeg=eeg, stim=stim,
                                    eog=eog)
        e = epochs.Epochs(raw, events.events, picks, float(tmin), float(tmax),
                          int(event_id))
        
        evoked = e.average()
        evoked.plot()