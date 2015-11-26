"""
Created on 26.11.2015

@author: Janne Pesonen
"""
import os
import logging

from meggie.code_meggie.general.caller import Caller

    #logger = logging.getLogger('mne')
    #mne.utils.set_log_file('reallogs.log', '%(message)', None)  
    #mne.utils.set_log_level('INFO')
    
    # TODO: new logging system for Meggie
    #logger = logging.getLogger('meggie')  # one selection here used across mne-python
    #logger.propagate = False  # don't propagate (in case of multiple imports)
    #logging.basicConfig(filename='reallogs.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
    #logging.info('Config file in path: ' + mne.get_config_path())




class WorkFlowLogger(object):
    """
    classdocs
    """


    def __init__(self, params):
        """
        Constructor
        """
        self._logger = logging.getLogger('meggie')  # one selection here used across Meggie
        self._handler = logging.FileHandler('reallog.log')
        caller = Caller.Instance()

    @property
    def logger(self):
        """
        Method for getting activated subject.
        """
        return self._logger
        
    def initialize_logger(self):
        handler = logging.FileHandler(os.path.join(self.caller.experiment._active_subject_name, 'log.log'))
        self._logger.propagate = False  # don't propagate (in case of multiple imports)
        
        