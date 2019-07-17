# coding: utf-8

"""
"""

import os
import re
import logging

import numpy as np

import meggie.utilities.fileManager as fileManager


class Spectrum(object):

    """
    """
    def __init__(self, name, spectrum_directory, params, content=None):
        """
        """
        # name has no group number and no '.fif'
        self._name = name

        if not content:
            self._content = {}
        else:
            self._content = content

        self._spectrums_directory = spectrums_directory

        self._params = params

    def _load_content(self):
        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.csv'
        for fname in os.listdir(self._spectrums_directory):
            match = re.match(template, fname)
            if match:
                logging.getLogger('ui_logger').debug(
                    'Reading spectrum file: ' + str(fname))
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    raise Exception("Unknown file name format.")

                freqs, ch_names, psd = fileManager.load_csv(
                    os.path.join(self._spectrums_directory, fname))

                freqs = np.array(freqs).astype(np.float)

                self._content[key] = np.array(psd)

    def save_content(self):

        # if exists, delete first
        self.delete_content()

        for key, psd in self.content.items():

            row_names = self._ch_names
            column_names = self._freqs.tolist()
            data = psd.tolist()

            path = os.path.join(self._spectrums_directory,
                                self.name + '_' + str(key) + '.csv')

            fileManager.save_csv(path, data, column_names, row_names)

    def delete_content(self):
        template = self.name + '_' + r'[0-9]*\.csv'
        for fname in os.listdir(self._spectrums_directory):
            if re.match(template, fname):
                logging.getLogger('ui_logger').debug(
                    'Removing existing spectrum file: ' + str(fname))
                os.remove(os.path.join(self._spectrums_directory, fname))

    @property
    def content(self):
        if not self._content:
            self._load_content()

        return self._content

    @property
    def freqs(self):
        return self._params['freqs']

    @property
    def ch_names(self):
        return self._params['ch_names']

    @property
    def log_transformed(self):
        return self._params['log_transformed']

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self):
        self._params = params


