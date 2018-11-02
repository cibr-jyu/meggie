# coding: utf-8

"""
"""

import logging

import numpy as np
import meggie.code_meggie.general.mne_wrapper as mne

class Events(object):
    """
    Class for getting events from the raw file, by type if need be.
    """

    def __init__(self, experiment, raw, stim_ch=None, mask=0, id_=None):
        """
        Constructor    
        Keyword arguments:
        raw           -- A raw object
        stim_ch       -- Name of the stimulus channel
        mask          -- Mask for excluding bits.
        """

        events = mne.find_events(raw, stim_channel=stim_ch, shortest_event=1, 
                                 uint_cast=True)
        
        if mask or id_:
            events = list(filter(
                lambda event: self._should_take(id_, mask, event), events))
            events = np.array(events)

        # remove spurious events
        counter = 0
        for idx in reversed(range(1, len(events))):
            if events[idx][0] - events[idx-1][0] < 2:
                events = np.delete(events, idx-1, axis=0)
                counter += 1

        if counter > 0:
            message = (str(counter) + 
                       " events dropped because they seem spurious "
                       "(only one sample difference to next event)")
            logging.getLogger('ui_logger').warning(message)

        self._events = events
        
    def _should_take(self, id_, mask, event):
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
    
    @property    
    def events(self):
        """
        Property for events.
        """
        return self._events
