# coding: latin1
"""
Created on Mar 13, 2013

@author: Jaakko Leppäkangas
"""
import mne

import os

class File(object):
    """
    A class for file operations.
    """


    def __init__(self):
        pass 
        
    def open_raw(self, fname):
        """
        Opens a raw file.
        
        
        Keyword arguments:
        fname         -- A file to open
        Raises an exception if the file cannot be opened.
        """
        if os.path.isfile(fname):# and fname.endswith('fif'):
            return mne.fiff.Raw(fname, preload=True)
            #self.raw = mne.fiff.Raw(str(fname))
        else:
            raise Exception('Could not open file.')