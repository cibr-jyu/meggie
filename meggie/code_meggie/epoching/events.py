# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 12, 2013

@author: Jaakko Leppakangas
Contains the Events-class that gets events from a raw file.
"""
import mne
import numpy as np
from meggie.code_meggie.general.wrapper import wrap_mne_call

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

        #events = mne.find_events(raw, stim_channel=stim_ch, shortest_event=1, uint_cast=True)
        events = wrap_mne_call(experiment, mne.find_events, raw,
            stim_channel=stim_ch, shortest_event=1, uint_cast=True,
            verbose='warning')
        
        if mask or id_:
            events = filter(
                lambda event: self._should_take(id_, mask, event), events)
            events = np.array(events)

        # remove spurious events
        counter = 0
        for idx in reversed(range(1, len(events))):
            if events[idx][0] - events[idx-1][0] < 2:
                events = np.delete(events, idx-1, axis=0)
                counter += 1

        if counter > 0:
            print str(counter) + " events dropped because they seem spurious (only one sample difference to next event)"

        print str(len(events)) + " events found."
        
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
