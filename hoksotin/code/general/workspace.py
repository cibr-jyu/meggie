"""
Created on Apr 4, 2013

@author: jaolpeso
"""
import os
import ConfigParser

class Workspace(object):
    """
    Class for creating and managing the working directory.
    """


    def __init__(self):
        """
        Constructor sets default working directory.
        """
        config = ConfigParser.RawConfigParser()
        config.read('settings.cfg')
        workspace = config.get('Workspace', 'workspace')
        self._working_directory = workspace
        
    @property    
    def working_directory(self):
        return self._working_directory
    
    @working_directory.setter
    def working_directory(self, working_directory):
        """
        Keyword arguments:
        self._working_directory    - - Default workspace is used for the
                                      measurement if user doesn't define.
        """

        self._working_directory = working_directory