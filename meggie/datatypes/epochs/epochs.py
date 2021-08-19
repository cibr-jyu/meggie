""" Defines Epochs class, wraps mne.Epochs objects.
"""
import os
import logging

import mne

from meggie.utilities.datatype import Datatype


class Epochs(Datatype):
    """ A wrapper for mne.Epochs objects.

    Parameters
    ----------
    name : str
        Name of the epochs, used in the UI lists and in the .exp file.
    directory : str
        Absolute path to the data folder, usually workspace/experiment/subject/epochs.
    params : dict
        Contains additional information about the epochs, 
        such as the events used in the construction
    content : instance of mne.Epochs, optional
        A mne.Epochs object. If not provided, is assumed to be
        saved to file system earlier.
    """

    def __init__(self, name, directory, params, content=None):
        self._name = name
        self._content = content
        self._params = params
        self._path = os.path.join(directory, name + '.fif')

    @property
    def content(self):
        """Returns the actual mne.Epochs, either from cache or
        from the file system.
        """
        if self._content is not None:
            return self._content
        else:
            try:
                self._content = mne.read_epochs(self._path)
                return self._content
            except IOError:
                raise Exception('Reading epochs failed.')

    @property
    def name(self):
        """Returns the name of the collection.
        """
        return self._name

    @property
    def count(self):
        """Return the number of epochs in the collection.
        """
        return len(self.content.events)

    @property
    def params(self):
        """Returns additional information stored.
        """
        return self._params

    def delete_content(self):
        """Deletes the fif file from the files system
        """
        os.remove(self._path)

    def save_content(self):
        """Saves the mne.Epochs to a fif file in the epochs
        directory """
        try:
            self._content.save(self._path, overwrite=True)
        except Exception as exc:
            raise Exception("Writing epochs failed. Please ensure that "
                            "the entire experiment folder has write permissions")

