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

    def __init__(self, name, spectrum_directory, params,
                 content=None, freqs=None, ch_names=None):
        """
        """
        # name has no group number and no '.fif'
        self._name = name
        self._spectrum_directory = spectrum_directory
        self._params = params

        self._content = {}
        if content is not None:
            self._content = content

        if freqs is not None:
            self._freqs = freqs
        else:
            self._freqs = None

        if ch_names is not None:
            self._ch_names = ch_names
        else:
            self._ch_names = None

    def _load_content(self):

        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.csv'
        for fname in os.listdir(self._spectrum_directory):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    raise Exception("Unknown file name format.")

                # if proper condition parameters set,
                # check if the key is in there.
                if 'conditions' in self._params:
                    if key not in [str(elem) for elem in
                                   self._params['conditions']]:
                        continue

                logging.getLogger('ui_logger').debug(
                    'Reading spectrum file: ' + str(fname))

                freqs, ch_names, psd = filemanager.load_csv(
                    os.path.join(self._spectrum_directory, fname))

                # for backwards compatibility
                # (used to have possibility to have spectrum data
                # saved as log transformed)
                if 'log_transformed' in self._params:
                    if self._params['log_transformed'] is True:
                        if np.mean(psd) < 0:
                            psd = 10 ** (psd / 10.0)

                freqs = np.array(freqs).astype(np.float)

                self._freqs = freqs
                self._ch_names = ch_names
                self._content[key] = np.array(psd)

    def save_content(self):

        # if exists, delete first
        self.delete_content()

        for key, psd in self._content.items():

            row_names = self._ch_names
            column_names = self._freqs.tolist()
            data = psd.tolist()

            path = os.path.join(self._spectrum_directory,
                                self._name + '_' + str(key) + '.csv')

            filemanager.save_csv(path, data, column_names, row_names)

    def delete_content(self):

        template = self.name + '_' + r'([a-zA-Z1-9_]+)\.csv'
        for fname in os.listdir(self._spectrum_directory):
            match = re.match(template, fname)
            if match:
                try:
                    key = str(match.group(1))
                except Exception as exc:
                    continue

                # if proper condition parameters set,
                # check if the key is in there.
                if 'conditions' in self._params:
                    if key not in [str(elem) for elem in
                                   self._params['conditions']]:
                        continue

                logging.getLogger('ui_logger').debug(
                    'Removing existing spectrum file: ' + str(fname))
                os.remove(os.path.join(self._spectrum_directory, fname))

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
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self):
        self._params = params
