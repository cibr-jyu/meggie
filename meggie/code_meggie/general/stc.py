'''
Created on 6.3.2018

@author: erpipehe
'''

import os

import numpy as np

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

    def save(self, experiment):
        pass

    def load(self, experiment):
        pass

    def get_data(self, experiment):
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

    def save(self, experiment):
        path = os.path.join(experiment.active_subject.stc_directory, self.name)
        if not os.path.exists(path):
            os.makedirs(path)

        fname = experiment.active_subject.working_file_name.split('.fif')[0]
        self._stc.save(os.path.join(path, fname))

    def load(self, experiment):
        path = os.path.join(experiment.active_subject.stc_directory, self.name)
        fname = experiment.active_subject.working_file_name.split('.fif')[0]
        self._stc = mne.read_source_estimate(os.path.join(path, fname))
        return self._stc

    def get_data(self, experiment):
        if self._stc:
            return self._stc
        else:
            # load from files
            return self.load(experiment)


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

    def save(self, experiment):
        path = os.path.join(experiment.active_subject.stc_directory, self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        for idx, stc in enumerate(self._stcs):
            # use number as filename (and pad proper amount of zeros)
            fname = str(idx).zfill(int(np.ceil(np.log10(len(self._stcs)+1))) + 1)
            stc.save(os.path.join(path, fname))

    def load(self, experiment):
        path = os.path.join(experiment.active_subject.stc_directory, self.name)
        fnames = os.listdir(path)
        keys = sorted(list(set([fname.split('-')[0] for fname in fnames])))
        self._stcs = []
        for key in keys:
            stc = mne.read_source_estimate(os.path.join(path, key))
            self._stcs.append(stc)
        return self._stcs

    def get_data(self, experiment):
        if self._stcs:
            return self._stcs
        else:
            # load from files
            return self.load(experiment)



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

    def keys(self):
        return self._stcs.keys()

    def save(self, experiment):
        path = os.path.join(experiment.active_subject.stc_directory, self.name)
        if not os.path.exists(path):
            os.makedirs(path)
        for key, stc in self._stcs.items():
            stc.save(os.path.join(path, key))

    def load(self, experiment):
        path = os.path.join(experiment.active_subject.stc_directory, self.name)
        keys = self.keys()
        for key in keys:
            self._stcs[key] = mne.read_source_estimate(os.path.join(path, key))
        return self._stcs

    def get_data(self, experiment):
        if len(filter(bool, self._stcs.values())) == len(self._stcs):
            return self._stcs
        else:
            # load from files
            return self.load(experiment)

