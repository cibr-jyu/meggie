'''
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
'''
import mne
from Crypto.Util.py21compat import isinstance
class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, raw, events, tmin=-0.2, tmax=0.5, event_id=0):
        '''
        Constructor
        
        Keyword arguments:
        raw           -- Raw object
        events        -- Array of events
        tmin          -- Start time before event
        tmax          -- End time after the event
        event_id      -- The id of the event
        '''
        if events is None:
            raise Exception('No events given')
        if isinstance(raw, mne.fiff.raw.Raw):
            return mne.Epochs(raw, events, event_id, tmin, tmax)
        else:
            raise TypeError('Not a Raw object.')