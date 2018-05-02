# coding: utf-8

"""
"""

import os

import meggie.code_meggie.general.mne_wrapper as mne

class TFR(object):
    
    """
    A class for creating and handling TFR's
    
    """

    def __init__(self, tfr, name, subject, decim, n_cycles):
        """
        """
        self._tfr = tfr
        self._name = name
        self._tfr_directory = subject.tfr_directory
        self._decim = decim
        self._n_cycles = n_cycles

    def save_data(self):
        from meggie.code_meggie.utils.debug import debug_trace;
        debug_trace()
        print "miau"

    def delete_data(self):
        pass

    def _load_data(self):
        pass

    @property
    def data(self):
        pass

    @property
    def decim(self):
        return self._decim

    @property
    def n_cycles(self):
        return self._n_cycles
