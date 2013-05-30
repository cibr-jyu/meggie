#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
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

# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppakangas
Contains the Events-class that gets events from a raw file.
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
