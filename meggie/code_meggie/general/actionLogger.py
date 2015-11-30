"""
Created on 26.11.2015

@author: Janne Pesonen
"""
import os
import logging

#from meggie.code_meggie.general.caller import Caller

    #logger = logging.getLogger('mne')
    #mne.utils.set_log_file('reallogs.log', '%(message)', None)  
    #mne.utils.set_log_level('INFO')
    
    # TODO: new logging system for Meggie
    #logger = logging.getLogger('meggie')  # one selection here used across mne-python
    #logger.propagate = False  # don't propagate (in case of multiple imports)
    #logging.basicConfig(filename='reallogs.log', format='%(levelname)s:%(message)s', level=logging.DEBUG)
    #logging.info('Config file in path: ' + mne.get_config_path())




class ActionLogger(object):
    """
    classdocs
    """


    def __init__(self, params):
        """
        Constructor
        """
        #copied stuff from MNE-Python utils.py
        self._logger = logging.getLogger('meggie')  # one selection here used across Meggie
        self._logger.propagate = False  # don't propagate (in case of multiple imports)
        self._actionCounter = 1;
        
    @property
    def logger(self):
        """
        Returns the logger.
        """
        return self._logger
        
    def initialize_logger(self, path):
        """Initializes the logger and adds a handler to it that handles writing and formatting
        the logs to a file.         
        """
        #TODO: try JSON or YAML
        #TODO: If you use FileHandler for writing logs, the size of log file will grow with time.
        #Someday, it will occupy all of your disk. In order to avoid that situation, you should
        #use RotatingFileHandler instead of FileHandler in production environment.
        handler = logging.FileHandler('log.log')
        handler.setLevel(logging.INFO)
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        
        
    def log_params(self, function_name, params, msg):
        """
        
        """
        self._logger.info('----------')
        self._logger.info('>' + self._actionCounter)
        self._logger.info(function_name + ': ' + msg)
        for key, value in params.items():
            self._logger.info(str(key) + ',' + str(value))
        self._actionCounter += 1
        
    def log_success(self, function_name, params):
        msg = 'The action was successful.'
        self.log_params(function_name, params, msg)
        
    def log_error(self, function_name, params, error):
        msg = 'The action was not successful. It raised the following ERROR: ' + error
        self.log_params(function_name, params, msg)
        
    def log_warning(self, function_name, params, warning):
        msg = 'The action was successful, but it raised the following WARNING: ' + warning
        self.log_params(function_name, params, msg)
        
        
        
        