# coding: utf-8

"""
"""

import os
import re
import logging

import numpy as np

import meggie.code_meggie.general.fileManager as fileManager

class Spectrum(object):
    
    """
    A class for creating and handling spectrums
    
    """

    def __init__(self, name, subject, log_transformed, data, freqs, ch_names):
        """
        """
        # name has no group number and no '.fif'
        self._name = name

        if not data:
            self._data = {}
        else:
            self._data = data

        self._freqs = freqs
        self._spectrums_directory = subject.spectrums_directory
        self._ch_names = ch_names
        self._log_transformed = log_transformed
   
    def _load_data(self):
        template = self.name + '_' + '([0-9]*)\.csv'
        for fname in os.listdir(self._spectrums_directory):
            match = re.match(template, fname)
            if match:
                logging.getLogger('ui_logger').debug(
                    'Reading spectrum file: ' + str(fname))
                try:
                    key = int(match.group(1))
                except Exception as exc:
                    raise Exception("Unknown file name format.")
                freqs, ch_names, psd = fileManager.load_csv(
                    os.path.join(self._spectrums_directory, fname))

                freqs = np.array(freqs).astype(np.float)

                self._ch_names = ch_names
                self._freqs = np.array(freqs)
                self._data[key] = np.array(psd)

    def save_data(self):

        # if exists, delete first 
        self.delete_data()

        for key, psd in self.data.items():

	    row_names = self._ch_names
	    column_names = self._freqs.tolist()
	    data = psd.tolist()

            path = os.path.join(self._spectrums_directory, 
                                self.name + '_' + str(key) + '.csv')
 
            fileManager.save_csv(path, data, column_names, row_names)

    def delete_data(self):
        template = self.name + '_' + '[0-9]*\.csv'
        for fname in os.listdir(self._spectrums_directory):
            if re.match(template, fname):
                logging.getLogger('ui_logger').debug(
                    'Removing existing spectrum file: ' + str(fname))
                os.remove(os.path.join(self._spectrums_directory, fname))


    @property
    def data(self):
        if not self._data:
            self._load_data()

        return self._data
            
    @property
    def freqs(self):
        if self._freqs is None:
            self._load_data()

        return self._freqs

    @property
    def ch_names(self):
        if self._ch_names is None:
            self._load_data()

        return self._ch_names

    @property
    def name(self):
        return self._name

    @property
    def log_transformed(self):
        return self._log_transformed


