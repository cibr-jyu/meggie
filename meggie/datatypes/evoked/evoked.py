"""
"""

import os
import logging

import mne


class Evoked(object):
    """
    """

    def __init__(self, name, evoked_directory, params={}, content=None):
        """
        """
        self._name = name.strip('.fif')
        self._path = os.path.join(evoked_directory, name + '.fif')
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
        """
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

    def save_content(self):
        """
        """
        try:
            mne.write_evokeds(self._path, list(self.content.values()))
        except Exception as exc:
            logging.getLogger('ui_logger').exception('')
            raise IOError('Writing evokeds failed')

    def delete_content(self):
        os.remove(self._path)
