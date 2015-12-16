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
        #TODO: try JSON or YAML
        #TODO: If you use FileHandler for writing logs, the size of log file will grow with time.
        #Someday, it will occupy all of your disk. In order to avoid that situation, you should
        #use RotatingFileHandler instead of FileHandler in production environment.
        #home = expanduser("~")
        self._logger = logging.getLogger(path)
        handler = logging.FileHandler(os.path.join(path, 'meggie.log'))
        #handler = RotatingFileHandler(os.path.join(path, 'meggie.log'))
        handler.setLevel(logging.INFO)
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(asctime)s - %(message)s')
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
        self._logger.info('----------')
        self._logger.info(msg)
        
    def log_outcome(self, outcome):
        self._logger.info(outcome)
        
    def add_notification(self, notification):
        """
        Adds the notification to the notifications list.
        
        Keyword arguments
        notification    -- notification message
        """
        self._notifications.append(notification)
        
    def include_notifications_to_msg(self, msg):
        """
        Takes care of the notifications
        if there are any.
        
        Keyword arguments:
        msg    -- message to include the notifications to (=SUCCESS/WARNING/ERROR)
        """
        if len(self._notifications) > 0:
            msg += '. NOTE:\n'
            for notification in self._notifications:
                msg += notification + '\n'
            #Remove notifications to prevent logging them after the next computation
            del self._notifications[:]
        return msg
    