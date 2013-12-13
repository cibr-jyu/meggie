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
import os

import re

from workspace import Workspace

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
        #TODO: setter and getter for workspace?
        self._workspace = ''
        self._author = 'unknown author'
        self._description = 'no description'
        
        self._subjects = [] #dict()
        self._subject_paths = []
        self._active_subject_path = ''
        self.mainWindow = None
        

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
    def active_subject_path(self):
        """
        Method for activating subject to enable its processing in Meggie.
        """
        return self._active_subject_path
    
    @active_subject_path.setter
    def active_subject_path(self, subject_path):
        """
        Method for setting an active subject to enable its processing in Meggie.
        """
        self._active_subject_path = subject_path

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
        self._subject_paths.append(subject_path)

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
        
        settingsFile = open(experiment_directory + '/' + settingsFileName, 'wb')
        
        # Actually a file object
        #settingsFile = open(self._workspace + '/' + settingsFileName, 'wb')
        
        # Protocol 2 used because of file object being pickled
        pickle.dump(self, settingsFile, 2)
        print '[done]'
        settingsFile.close()        

    def update_experiment_settings(self):
        """
        Updates experiment settings after adding a subject.
        """
        experiment_directory = self._workspace + '/' + self._experiment_name
        settingsFileName = str(self._experiment_name + '.pro')
        settingsFile = open(experiment_directory + '/' + settingsFileName, 'wb')
        pickle.dump(self, settingsFile, 2)
        settingsFile.close()


    def __getstate__(self):
        """
        Return state values to be pickled. Used to avoid pickling huge
        files two times to disk. Standard pickle method.
        """
        # TODO: muokkaa sitä mukaa kun tulee tarvetta, esim. subjectien,
        # epochien, evokedien jne. lisäämisten yhteydessä tarvitsee
        # päivittää settingsejä
        odict = self.__dict__.copy()
        #del odict['_subjects']
        #del odict['_active_subject']
        
        """
        del odict['_raw_data']
        del odict['_working_file']
        """
        #turha?
        for subject in self._subjects:
            del odict['subject._raw_data']
        
        
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
        workingPath = odict['_workspace']
        #self.subjects = odict['_subjects']
        self.subject_paths = odict['_subject_paths']
        self.active_subject_path = odict['_active_subject_path']
        self.__dict__.update(odict)    
        """
        rawFullPath = odict['_raw_data_path']
        workingFullPath = odict['_working_file_path']
        raw = mne.fiff.Raw(rawFullPath, preload=True)
        self.raw_data = raw
        self.working_file = workingFullPath
        """
        
        