'''
Created on 20.2.2014

@author: jaolpeso
'''

import os

from PyQt4.QtCore import QObject

import mne

from meggie.code_meggie.general.fileManager import load_evoked

class Evoked(QObject):
    """
    Class for creating and handling evokeds
    """

    def __init__(self, name, subject, categories, raw=None):
        """
        Constructor
        
        Keyword arguments:
        raw    -- raw evoked file
        name   -- name of the raw evoked file
        events -- list of events in raw file
        """
        QObject.__init__(self)
        self._name = name
        self._raw = raw
        self._categories = categories
        self._path = os.path.join(subject.evokeds_directory, name)
        
    @property
    def raw(self):
        """
        Returns the raw .fif of the evoked.
        """
        if isinstance(self._raw, mne.Evoked):
            return self._raw
        else:
            raw = self.load_working_file()
            return raw
        
    @raw.setter
    def raw(self, raw):
        """
        Sets the raw data for the evoked collection.
         
        Keyword arguments:
        raw    -- the raw .fif of the collection
        """
        self._raw = raw        

    @property
    def name(self):
        """
        Returns the name of the raw file.
        """
        return self._name
    
    @name.setter
    def name(self, name):
        """
        Sets the name for the raw
        
        Keyword arguments:
        name    -- name of the evoked fif file without suffix
        """
        self._name = name
        
    @property
    def categories(self):
        """
        Returns the dictionary of categories (events in epochs which were
        averaged).
        """
        return self._categories
        
    @categories.setter
    def categories(self, categories):
        """
        Sets the categories for evoked.
        
        Keyword arguments:
        categories    -- dict() of events in epochs.event_id
        """
        self._categories = categories
        
    def load_working_file(self):
        if self._raw is None:
            self._raw = load_evoked(self._path)
        return self._raw

