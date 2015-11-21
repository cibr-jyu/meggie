'''
Created on 20.2.2014

@author: jaolpeso
'''

from PyQt4.QtCore import QObject


class Evoked(QObject):
    """
    Class for creating and handling evokeds
    """

    def __init__(self):
        """
        Constructor
        
        Keyword arguments:
        raw    -- raw evoked file
        name   -- name of the raw evoked file
        events -- list of events in raw file
        """
        QObject.__init__(self)
        self._name = ''
        self._raw = None
        self._categories = dict()
        
    @property
    def raw(self):
        """
        Returns the raw .fif of the evoked.
        """
        return self._raw

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
