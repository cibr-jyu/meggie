'''
Created on 20.2.2014

@author: jaolpeso
'''

from PyQt4.QtCore import QObject

import mne


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
        
        # Useless?
        #self._events = []
        
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
    def events(self):
        """
        Returns the list of events.
        """
        return self._events
        
    @events.setter
    def events(self, events):
        """
        Sets the events for evoked.
        
        Keyword arguments:
        events    -- can be given list of setno names
        """
        # TODO: just a fast construction of probably useless code
        if events is None:
            pass
        else:
            for setno in events:
                self._events.append(setno)
            return
                
        for setno in self._raw.setno(names):
            self._events.append(setno)
        