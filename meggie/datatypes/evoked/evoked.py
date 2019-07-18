"""
"""

import os


class Evoked(object):
    """
    """
    def __init__(self, name, evoked_directory, params, content=None):
        """
        """
        self._name = name
        self._content = content
        self._path = os.path.join(evoked_directory, name)
        self._params = params

        # for backwards compatbility, 
        # evokeds used to be stored in epochs/average
        if 'bwc_path' in self._params:
            self._bwc_path = os.path.join(self._params.pop('bwc_path'),
                                          name)

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

        for key in self._params['event_names']:
            for evoked in evokeds:
                if key == evoked.comment:
                    self._content[key] = evoked
                    break

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
    def info(self):
        return str(self._params)
    
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
        pass

    def delete_content(self):
        os.remove(self._path)
        

