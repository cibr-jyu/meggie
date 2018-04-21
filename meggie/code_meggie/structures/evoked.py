'''
Created on 20.2.2014

@author: jaolpeso
'''

import os

from meggie.code_meggie.general.fileManager import load_evoked

class Evoked(object):
    """
    Class for creating and handling evokeds
    """

    def __init__(self, name, subject, mne_evokeds):
        """
        Constructor
        
        Keyword arguments:
        name   -- name of the raw evoked file
        """
        self._name = name
        self._mne_evokeds = mne_evokeds
        self._path = os.path.join(subject.evokeds_directory, name)
        self._info = {}
        
    @property
    def mne_evokeds(self):
        """
        """
        if None in self._mne_evokeds.values():
            # load everything
            evokeds = load_evoked(self._path)
            for key in self._mne_evokeds:
                for evoked in evokeds:
                    if key == evoked.comment:
                        self._mne_evokeds[key] = evoked
                        break
            if None in self._mne_evokeds.keys():
                raise ValueError('Event name ' + key + 
                                 ' missing from Evoked FIF file.')
        return self._mne_evokeds

    def forget_evokeds(self):
        for key in self._mne_evokeds:
            self._mne_evokeds[key] = None

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
    def info(self):
        return self._info

    @info.setter
    def info(self, info):
        self._info = info

