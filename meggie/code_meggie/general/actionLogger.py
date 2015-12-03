"""
Created on 26.11.2015

@author: Janne Pesonen
"""
import os
import logging
from boto.mturk import notification

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


    def __init__(self):
        """
        Constructor
        """
        #copied stuff from MNE-Python utils.py
        self._logger = logging.getLogger('meggie')  # one selection here used across Meggie
        self._logger.propagate = False  # don't propagate (in case of multiple imports)
        self._actionCounter = 1;
        self._notifications = []
        #self.initialize_logger()
        
    @property
    def logger(self):
        """
        Returns the logger.
        """
        return self._logger
    
        
    def initialize_logger(self):
        """Initializes the logger and adds a handler to it that handles writing and formatting
        the logs to a file.
        
        Keyword arguments
        path -    path to save the log file
        """
        #TODO: try JSON or YAML
        #TODO: If you use FileHandler for writing logs, the size of log file will grow with time.
        #Someday, it will occupy all of your disk. In order to avoid that situation, you should
        #use RotatingFileHandler instead of FileHandler in production environment.
        handler = logging.FileHandler('meggie_log.log')
        handler.setLevel(logging.INFO)
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)
        self._logger.setLevel(logging.INFO)
        
    def log_dict(self, params):
        """
        Logs parameters from dictionary
        """
        self._logger.info('*Begin dict*')
        #TODO: Check for external parameters, if exist add them to the dictionary.
        #      Basically the same idea as with notifications list -> gather parameters in code and
        #      let some ActionLogger variable handle them.  
        #      Example: params = self.append_variables_to_dict(params)
        #      Usage example: epoch collection creation events list is a huge mess for the user ->
        #      select the event ID and event name only
        #      Also, if the stim channel is included (true), get the name of the stimulus channel (STI001, ... , STI008, STI101) 
        if params != None:
            for key, value in params.items():
                self._logger.info(str(key) + ',' + str(value))
        self._actionCounter += 1
        self._logger.info('*End dict*')
        
    def log_list(self, params):
        """
        Logs parameters from list
        """
        self._logger.info('*Begin list*')
        for param in params:
            self._logger.info(str(param))
        self._actionCounter += 1
        self._logger.info('*End list*')
    
    def log_success(self, function_name, params):
        """
        Logs successful actions.
        
        Keyword arguments:
        function_name    - function to be logged
        params           - parameters of the function
        """
        msg = 'SUCCESS'
        msg = self.include_notifications_to_msg(msg)
        self.create_header(function_name, msg)
        if isinstance(params, dict):
            self.log_dict(params)
        else:
            self.log_list(params)
        
    def log_error(self, function_name, params, error):
        msg = 'FAILURE: ' + error
        msg = self.include_notifications_to_msg(msg)
        self.create_header(function_name, msg)
        if isinstance(params, dict):
            self.log_dict(params)
        else:
            self.log_list(params)
        
    def log_warning(self, function_name, params, warning):
        msg = 'WARNING: ' + warning
        msg = self.include_notifications_to_msg(msg)
        self.create_header(function_name, msg)
        if isinstance(params, dict):
            self.log_dict(params)
        else:
            self.log_list(params)
        
    def log_message(self, msg):
        """
        Logs given messages.
        TODO: let user write messages in Meggie to log them using this function
        
        Keyword arguments
        msg
        """
        self._logger.info('#')
        self._logger.info(msg)
        self._logger.info('#')
        #self._actionCounter += 1
        
    def log_subject_activation(self, subject_name):
        self._logger.info('----------------------------------------------------------------------------------------------------')
        #self._logger.info('Activated subject: ')
        self._logger.info(subject_name)
        
    def create_header(self, function_name, msg):
        """
        Creates header for the action
        
        Keyword arguments:
        function_name
        msg
        """
        self._logger.info('>>>')
        self._logger.info(function_name)
        self._logger.info(msg)
        self._logger.info('>>>')
        
    def add_notification(self, notification):
        """
        Sets the notification.
        """
        self._notifications.append(notification)
        
    def include_notifications_to_msg(self, msg):
        """
        Takes care of the notifications
        if there were some.
        
        Keyword arguments:
        msg    - message to include the notifications to (SUCCESS, WARNING, ERROR)
        """
        if len(self._notifications) > 0:
            msg += '. NOTE:\n'
            for notification in self._notifications:
                msg += notification + '\n'
            #Remove notifications to prevent logging them after the next successful calculation
            del self._notifications[:]
        return msg