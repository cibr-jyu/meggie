""" Defines Evoked class, wraps mne.Evoked objects.
"""

import os
import logging

import mne

from meggie.utilities.datatype import Datatype


class Evoked(Datatype):
    """ A wrapper for mne.Evoked objects.

    Parameters
    ----------
    name : str
        Name of the evoked, used in the UI lists and in the .exp file.
    directory : str
        Absolute path to the data folder, usually workspace/experiment/subject/evokeds.
    params : dict
        Contains additional information about the evoked.
    content : dict of mne.Evoked, optional
        Stores mne.Evoked objects as values, conditions as keys. If not provided,
        is assumed to be saved to file system earlier.
    """

    def __init__(self, name, directory, params, content=None):
        self._name = name.strip('.fif')
        self._path = os.path.join(directory, name + '.fif')
        self._params = params

        # ensure comments are set to match the keys / conditions
        self._content = content
        if self._content:
            for key in self._content.keys():
                self._content[key].comment = key

        # for backwards compatbility,
        # evokeds used to be stored in epochs/average
        if 'bwc_path' in self._params:
            self._bwc_path = os.path.join(self._params.pop('bwc_path'),
                                          self._name + '.fif')

    @property
    def content(self):
        """Returns the actual mne.Evoked objects either
        from cache or from the file system.
        """
        if self._content:
            return self._content

        self._content = {}

        # for backwards compatibility,
        # try first from the new path,
        # and then from the old path
        try:
            evokeds = mne.read_evokeds(self._path)
        except Exception:
            try:
                evokeds = mne.read_evokeds(self._bwc_path)
            except Exception:
                raise IOError('Reading evokeds failed.')

        for evoked in evokeds:
            self._content[evoked.comment] = evoked

        return self._content

    @property
    def name(self):
        """Returns name of the evoked object.
        """
        return self._name

    @property
    def params(self):
        """Returns additional information stored.
        """
        return self._params

    @property
    def ch_names(self):
        """Returns names of the data channels, must read the
        evoked to memory.
        """
        return list(self.content.values())[0].info['ch_names']

    @property
    def times(self):
        """Returns times (array of points in time), must read
        the evoked to memory.
        """
        return list(self.content.values())[0].times

    @property
    def info(self):
        """Returns info structure containing e.g. sensor locations,
        must read the evoked to memory.
        """
        return list(self.content.values())[0].info

    @property
    def data(self):
        """Returns dict of the data (numpy arrays).
        """
        data = {}
        for key in self.content.keys():
            data[key] = self.content[key].data
        return data

    def save_content(self):
        """Saves the mne.Evoked to a fif file in the evoked directory.
        """
        try:
            mne.write_evokeds(self._path, list(self.content.values()))
        except Exception as exc:
            raise Exception("Writing evokeds failed. Please check that the "
                            "entire experiment folder has write permissions.")

    def delete_content(self):
        """Deletes the fif file from the file system.
        """
        os.remove(self._path)
