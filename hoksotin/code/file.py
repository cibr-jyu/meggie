#!/usr/bin/env python
#coding: utf8 
"""
Created on Mar 13, 2013

@author: Jaakko Leppäkangas
"""
import mne
import os

class File(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
        
        
    def open_raw(self, fname):
        """
        Opens a raw file.
        
        
        Keyword arguments:
        fname         -- A file to open
        """
        if os.path.isfile(str(fname)) and str(fname).endswith('fif'):
            return mne.fiff.Raw(str(fname))
            #self.raw = mne.fiff.Raw(str(fname))
        else:
            raise Exception('Could not open file.')