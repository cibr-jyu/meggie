#!/usr/bin/env python
# coding: latin1
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne

class Events(object):
    """
    classdocs
    """


    def __init__(self, raw, stim_ch):
        """
        Constructor
        """
        self.events = mne.find_events(raw, stim_channel=stim_ch)
        #if os.path.isfile(eveFile):
        #    self.events = mne.read_events(eveFile)
        
        
