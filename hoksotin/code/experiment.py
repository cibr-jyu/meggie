"""
Created on Mar 6, 2013

@_author: Janne Pesonen
"""

import mne

import os

import time
import re

import numpy as np
# Better to use pickle rather than cpickle, as project paths may
# include unicode characters
import pickle
import shutil

from node import Node
from tree import Tree

class Experiment(object):
    """
    Experiment holds information about the currently saved raw data,
    path of the experiment file, _author, date and _description.
    """
    
    def __init__(self):
        """
        Constructor sets default values for attributes.
        """
        
        self._experiment_name = 'experiment'
        self._raw_data = 'no data specified'
        self._file_path = 'no path defined'
        self._author = 'unknown _author'
        self._description = 'no _description'
        self.date = time.strftime('%Y %m %d %X')
        self.tree = Tree()
        self.__index = 0
        self._event_set = []
        
    @property
    def experiment_name(self):
        """
        Returns the name of the experiment.
        """
        return self._experiment_name

    @experiment_name.setter
    def experiment_name(self, experiment_name):
        """
        Sets the name for the experiment.
        
        Keyword arguments:
        experiment_name    - - the name of the experiment 
        """
        if (len(experiment_name) <= 30):
            if re.match("^[A-Za-z0-9 ]*$", experiment_name):
                self._experiment_name = experiment_name
            else:
                raise Exception("Use only letters and numbers in experiment name")
        else:
            raise Exception('Too long experiment name')
    
    @property
    def file_path(self):
        """
        Returns the path of the current experiment file.
        """
        return self._file_path
    
    @file_path.setter
    def file_path(self, file_path):
        """
        Sets the given path for the experiment file.
        Raises exception if the given path doesn't exist.
        
        Keyword arguments:
        file_path       - - the path of the saved experiment
        """
        if (os.path.isdir(file_path)): 
            self._file_path = file_path
        else:
            raise Exception('No such path')
    
    @property
    def raw_data(self):
        """
        Returns the raw data file of the experiment.
        """
        return self._raw_data
    
    @raw_data.setter
    def raw_data(self, raw_data):
        """
        Sets the raw data file for the experiment.
        Raises exception if the given data type is wrong. 
        
        Keyword arguments:
        raw_data        - - the raw data file of the measured data
        """
        if (isinstance(raw_data, mne.fiff.Raw)):
            self._raw_data = raw_data
        else:
            raise Exception('Wrong data type')
    
    @property
    def author(self):
        """
        Returns the _author of the experiment
        """
        return self._author
    
    @author.setter
    def author(self, author):
        """
        Sets the _author of the experiment.
        Raises exception if the _author name is too long.
        Raises exception if the _author name includes other characters
        than letters and numbers.
        
        Keyword arguments:
        author          - - the _author of the experiment
        """
        if (len(author) <= 50):
            if re.match("^[A-Za-z0-9 ]*$", author):
                self._author = author
            else:
                raise Exception("Use only letters and numbers in _author name")
        else:
            raise Exception('Too long _author name')
    
    def get_date(self):
        """
        Returns the saving time and date of the experiment.
        """
        return self.date
    
    @property
    def description(self):
        """
        Returns the _description of the experiment.
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the _description of the experiment written by the _author.
        Raises exception if the _description is too long.
        Raises exception if the _description includes other characters
        than letters and numbers.        
        
        Keyword arguments:
        description     - - the _description of the experiment written by the _author
        """
        if (len(description) <= 1000):
            if (re.match(
                "^[A-Za-z0-9 \t\r\n\v\f\]\[!\"#$%&'()*+,./:;<=>?@\^_`{|}~-]+$",
                 description) or len(description) == 0):
                self._description = description
            else:
                raise Exception("Use only letters and " + 
                                "numbers in your _description")
        else:
            raise Exception("Too long _description")
    
    @property
    def event_set(self):
        """
        Returns the events as a tuple, where the first element is the id
        and the second element is the number of the events.
        """
        return self._event_set
    
    def create_event_set(self):
        """
        Creates an event set where the first element is the id
        and the second element is the number of the events.
        Raises type error if the raw_data attribute is not set or
        if the data is not of type mne.fiff.Raw.
        """
        if not isinstance(self._raw_data, mne.fiff.Raw):
            raise TypeError('Not a raw object')
        events = mne.find_events(self._raw_data)
        event_occ = [] #occurrences of all the events
        for i in range(len(events)):
            event_occ.append(events[i][2])
        bins = np.bincount(event_occ) #number of events stored in an array
        event_numbers = np.nonzero(bins)[0]
        d = []
        for i in event_numbers:
            d.append((i, bins[i]))
        print d
    
    def save_experiment_settings(self):
        """
        Saves experiment settings into a file in the root of the experiment
        directory structure.
        """
        
        # String conversion, because shutil doesn't accept QStrings
        settingsFileName = str(self._experiment_name + '.pro')
        
        # Actually a file object
        settingsFile = open(self._file_path + '/' + settingsFileName, 'wb')
        
        # Protocol 2 used because of file object being pickled
        pickle.dump(self, settingsFile, 2)
       
        # Move the file from working directory to 
        #shutil.move(settingsFileName, str(self._file_path))
        
        settingsFile.close()
        
        
    def load_experiment_settings(self, fname):
        """
        Loads project settings from a file in the root of the experiment
        directory structure.
        
        Keyword arguments:
        experiment    - - experiment object to save
        """
        
    
    def save_experiment(self, workspace):
        """
        Creates the experiment folder.
        
        Keyword arguments:
        workspace    - - workspace for the chosen experiment.
        """
        self._file_path = workspace + self._experiment_name + '/'
        if os.path.exists(workspace):
            try:
                os.mkdir(self._file_path)
            except OSError:
                print "no rights to save to the chosen path"
        else:
            raise Exception('No such path')
        
    def save_raw(self, file_name):
        """
        Saves the raw data file into the experiment folder.
        
        Keyword arguments:
        file_name      - - the full path and name of the chosen raw data file
        """
        folder_name = file_name.split("_", 1)
        try:
            if os.path.exists(self._file_path + folder_name[0]):
                pass
            else:
                os.mkdir(self._file_path + folder_name[0])
        except OSError:
            print "no rights to save the raw file to the chosen path or bad raw file name"
        raw_file_path = str(self._file_path) + folder_name[0] + '/' + file_name
        mne.fiff.Raw.save(self._raw_data, raw_file_path)
        self._raw_data = mne.fiff.Raw(raw_file_path)
            
    def write_commands(self, commands, node, parent=''):
        """
        Writes an array of commands in a tree structure.
        Used for creating a batch file.
        
        Keyword arguments:
        commands      -- An array of commands
        node          -- Node id
        parent        -- Parent of the node
        """
        if parent == '':
            self.tree.create_node(commands, 'prep'+str(self.__index))
        else:
            self.tree.create_node(commands, node + str(self.__index), parent)
        self.__index += 1
        return self.__index - 1
            
    def get_subtree(self, nid, s=''):
        """
        Returns a set of commands from a subtree.
        
        Keyword arguments:
        nid           -- ID of the leaf
        s             -- Helper for recursion
        """
        while nid is not None:
            n = self.tree.get_node(nid)
            s = self.get_subtree(n.bpointer, s)
            s += ''.join(n.name)
            return s
        return ''
    