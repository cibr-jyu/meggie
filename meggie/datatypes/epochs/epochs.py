# coding: utf-8

"""
"""
import os

import meggie.utilities.mne_wrapper as mne


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
        if isinstance(self._content, mne.EPOCHS_TYPE):
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

    @property
    def info(self):
        return str(self._params)

    def delete_content(self):
        try:
            os.remove(self._path)
        except OSError:
            raise IOError('Epochs could not be deleted from epochs folder.')

    def save_content(self):
        pass

