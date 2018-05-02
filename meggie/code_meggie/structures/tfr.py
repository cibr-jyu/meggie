# coding: utf-8

"""
"""

import os

import meggie.code_meggie.general.mne_wrapper as mne

class TFR(object):
    
    """
    A class for creating and handling TFR's
    
    """

    def __init__(self, tfr, name, subject, decim, n_cycles, evoked_subtracted):
        """
        """
        self._tfr = tfr
        self._name = name
        self._tfr_directory = subject.tfr_directory
        self._decim = decim
        self._n_cycles = n_cycles
        self._evoked_subtracted = evoked_subtracted

    def save_tfr(self):
        fname = os.path.join(self._tfr_directory, 
                             self._name + '-tfr.h5')
        self._tfr.save(fname, overwrite=True)

    def delete_tfr(self):
        fname = os.path.join(self._tfr_directory, 
                             self._name + '-tfr.h5')
        os.remove(fname)

    def _load_tfr(self):
        fname = os.path.join(self._tfr_directory, 
                             self._name + '-tfr.h5')
        self._tfr = mne.read_tfrs(fname)[0]

    @property
    def tfr(self):
        if not self._tfr:
            self._load_tfr()
        return self._tfr

    @property
    def name(self):
        return self._name

    @property
    def decim(self):
        return self._decim

    @property
    def n_cycles(self):
        return self._n_cycles

    @property
    def evoked_subtracted(self):
        return self._evoked_subtracted
