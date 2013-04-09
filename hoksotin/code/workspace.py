"""
Created on Apr 4, 2013

@author: jaolpeso
"""
import os

class Workspace(object):
    """
    classdocs
    """


    def __init__(self):
        """
        Constructor sets default working directory.
        """
        self._working_directory = os.getcwd()
        
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