# coding: utf-8

"""
"""

import os
import re
import logging

import meggie.code_meggie.general.mne_wrapper as mne

class TFR(object):
    
    """
    A class for creating and handling TFR's
    
    """

    def __init__(self, tfrs, name, subject, decim, n_cycles, 
                 evoked_subtracted):
        """
        """
        self._tfrs = tfrs
        self._name = name
        self._tfr_directory = subject.tfr_directory
        self._decim = decim
        self._n_cycles = n_cycles
        self._evoked_subtracted = evoked_subtracted

    def _get_fname(self, tfr_name):
        # for backward compatibility
        if tfr_name == '':
            name = self._name + '-tfr.h5'
        else:
            name = self._name + '-' + tfr_name + '-tfr.h5'

        fname = os.path.join(self._tfr_directory, 
                             name)
        return fname


    def save_tfr(self):
        for tfr_name, tfr in self._tfrs.items():
            fname = self._get_fname(tfr_name)
            tfr.save(fname, overwrite=True)

    def delete_tfr(self):
        if not self._tfrs:
            return

        for tfr_name, tfr in self._tfrs.items():
            fname = self._get_fname(tfr_name)
            os.remove(fname)

    def _load_tfrs(self):
        self._tfrs = {}
        template = self._name + '-' + '([a-zA-Z1-9_]+)\-tfr\.h5'
        for fname in os.listdir(self._tfr_directory):
            path = None
            if fname == self._name + '-tfr.h5':
                path = os.path.join(self._tfr_directory, fname)
                key = ''
            else:
                match = re.match(template, fname)
                if match:
                    try:
                        key = str(match.group(1))
                    except Exception as exc:
                        raise Exception("Unknown file name format.")

                    path = os.path.join(self._tfr_directory, 
                                        fname)
            if path:
                logging.getLogger('ui_logger').debug(
                    'Reading tfr file: ' + str(path))

                self._tfrs[key] = mne.read_tfrs(path)[0]

    @property
    def tfrs(self):
        if self._tfrs is None:
            self._load_tfrs()
        return self._tfrs

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
