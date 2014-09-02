'''
Created on 1.7.2014

@author: Kari Aliranta

Module for code related to creating and handling forward models via
mne_setup_source_space, mne_watershed_bem and mne_setup_forward_model.

'''

from PyQt4.QtCore import QObject

class ForwardModels(QObject):

    def __init__(self):
        """
        Constructor
        """
        QObject.__init__(self)
        self._fmodel_name = ''
        self._params = dict()
        
        
    