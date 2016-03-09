# coding: utf-8

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppakangas, Janne Pesonen and Atte Rautio>
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
@author: Janne Pesonen, Kari Aliranta

Classes needed for controlling Meggie experiments.

"""
import os
import re
import json


from meggie.code_meggie.general import fileManager
from meggie.code_meggie.general.subject import Subject
from meggie.code_meggie.general.actionLogger import ActionLogger
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.epoching.evoked import Evoked

from meggie.ui.utils.decorators import messaged

from PyQt4.QtCore import QObject


class Experiment(QObject):
    
    """A class that holds experiment info.

    Experiment stores path of the experiment file, author, description and
    list of the subjects. It also has methods for saving and parsing parameter
    files and pickling and unpickling itself to and from disk.

    Properties:
    experiment_name    -- The name of the experiment
    workspace          -- The path to the experiment folder
    author             -- The name of the experiment's author
    description        -- A user defined description of the experiment
    subjects           -- The list of the Subject objects in this experiment
    active_subject     -- The subject that is currently processed
    action_logger      -- logs action
    """

    def __init__(self):
        """
        Constructor sets default values for attributes.
        """
        QObject.__init__(self)
        self._experiment_name = 'experiment'
        self._author = 'unknown author'
        self._description = 'no description'
        self._subjects = []
        self._active_subject = None
        self._action_logger = None
        self._workspace = None

        

    @property
    def workspace(self):
        return self._workspace
    
    @workspace.setter
    def workspace(self, workspace):
        self._workspace = workspace

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
        name = os.path.basename(experiment_name)
        
        if (len(name) <= 30):
            if re.match("^[A-Za-z0-9_ ]*$", name):
                self._experiment_name = str(experiment_name)
            else:
                raise ValueError('Use only letters and numbers in experiment' +
                                 'name')
        else:
            raise ValueError('Too long experiment name')

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
            if re.match("^[A-Za-zäÄöÖåÅ0-9 ]*$", author):
                self._author = author
            else:
                raise ValueError("Use only letters and numbers in _author name")
        else:
            raise ValueError('Too long _author name')

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
                "^[A-Za-zäÄöÖåÅ0-9 \t\r\n\v\f\]\[!\"#$%&'()*+,./:;<=>?@\^_`{|}~-]+$",
                 description) or len(description) == 0):
                self._description = description
            else:
                raise ValueError("Use only letters and " + 
                                 "numbers in your _description")
        else:
            raise ValueError("Too long _description")

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

    @property
    def action_logger(self):
        return self._action_logger

    @action_logger.setter
    def action_logger(self, action_logger):
        self._action_logger = action_logger

    def add_subject(self, subject):
        """
        Adds subject to the current experiment.
        
        Keyword arguments:
        subject    -- the subject object created by subject class
        """
        self._subjects.append(subject)

    def get_subjects(self):
        """
        Returns a list of all subjects.
        """
        return self._subjects

    def remove_subject(self, sname, main_window):
        """
        Removes the subject folder and its contents under experiment tree.
        Removes the subject information from experiment properties and updates
        the experiment settings file.

        Keyword arguments:
        sname        -- name of the subject to remove
        main_window -- MainWindow object
        """
        # subject_path = os.path.join(self.workspace, self.experiment_name, sname)

        # if (subject_path in path for path in self.subject_paths):
        #     # Need to call _subject_paths to be able to remove.
        #     # Doesn't work if call subject_path without _.
        #     self._subject_paths.remove(subject_path)
        #     del self._working_file_names[sname]

        # # If subject is not created with the chosen subject list item,
        # # hence activated using activate -button after opening an existing
        # # experiment, only subject_paths list and working_file_names dictionary
        # # needs to be updated.
        # for subject in self._subjects:
        #     if subject.subject_name == sname:
        #         self._subjects.remove(subject)

        # # If active subject is removed, the active properties have to be
        # # reseted to default values.    
        # if subject_path == os.path.join(self._workspace, self._experiment_name,
        #                                 self.active_subject_name):
        #     self._active_subject_name = ''
        #     self._active_subject = None

        # try:
        #     shutil.rmtree(subject_path)
        # except OSError('Could not remove the contents of the subject folder.'):
        #     raise
        # self.save_experiment_settings()
        # main_window._initialize_ui()
        raise NotImplementedError

    def activate_subject(self, subject_name):
        """Activates a subject from the existing Subjects. Reads the working
        file under the directory of the given subject name and sets it
        to the corresponding Subject.

        Keyword arguments:
        subject_name -- name of the subject
        """
        # Remove raw files from memory before activating new subject.
        if self.active_subject:
            self.active_subject.release_memory()
        # if subject_name in [subject.subject_name for subject in self.get_subjects()]:
        #     working_file = subject.get_working_file()
        for subject in self._subjects:
            if subject_name == subject.subject_name:
                subject.set_working_file(
                    fileManager.open_raw(subject.working_file_path))
                self.active_subject = subject
        self.save_experiment_settings()
 
    def create_subject(self, subject_name, experiment, working_file_name, raw_path=None):
        """Creates a Subject when adding a new one to the experiment.
        
        Keyword arguments:
        subject_name    -- name of the subject
        experiment      -- Experiment object
        """
        subject = Subject(experiment, subject_name, working_file_name)
        if raw_path:
            fileManager.save_subject(subject, raw_path)
        self.add_subject(subject)
        
    def save_experiment_settings(self):
        """
        Saves (pickles) the experiment settings into a file in the root of
        the experiment directory structure.
        """        
        # save to file:
        # construct save dict
        subjects = []
        for subject in self.get_subjects():
            subject_dict = {
                'subject_name': subject.subject_name,
                'working_file_name': subject.working_file_name,
                'epochs': [], 
                'evokeds': []
            }
            for epoch in subject.epochs.items():
                epoch_dict = {
                    'collection_name': epoch.collection_name,
                    'params': epoch.params
                }
                subject_dict['epochs'].append(epoch_dict)
            for evoked in subject.evokeds.items():
                evoked_dict = {
                    'name': evoked.name
                }
                subject_dict['evokeds'].append(evoked_dict)
            subjects.append(subject_dict)
        
        save_dict = {
            'subjects': subjects,
            'name': self.experiment_name,
            'workspace': self.workspace,
            'author': self.author,
            'description': self.description,
        }
        
        if self.active_subject:
            save_dict['active_subject'] = self.active_subject.subject_name
        
        # save to file
        try:
            os.makedirs(self.workspace)
        except OSError:
            pass
        
        with open(os.path.join(self.workspace, self.experiment_name + '.exp'), 'w') as f:
            json.dump(save_dict, f)


class ExperimentHandler(QObject):
    """
    Class for handling the creation of a new experiment.
    
    TODO: should also handle switching active experiment.
    """
    
    def __init__(self, parent):
        """
        Constructor
        Keyword arguments:
        parent        -- Parent of this object.
        """
        self.parent = parent

    def initialize_new_experiment(self, expDict):
        """
        Initializes the experiment object with the given data. Assumes that
        Meggie is currently devoid of a current experiment.
        
        TODO: Keyword arguments:
           
        """
        prefs = self.parent.preferencesHandler
      
        try:
            experiment = Experiment()
            experiment.author = expDict['author']
            experiment.experiment_name = expDict['name']
            experiment.description = expDict['description']
        except AttributeError:
            raise Exception('Cannot assign attribute to experiment.')
        
        experiment.workspace = os.path.join(prefs.working_directory, expDict['name'])
        
        experiment.save_experiment_settings()
        
        self.initialize_logger(experiment)
        
        prefs.previous_experiment_name = experiment.experiment_name
        prefs.write_preferences_to_disk()
        
        return experiment
        
    def open_existing_experiment(self, name):
        """
        Opens an existing experiment, which is assumed to be in the working
        directory.
        
        Keyword arguments:
        
        name        -- name of the existing experiment to be opened
        """
        with open(name + '.exp', 'r') as f:
            data = json.load(f)
        prefs = self.parent.preferencesHandler
        experiment = Experiment()
        experiment.author = data['author']
        experiment.experiment_name = data['name']
        experiment.description = data['description']
        experiment.workspace = data['workspace']
 
        for subject_data in data['subject'].values():
            subject = Subject(experiment, subject_data['subject_name'], subject_data['working_file_name'])
            for epoch_data in subject_data['epochs']:
                epochs = Epochs()
                epochs.collection_name = epoch_data['collection_name']
                epochs.params = epoch_data['params']
                subject.add_epochs(epochs)
            for evoked_data in subject_data['evokeds']:
                evoked = Evoked()
                evoked.name = evoked_data['name']
                subject.add_evoked(evoked)
            experiment.add_subject(subject)
        if 'active_subject' in data.keys():
            self.parent.caller.experiment.activate_subject(data['active_subject'])

        experiment.save_experiment_settings()
        self.initialize_logger(experiment)
        prefs.previous_experiment_name = experiment.experiment_name
        prefs.write_preferences_to_disk()
        self.parent.caller.experiment = experiment
        self.parent.add_tabs()
        self.parent._initialize_ui()
       
        # working_directory = self.parent.preferencesHandler.working_directory
        # if not os.path.exists(working_directory):
        #     raise Exception('Could not find working directory. Check preferences.')
        # if name is not '':
        #     print "Opening experiment " + name
        #     try:
        #         path = os.path.join(
        #                     self.parent.preferencesHandler.working_directory, 
        #                     name)
        #     except IOError:
        #         raise Exception("Error opening the experiment.")
        # else:
        #     return
        # 
        # fname = os.path.join(path, os.path.basename(path + '.exp'))
        # if os.path.exists(path) and os.path.isfile(fname):
        #     caller = Caller.Instance()
        #     # Releases memory from the previously open experiment
        #     caller._experiment = None
        #     gc.collect()
        #     print "Opening file " + fname
        #     caller._experiment = fileManager.unpickle(fname)
        #     self.initialize_logger(caller._experiment)
        # 
        #     self.parent.update_ui()
        #     caller.experiment.create_subjects(caller._experiment,
        #                     caller._experiment._subject_paths,
        #                     self.parent.preferencesHandler.working_directory)
        #     if caller.experiment.workspace != working_directory:
        #         caller.experiment.workspace = working_directory
        #     self.parent.update_ui()
        #     caller.activate_subject(caller._experiment._active_subject_name,
        #                             do_meanwhile=self.parent.update_ui,
        #                             parent_handle=self.parent)
        #     self.parent.add_tabs()
        #     self.parent._initialize_ui()
        #     self.parent.reinitialize_models() 
        #     
        # 
        #     self.parent.preferencesHandler.previous_experiment_name = caller.experiment._experiment_name
        #     self.parent.preferencesHandler.write_preferences_to_disk()
        # else:
        #     raise Exception("Experiment configuration file (.exp) not found!")
    
    def initialize_logger(self, experiment):

        print 'Initializing logger' 
        try:
            experiment.action_logger = ActionLogger()
            experiment.action_logger.initialize_logger(experiment.workspace)
        except:
            experiment.action_logger.log_message('Could not initialize logger.')
            print 'Unable to initialize logger'
            return
        experiment.action_logger.log_message('Opened experiment: '+ experiment.experiment_name)
        print 'Logger initialized'
