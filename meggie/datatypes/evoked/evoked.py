"""
"""

import os

from meggie.utilities.fileManager import load_evoked


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

    @property
    def content(self):
        """
        """
        if None in self._content.values():
            # load everything
            evokeds = load_evoked(self._path)
            for key in self._content:
                for evoked in evokeds:
                    if key == evoked.comment:
                        self._content[key] = evoked
                        break
            if None in self._content.keys():
                raise ValueError('Event name ' + key +
                                 ' missing from Evoked FIF file.')
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
    
    @proprty
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
        

