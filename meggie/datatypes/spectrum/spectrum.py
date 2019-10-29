# coding: utf-8

"""
"""

import os
import re
import logging

import numpy as np

import meggie.utilities.filemanager as filemanager


class Spectrum(object):

    """
    """
    def __init__(self, name, spectrums_directory, params, content=None):
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

        from meggie.utilities.debug import debug_trace;
        debug_trace()

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

                freqs, ch_names, psd = filemanager.load_csv(
                    os.path.join(self._spectrums_directory, fname))

                freqs = np.array(freqs).astype(np.float)

                self._freqs = freqs
                self._ch_names = ch_names
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

            filemanager.save_csv(path, data, column_names, row_names)

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
        if not self._content:
            self._load_content()
        return self._freqs

    @property
    def ch_names(self):
        if not self._content:
            self._load_content()
        return self._ch_names

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


