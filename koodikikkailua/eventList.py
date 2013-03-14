#!/usr/bin/env python
#coding: utf8 
"""
Created on Mar 12, 2013

@author: Jaakko Leppäkangas
"""
import mne
import os

class MyClass(object):
    """
    classdocs
    """


    def __init__(self, eveFile):
        """
        Constructor
        
        Keyword arguments:
        eveFile       -- Event file.
        """
        if os.path.isfile(eveFile):
            return mne.find_events(eveFile)