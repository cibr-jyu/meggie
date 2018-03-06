'''
Created on 6.3.2018

@author: erpipehe
'''

import os

import meggie.code_meggie.general.mne_wrapper as mne

class SourceEstimate(object):
    """ Abstract class for source estimates
    """
    def __init__(self, name):
        self._name = name
        self._type = None

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
    def type(self):
        """
        """
        return self._type
    
    @type.setter
    def type(self, type_):
        """
        """
        self._type = type_

    def save(self):
        pass

    def load(self):
        pass

    def get_data(self):
        pass

class SourceEstimateRaw(SourceEstimate):
    """
    Class for storing raw source estimates
    """

    def __init__(self, name, stc=None):
        """
        """
        super(SourceEstimateRaw, self).__init__(name)
        self._stc = stc
        self._type = 'raw'

    def save(self):
        pass

    def load(self):
        pass

    def get_data():
        if self._stc:
            return self._stc
        else:
            # load from files
            return self.load()


class SourceEstimateEpochs(SourceEstimate):
    """
    Class for storing epochs source estimates
    """

    def __init__(self, name, stcs=None):
        """
        """
        super(SourceEstimateEpochs, self).__init__(name)
        self._stcs = stcs
        self._type = 'epochs'

    def save(self):
        pass

    def load(self):
        pass

    def get_data(self):
        if self._stcs:
            return self._stcs
        else:
            # load from files
            return self.load()



class SourceEstimateEvoked(SourceEstimate):
    """
    Class for storing evoked source estimates
    """

    def __init__(self, name, stcs=None):
        """
        """
        super(SourceEstimateEvoked, self).__init__(name)
        self._stcs = stcs
        self._type = 'evoked'

    def save(self):
        pass

    def load(self):
        pass

    def get_data(self):
        if self._stcs:
            return self._stcs
        else:
            # load from files
            return self.load()

