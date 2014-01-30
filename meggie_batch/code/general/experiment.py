# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Oct 22, 2013

@author: jaolpeso
"""
import os, glob
import re
import csv

from workspace import Workspace
from fileManager import FileManager
from subject import Subject

from PyQt4.QtCore import QObject, pyqtSignal

# Better to use pickle rather than cpickle, as experiment paths may
# include non-ascii characters
import pickle

class Experiment(QObject):
    
    """A class that holds experiment info.
    
    Experiment stores path of the experiment file, author, description and
    list of the subjects. It also has methods for saving and parsing parameter
    files and pickling and unpickling itself to and from disk.
    
    Properties:
    experiment_name   -- The name of the experiment
    workspace         -- The path to the experiment folder
    author            -- The name of the experiment's author
    description       -- A user defined description of the experiment
    subjects          -- The list of the Subject objects in this experiment
    subject_paths     -- The list of the paths of the added subjects
    active_subject    -- The subject that is currently processed
    
    """
    
    def __init__(self):
        """
        Constructor sets default values for attributes.
        """
        QObject.__init__(self)
        self._experiment_name = 'experiment'
        self._workspace = ''
        self._author = 'unknown author'
        self._description = 'no description'
        self._subjects = []
        self._subject_paths = []
        self._active_subject_path = ''
        self._active_subject_raw_path = ''
        self._active_subject_name = ''
        self._working_file_names = dict()
        self._active_subject = None
        self.main_window = None
        

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
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText \
                ('Use only letters and numbers in experiment name')
                self.messageBox.show()
                raise Exception('Use only letters and numbers in experiment' +
                                'name')
                
        else:
            raise Exception('Too long experiment name')

    @property
    def workspace(self):
        """
        Returns the path of the current experiment.
        """
        return self._workspace
    
    @workspace.setter
    def workspace(self, workspace):
        """
        Sets the given workspace for the experiment.
        Raises an exception if the given workspace path doesn't exist.
        Keyword arguments:
        workspace       -- the path of the saved experiment
        """
        if (os.path.isdir(workspace)): 
            self._workspace = workspace
        else:
            raise Exception('No such path')


    @property
    def author(self):
        """
        Returns the author of the experiment
        """
        return self._author
    
    @author.setter
    def author(self, author):
        """
        Sets the author of the experiment.
        Raises exception if the author name is too long.
        Raises exception if the author name includes other characters
        than letters and numbers.
        Keyword arguments:
        author          - - the author of the experiment
        """
        if (len(author) <= 30):
            if re.match("^[A-Za-zÄäÖöÅå0-9 ]*$", author):
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
        description     -- the description of the experiment written by the
                           author
        """
        if (len(description) <= 1000):
            if (re.match(
                "^[A-Za-zÄäÖöÅå0-9 \t\r\n\v\f\]\[!\"#$%&'()*+,./:;<=>?@\^_`{|}~-]+$",
                 description) or len(description) == 0):
                self._description = description
            else:
                raise Exception("Use only letters and " + 
                                "numbers in your _description")
        else:
            raise Exception("Too long _description")

    @property
    def active_subject_name(self):
        """
        Method for getting active subject name.
        """
        return self._active_subject_name
    
    @active_subject_name.setter
    def active_subject_name(self, subject_name):
        """
        Method for setting active subject name.
        """
        self._active_subject_name = subject_name

    @property
    def active_subject_path(self):
        """
        Method for getting active subject path.
        """
        return self._active_subject_path
    
    @active_subject_path.setter
    def active_subject_path(self, subject_path):
        """
        Method for setting active subject path.
        """
        self._active_subject_path = subject_path


    @property
    def active_subject_raw_path(self):
        """
        Method for getting active subject raw path.
        """
        return self._active_subject_raw_path
    
    @active_subject_raw_path.setter
    def active_subject_raw_path(self, raw_path):
        """
        Method for setting active subject raw path.
        """
        self._active_subject_raw_path = raw_path

    @property
    def active_subject(self):
        """
        Method for getting activated subject.
        """
        return self._active_subject
    
    @active_subject.setter
    def active_subject(self, subject):
        """
        Method for setting active subject.
        """
        self._active_subject = subject
    
    def add_subject(self, subject):
        """
        Adds subject to the current experiment.
        
        Keyword arguments:
        subject    -- the subject object created by subject class
        """
        #dictionary example:
        #self._subjects[subject.subject_name] = subject 
        self._subjects.append(subject)

    def add_subject_path(self, subject_path):
        """
        Adds subject path to the current experiment.
        
        Keyword arguments:
        subject_path    -- the subject path of the subject object
                           created by subject class
        """
        # Prevents adding same subject path several times.
        if not subject_path in self._subject_paths:
            self._subject_paths.append(subject_path)

    def update_working_file(self, working_file_name):
        """
        Adds working file name to the working_file list.
        Updates to the previously processed file.
        
        Keyword arguments:
        working_file_name    -- name of the working file
        """
        # Uusi koodi:
        self._working_file_names[self.active_subject_name] = working_file_name
        
    def activate_subject(self, main_window, raw_path, subject_name, experiment):
        """
        Method for activating a subject. Creates a new subject object
        to be processed if it doesn't exist in the subjects list property.
        Subject.working_file is the previously created raw file.
        
        Keyword arguments:
        raw_path     -- path of the raw file
        subject_name -- name of the subject
        experiment   -- currently active experiment                        
        """
        # TODO: Lataa epochit/evokedit aktivoitaessa subjectia.
        
        raw_file_name = raw_path.split('/')[-1]
        # Checks if the subject to be activated already exists in subjects
        # list.
        # Prevents creating multiple subjects when activating the same subject
        # more than once.
        for subject in self._subjects:
            if subject_name == subject.subject_name:
                # Raw file is still in memory while processing other
                # subjects and the file does not need to be opened here.
                # NOTE! These 4 properties must be set to be able to handle the
                # activated subject.
                self._active_subject = subject
                self._active_subject_name = subject.subject_name
                self._active_subject_path = subject.subject_path
                full_raw_path = subject.subject_path + raw_file_name
                self._active_subject_raw_path = full_raw_path
                main_window.load_epoch_collections()
                main_window.load_evoked_collections()
                return
        subject = Subject(experiment, subject_name)
        f = FileManager()
        # TODO: When opening experiment the right path is saved into the
        # working_file, but when activating subject the working_file path is the
        # one where the original raw was found.
        raw = f.open_raw(raw_path)
        #subject.raw_data = raw
        subject.working_file = raw
        #raw_file_name = raw_path.split('/')[-1]
        full_raw_path = subject.subject_path + raw_file_name
        # Check if file already exists.
        if not os.path.isfile(full_raw_path):
            # save_raw method calls create_epochs_directory in experiment
            subject.save_raw(raw_path, subject.subject_path)
            # When activating subject the working_file filename is the one where
            # the file was originally found. This is used to change it to
            # the location of the subject path.
            subject.working_file.info['filename'] = full_raw_path
        # TODO: working_file_path saattaa olla hyötyä setata subjectille.
        # Setteri ja getteri puuttuu subject-luokasta.
        # subject.working_file_path
        subject.find_stim_channel()
        subject.create_event_set()
        self._active_subject_name = subject_name
        self._active_subject_path = subject.subject_path
        self.update_working_file(raw_path)
        self.add_subject_path(subject.subject_path)
        self._active_subject_raw_path = full_raw_path
        self._active_subject = subject
        self.add_subject(subject)
        main_window.load_epoch_collections()
        main_window.load_evoked_collections()
        
    def save_experiment_settings(self):
        """
        Saves (pickles) the experiment settings into a file in the root of
        the experiment directory structure. Please note that loading is done
        in the mainWindow class. 
        """
        experiment_directory = self._workspace + '/' + self._experiment_name
        try:
            os.mkdir(experiment_directory)
            print 'Creating experiment settings ...'
        except OSError:
            raise Exception('No rights to save to the chosen path or' + 
                            ' experiment name already exists')
            return
        # String conversion, because shutil doesn't accept QStrings
        # TODO the file should end with .exp
        settingsFileName = str(self._experiment_name + '.pro')
        
        # Actually a file object
        settingsFile = open(experiment_directory + '/' + settingsFileName, 'wb')
        
        # Protocol 2 used because of file object being pickled
        pickle.dump(self, settingsFile, 2)
        print '[done]'
        settingsFile.close()        

    def update_experiment_settings(self):
        """
        Updates experiment settings after adding a subject.
        """
        # TODO: turha metodi, tee tarkistus save_experiment_settings metodissa,
        # sille onko kyseistä kansiota jo olemassa
        experiment_directory = self._workspace + '/' + self._experiment_name
        settingsFileName = str(self._experiment_name + '.pro')
        settingsFile = open(experiment_directory + '/' + settingsFileName, 'wb')
        pickle.dump(self, settingsFile, 2)
        settingsFile.close()

    def save_parameter_file(self, command, inputfilename, outputfilename,
                            operation, dic):
        """
        Saves the command and parameters related to creation of a certain
        output file to a separate parameter file in csv-format.
        
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
        command          -- command (as string) used.
        inputfilename    -- name of the file the command with parameters
                            was executed on
        outputfilename   -- the resulting output file from the command.
        operation        -- operation the command represents. Used for
                            determining the parameter file name.
        dic              -- dictionary including commands.
        """
        paramfilename = self.active_subject_path + operation + '.param'
        
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
        operation    -- String that designates the operation. See Caller class
                        for operation names.
                        
        """
        
        # Reading parameter file.
        paramdirectory = self.active_subject_path 
        paramfilefullpath = paramdirectory + operation + '.param'
        
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
            # In no dictionary is returned, the dialog just falls back to
            # default initial values.
            return None  


    def __getstate__(self):
        """
        Return state values to be pickled. Used to avoid pickling huge
        files two times to disk. Standard pickle method.
        """
        # TODO: muokkaa sitä mukaa kun tulee tarvetta, esim. subjectien,
        # epochien, evokedien jne. lisäämisten yhteydessä tarvitsee
        # päivittää settingsejä
        odict = self.__dict__.copy()
        del odict['_subjects']
        del odict['_active_subject']
        #del odict['_active_subject']
        
        
        return odict

    def __setstate__(self, odict):
        """
        Restore state from the unpickled state values. Restores raw and working
        files from the files in the experiment directory. Standard pickle
        method.
        """ 
        # TODO: muokkaa sitä mukaa kun tulee tarvetta, esim. subjectien,
        # epochien, evokedien jne. lisäämisten yhteydessä tarvitsee
        # päivittää settingsejä
        QObject.__init__(self)
        
        # Pickle doesn't save subjects and active_subject so the properties
        # need to be set here.
        self._subjects = []
        self._active_subject = None
        
        self._workspace = odict['_workspace']
        self._subject_paths = odict['_subject_paths']
        self._active_subject_path = odict['_active_subject_path']
        self._active_subject_raw_path = odict['_active_subject_raw_path']
        self._active_subject_name = odict['_active_subject_name']
        
        
        self.__dict__.update(odict)    
        """
        rawFullPath = odict['_raw_data_path']
        workingFullPath = odict['_working_file_path']
        raw = mne.fiff.Raw(rawFullPath, preload=True)
        self.raw_data = raw
        self.working_file = workingFullPath
        """
        
        