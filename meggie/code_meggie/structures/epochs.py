# coding: utf-8

"""
"""
import os

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.code_meggie.general.fileManager import load_epochs

class Epochs(object):
    
    """
    A class for creating and handling epochs.
    
    """

    def __init__(self, collection_name, subject, params, raw=None):
        """
        Constructor
        """
        self._collection_name = collection_name
        self._raw = raw
        self._params = params
        self._path = os.path.join(subject.epochs_directory, collection_name + '.fif')

    @property
    def raw(self):
        """
        Returns the current working raw object.
        """
        if isinstance(self._raw, mne.EPOCHS_TYPE):
            return self._raw
        else:
            raw = self.load_working_file()
            return raw
 
    @raw.setter
    def raw(self, raw):
        """
        Sets the raw data for the epoch collection. 
        Keyword arguments:
        raw    -- the raw .fif of the collection
        """
        self._raw = raw
        
    @property
    def collection_name(self):
        """
        Returns the name of the epoch collection.
        """
        return self._collection_name

    @collection_name.setter
    def collection_name(self, collection_name):
        """
        Sets the name for the epoch collection. 
        Keyword arguments:
        collection_name    -- the name of the collection
        """
        # TODO: Add name checks, see experiment_name setter. At
        # this moment UI probably handlet interval s the name check.
        self._collection_name = collection_name
        
    @property
    def params(self):
        """
        Returns the params dictionary of the epoch collection parameters.
        """
        return self._params

    @params.setter
    def params(self, params):
        """
        Sets the parameters for the epoch collection. 
        Keyword arguments:
        params    -- dictionary of the parameters of the collection
        """
        self._params = params

    def load_working_file(self):
        if self._raw is None:
            self._raw = load_epochs(self._path)
        return self._raw

    @property
    def path(self):
        return self._path
                  
