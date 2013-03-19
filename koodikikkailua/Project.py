"""
Created on Mar 6, 2013

@author: Janne Pesonen
"""

import mne
import time
import os
import re

class Project():
    """
    Project holds information about the currently saved raw data,
    the path of the data file, the author, the date and description.
    """
    
    
    def __init__(self):
        """
        Constructor
        
        Keyword arguments:
        project_name - - the name of the project
        raw_data - - the raw data file of the measured data
        file_path - - the path of the saved project
        author - - the author of the project
        description - - the description of the project written by the author
        date - - the time and date of the saved project
        """
        
        self.project_name = 'project'
        self.raw_data = 'no data specified'
        self.file_path = 'no path defined'
        self.author = 'unknown author'
        self.description = 'no description'
        self.date = time.strftime('%Y %m %d %X')
        
        
    def get_project_name(self):
        """
        Returns the name of the project.
        """
        return self.project_name
    
    
    def set_project_name(self, project_name):
        """
        Sets the name for the project.
        """
        if (len(project_name) <= 30):
            if re.match("^[A-Za-z0-9 ]*$", project_name):
                self.project_name = project_name
            else:
                raise Exception("Use only letters and numbers in project name")
        else:
            raise Exception('Too long project name')
    
    
    def get_file_path(self):
        """
        Returns the path of the current project file.
        """
        return self.file_path
    
   
    def set_file_path(self, file_path):
        """
        Sets the given path for the project file.
        Raises exception if the given path doesn't exist.
        """
        if (os.path.isdir(file_path)): 
            self.file_path = file_path
        else:
            raise Exception('No such path')
            
        
    def get_raw_data(self):
        """
        Returns the raw data file of the project.
        """
        return self.raw_data
    
    
    def set_raw_data(self, raw_data):
        """
        Sets the raw data file for the project.
        Raises exception if the given data type is wrong. 
        """
        if (type(raw_data) == mne.fiff.Raw):
            self.raw_data = raw_data
        else:
            raise Exception('Wrong data type')
        
    
    def get_author(self):
        """
        Returns the author of the project
        """
        return self.author
    
    
    def set_author(self, author):
        """
        Sets the author of the project.
        Raises exception if the author name is too long.
        Raises exception if the author name includes other characters than letters and numbers.
        """
        if (len(author) <= 50):
            if re.match("^[A-Za-z0-9 ]*$", author):
                self.author = author
            else:
                raise Exception("Use only letters and numbers in author name")
        else:
            raise Exception('Too long author name')
    
    
    def get_date(self):
        """
        Returns the saving time and date of the project.
        """
        return self.date
    
    
    def get_description(self):
        """
        Returns the description of the project.
        """
        return self.description
    

    def set_description(self, description):
        """
        Sets the description of the project written by the author.
        Raises exception if the description is too long.
        Raises exception if the description includes other characters than letters and numbers.        
        """
        if (len(description) <= 1000):
            if re.match("^[A-Za-z0-9 \t\r\n\v\f\]\[!\"#$%&'()*+,./:;<=>?@\^_`{|}~-]+$", description):
                self.description = description
            else:
                raise Exception("Use only letters and numbers in your description")  
        else:
            raise Exception("Too long description")
        
    
    def save_project(self):
        """
        Saves the project folder and the contents including raw data file.
        """
        newpath = self.file_path + self.project_name
        if os.path.exists(self.file_path):
            os.mkdir(newpath)