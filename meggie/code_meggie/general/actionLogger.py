"""
Created on 26.11.2015

@author: Janne Pesonen
"""
import os
import logging
from logging.handlers import RotatingFileHandler

class ActionLogger(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor
        """
        #copied stuff from MNE-Python utils.py
        self._logger = None  #logging.getLogger('meggie')  # one selection here used across Meggie
        #self._logger.propagate = False  # don't propagate (in case of multiple imports)
        self._actionCounter = 1;
        self._notifications = []
        #self.initialize_logger()
        
    @property
    def logger(self):
        """
        Returns the logger.
        """
        return self._logger
    
    @logger.setter
    def logger(self, logger):
        self._logger = logger
    
        
    def initialize_logger(self, path):
        """Initializes the logger and adds a handler to it that handles writing and formatting
        the logs to a file.
        
        Keyword arguments
        path     -- path to save the log file
        """
        #TODO: If you use FileHandler for writing logs, the size of log file will grow with time.
        #Someday, it will occupy all of your disk. In order to avoid that situation, you should
        #use RotatingFileHandler instead of FileHandler in production environment.
        self._logger = logging.getLogger(path)
        handler = logging.FileHandler(os.path.join(path, 'meggie.log'))
        #handler = RotatingFileHandler(os.path.join(path, 'meggie.log'))
        handler.setLevel(logging.INFO)
        
        #see: https://docs.python.org/2/library/logging.html#logrecord-attributes
        formatter = logging.Formatter('%(asctime)s - %(message)s', '%Y-%m-%d %H:%M:%S')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        
    def log_message(self, msg):
        """
        Logs given messages.
        TODO: let user write messages in Meggie to log them using this function
              perhaps better create log_user_message method instead for unique separation
        
        Keyword arguments
        msg
        """
        self._logger.info('------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        self._logger.info(msg)
        
    def log_outcome(self, outcome):
        self._logger.info(outcome)
