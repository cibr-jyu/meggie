"""
Created on Mar 6, 2013

@_author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
"""

import mne

import os

import re
import csv
import glob

import numpy as np

# Better to use pickle rather than cpickle, as experiment paths may
# include unicode characters
import pickle

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
        self._raw_data_path = 'no path defined'
        self._subject_directory = 'no directory specified'
        self._file_path = 'no path defined'
        self._author = 'unknown _author'
        self._description = 'no _description'
        self._working_file = ''
        self._working_file_path = 'no path defined'
        self._event_set = []
        self._stim_channel = ''
        self.mainWindow = None
        
        # Add here all the possible actions that you can do to an experiment
        # TODO not in use, possibly not needed
        self.stateDict = dict(Maxfilter=False, ECGcomputed=False,
                              ECGapplied=False, EOGcomputed=False,
                              EOGapplied=False, Eventlist=False,
                              Epochs=False, Average=False)        
    
    
    # raw_data_path and working_file_path are only used internally 
    
    @property
    def raw_data_path(self):
        return self._raw_data_path
    
    @raw_data_path.setter
    def raw_data_path(self, fname):
        self._raw_data_path = fname
                
    @property
    def working_file_path(self):
        return self._working_file_path
    
    @working_file_path.setter
    def working_file_path(self, fname):
        self._working_file_path = fname
       
                
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
        experiment_name    -- the name of the experiment 
        """
        if (len(experiment_name) <= 30):
            if re.match("^[A-Za-z0-9 ]*$", experiment_name):
                self._experiment_name = experiment_name
            else:
                raise Exception("Use only letters and numbers in experiment \
                name")
        else:
            raise Exception('Too long experiment name')
    
    @property
    def subject_directory(self):
        """
        Returns the absolute path to the subject directory of the experiment.        
        """
        return self._subject_directory
    
    @subject_directory.setter
    def subject_directory(self, subject_directory):
        """
        Sets the subject directory for the experiment. Should be an absolute
        path. Not setable by user, for internal use only.
        TODO: should probably later be a list of subject directories, if the
        experiment is to include several of them
        """
        
        self._subject_directory = subject_directory
    
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
        file_path       -- the path of the saved experiment
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
        raw_data        -- the raw data file of the measured data
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
        description     - - the _description of the experiment written
        by the _author
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
    
    @property
    def working_file(self):
        """
        Returns the current working file.
        """
        return self._working_file
    
    @working_file.setter
    def working_file(self, fname):
        """
        Sets the current working file and notifies the main window to show it.
        Keyword arguments:
        fname         -- Name of the new working file.
        """
        self._working_file = mne.fiff.Raw(fname, preload=True)
        self.working_file_path = fname
        #self.shortname = os.path.basename(fname)
        #self.mainWindow.ui.statusbar.showMessage("Current working file: " + 
        #                                         shortname)
        
        
    @property
    def stim_channel(self):
        """
        Property for stimulus channel.
        """
        return self._stim_channel
    
    @stim_channel.setter
    def stim_channel(self, stim_ch):
        """
        Setter for stimulus channel.
        """
        """
        channels = self._raw_data.info.get('ch_names')
        if any('STI101' in channels for x in channels):
            self._stim_channel = 'STI101'
        elif any('STI 014' in channels for x in channels):
            self._stim_channel = 'STI 014'
        else:
            raise Exception('No stim channel found.')
        """
        self._stim_channel = stim_ch
    
    def find_stim_channel(self):
        """
        Finds the correct stimulus channel for the data.
        """
        channels = self._raw_data.info.get('ch_names')
        if any('STI101' in channels for x in channels):
            self._stim_channel = 'STI101'
        elif any('STI 014' in channels for x in channels):
            self._stim_channel = 'STI 014'
        else:
            raise Exception('No stim channel found.')
    
    def create_event_set(self):
        """
        Creates an event set where the first element is the id
        and the second element is the number of the events.
        Raises type error if the raw_data attribute is not set or
        if the data is not of type mne.fiff.Raw.
        """
        if not isinstance(self._raw_data, mne.fiff.Raw):
            raise TypeError('Nt a raw object')
        events = mne.find_events(self._raw_data,
                                 stim_channel=self._stim_channel)
        bins = np.bincount(events[:,2]) #number of events stored in an array
        d = dict()
        for i in set(events[:,2]):
            d[i] = bins[i]
        self._event_set = d
    
    def save_experiment_settings(self):
        """
        Saves (pickes) the experiment settings into a file in the root of
        the experiment directory structure. Please note that loading is done
        in the mainWindow class. 
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

    def save_raw(self, file_name, path):
        """
        Saves the raw data file into the experiment folder.
        
        Keyword arguments:
        file_name      -- the full path and name of the chosen raw data file
        """
        self._file_path = path + '/' + self._experiment_name + '/'
        folder_name = file_name.split("_", 1)
        if os.path.exists(path):
            try:
                os.mkdir(self._file_path)
                os.mkdir(self._file_path + '/' + folder_name[0])
            except OSError:
                raise OSError("no rights to save to the chosen path")
        else:
            raise Exception('No such path')
        
        if os.path.exists(self._file_path + folder_name[0]):
            self.subject_directory = str(self._file_path) + folder_name[0] + '/'
            raw_file_path = str(self._file_path) + folder_name[0] + '/' + file_name
            mne.fiff.Raw.save(self._raw_data, raw_file_path)
            self._raw_data = mne.fiff.Raw(raw_file_path, preload=True)
            self._raw_data_path = self._raw_data.info.get('filename')
        else:
            raise Exception('No rights to save the raw file to the chosen ' + 
                            'path or bad raw file name.')
            
    def save_parameter_file(self, command, inputfilename, outputfilename,
                            operation, dic):
        """
        Saves the command and parameters related to creation of a certain
        output file to a separate parameter file in csv-format.
        TODO: breaks if dictionary keys or values include commas --> check
        
        An example of the structure of the resulting parameter file:
        
        jn_multimodal01_raw_sss.fif
        jn_multimodal01_raw_sss_ecg_proj.fif 
        mne.preprocessing.compute_proj_eog
        tmin,0.2
        tmax,0.5
        .
        .
        .  
        
        Keyword arguments:
        inputfilename    -- name of the file the command with parameters
                            was executed on
        outputfilename   -- the resulting output file from the command.
        command          -- command (as string) used.
        operation        -- operation the command represents. Used for
                            determining the parameter file name.
        dic              -- dictionary including commands.
        """
        paramfilename = self.subject_directory + operation + '.param'
        
        with open(paramfilename, 'wb') as paramfullname:
            print 'writing param file'
            csvwriter = csv.writer(paramfullname)
            
            csvwriter.writerow([inputfilename])
            csvwriter.writerow([outputfilename])
            csvwriter.writerow([command])
            
            for key, value in dic.items():
                csvwriter.writerow([key, value])
                    
    def parse_parameter_file(self, operation):
        """
        Reads the parameters from a single file matching the operation
        and returns the parameters as a dictionary.        
        
        Keyword arguments:
        operation    -- string that designates the operation. See caller and
                        e for
                        operations and 
        """
        
        # Reading parameter file.
        paramdirectory = self._subject_directory 
        paramfilefullpath = paramdirectory + operation + '.param'
        
        #globquery = paramdirectory + globquerystring
        #globlist = glob.glob(globquery)
        
        try:
            with open(paramfilefullpath, 'rb') as paramfile:
                csvreader=csv.reader(paramfile)
                
                # skip the first three lines, as they don't include actual
                # info about parameters
                for i in range(3):
                    next(csvreader)
                
                # Read the rest of the parameter file into a dictionary as
                # key-value pairs
                paramdict = dict(x for x in csvreader)
                return paramdict           
        except IOError:
            return None
                        
    def __getstate__(self):
        """
        Return state values to be pickled. Used to avoid pickling huge files
        files two times to disk. 
        """
        odict = self.__dict__.copy()
        del odict['_raw_data']
        del odict['_working_file']
        return odict

    def __setstate__(self, odict):
        """
        Restore state from the unpickled state values. Restores raw and working
        files from the files in the experiment directory.
        """ 

        rawFullPath = odict['_raw_data_path']
        workingFullPath = odict['_working_file_path']
        
        self.__dict__.update(odict)        
        
        raw = mne.fiff.Raw(rawFullPath, preload=True)
        
        self.raw_data = raw
        self.working_file = workingFullPath
        
        