# coding: utf-8

"""
"""
import os

import mne


class Epochs:
    """
    """

    def __init__(self, name, epochs_directory, params, content=None):
        """
        """
        self._name = name
        self._content = content
        self._params = params
        self._path = os.path.join(epochs_directory, name + '.fif')

    @property
    def content(self):
        """
        """
        if self._content is not None:
            return self._content
        else:
            try:
                return mne.read_epochs(self._path)
            except IOError:
                raise Exception('Reading epochs failed.')

    @content.setter
    def content(self, content):
        """
        """
        self._content = content

    @property
    def name(self):
        """
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        """
        self._name = name

    @property
    def params(self):
        """
        """
        return self._params

    @params.setter
    def params(self, params):
        """
        """
        self._params = params

    @property
    def path(self):
        return self._path

    def delete_content(self):
        os.remove(self._path)

    def save_content(self):
        self._content.save(self._path)
