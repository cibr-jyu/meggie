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
        Constructor
        
        Keyword arguments:
        self.working_directory    - - Default workspace is used for the
                                      measurement if user doesn't define.
        """
        self.working_directory = os.getcwd()
        
        
    def get_workspace(self):
        return self.working_directory
    
    def set_workspace(self, working_directory):
        self.working_directory = working_directory