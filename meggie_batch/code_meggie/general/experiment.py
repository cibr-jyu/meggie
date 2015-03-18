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
@author: Janne Pesonen, Kari Aliranta

Classes needed for controlling Meggie experiments.

"""
import os
import re
import shutil
import gc
from threading import Event

import fileManager
from subject import Subject
from ui.general import messageBoxes
from code_meggie.general.caller import Caller

from PyQt4.QtCore import QObject
from PyQt4 import QtGui



# Better to use pickle rather than cpickle, as experiment paths may
# include non-ascii characters
import pickle

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
    subject_paths      -- The list of the paths of the added subjects
    active_subject     -- The subject that is currently processed
    working_file_names -- The complete path of the working file
    """
    
    e = Event()
    
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
        self._active_subject = None
        
        # For pickling purposes to make loading experiments and subjects
        # more simple.
        self._active_subject_name = ''
        self._subject_paths = []
        self._working_file_names = dict()
        
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
                self._experiment_name = str(experiment_name)
            else:
                message = 'Use only letters and numbers in experiment name'
                self.messageBox = messageBoxes.shortMessageBox(message)
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
            raise Exception('No such workspace path')


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
    

    def is_ready(self):
        """
        Method for polling threaded processes.
        """
        return self.e.is_set()

    
    def add_subject(self, subject):
        """
        Adds subject to the current experiment.
        
        Keyword arguments:
        subject    -- the subject object created by subject class
        """
        # dictionary
        #self._subjects[subject.subject_name] = subject
        
        # list 
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
        subject_path = os.path.join(self.workspace, self.experiment_name, sname)
        
        if (subject_path in path for path in self.subject_paths):
            # Need to call _subject_paths to be able to remove.
            # Doesn't work if call subject_path without _.
            self._subject_paths.remove(subject_path)
            del self._working_file_names[sname]
        
        # If subject is not created with the chosen subject list item,
        # hence activated using activate -button after opening an existing
        # experiment, only subject_paths list and working_file_names dictionary
        # needs to be updated.
        for subject in self._subjects:
            if subject.subject_name == sname:
                self._subjects.remove(subject)
        
        # If active subject is removed, the active properties have to be
        # reseted to default values.    
        if subject_path == os.path.join(self._workspace, self._experiment_name,
                                        self.active_subject_name):
            self._active_subject_name = ''
            self._active_subject = None
        
        try:
            shutil.rmtree(subject_path)
        except OSError('Could not remove the contents of the subject folder.'):
            raise
        self.save_experiment_settings()
        main_window._initialize_ui()


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
        self._working_file_names[self.active_subject_name] = working_file_name
      
        
    def activate_subject(self, subject_name):
        """Activates a subject from the existing Subjects. Reads the working
        file under the directory of the given subject name and sets it
        to the corresponding Subject.
        
        Keyword arguments:
        subject_name -- name of the subject
        """
        # Remove raw files from memory before activating new subject.
        self.e.clear()
        self.release_memory()
        self._active_subject_name = subject_name
        working_file_name = self._working_file_names[subject_name]
        if len(working_file_name) == 0:
            print 'There is no working file in the chosen subject folder.'
            self.e.set()
            return 1
        
        # Checks if the subject with subject_name already exists in subjects list.
        for subject in self._subjects:
            if subject_name == subject.subject_name:
                #self.set_active_subject(subject, raw_file_name)
                self._active_subject = subject
                self._active_subject_name = subject.subject_name
                # Check if the working file is actually loaded already (in the
                # case of addSubjectDialogMain accept() method).
                self.load_working_file(subject)
                self.save_experiment_settings()
        self.e.set()
        return 0
 
    def create_subject(self, subject_name, experiment, raw_path):
        """Creates a Subject when adding a new one to the experiment.
        
        Keyword arguments:
        subject_name    -- name of the subject
        experiment      -- Experiment object
        raw_path        -- original path of the raw file
        """
        subject = Subject(experiment, subject_name)
        raw = fileManager.open_raw(raw_path)
        subject._working_file = raw
        complete_raw_path = os.path.join(subject.subject_path, os.path.basename(raw_path))
        # Check if file already exists.
        if not os.path.isfile(complete_raw_path):
            try:
                # Makes the actual subject path on disk and copies raw file there.
                subject.save_raw(raw_path, subject.subject_path)
                
                # Best to create these right away to avoid insane amount of
                # checking later on.
                subject.create_epochs_directory()
                subject.create_evokeds_directory()
                subject.create_sourceAnalysis_directory()
                subject.create_reconFiles_directory()
                subject.create_forwardModels_directory()
                # When activating subject the working_file filename is the one
                # where the file was originally found. This changes it to
                # the location of the subject path.
                subject._working_file.info['filename'] = complete_raw_path
            except Exception: 
                # FIXME: remove whole subject directory as cleanup.
                raise
    
        self._subjects.append(subject)
        self._active_subject_name = subject_name
        self.add_subject_path(subject.subject_path)
        self.update_working_file(complete_raw_path)
        
        
    def create_subjects(self, experiment, subject_paths):
        """Creates subjects when opening an experiment with subjects.
        Raw file is not set here.
        
        Keyword arguments:
        experiment    -- experiment object from MainWindow
        subject_names -- list of subject names
        """
        for subject_path in subject_paths:
            subject = Subject(experiment, os.path.basename(subject_path))
            self._subjects.append(subject)
            
    
    def release_memory(self):
        """Releases memory from previously processed subject by removing
        references from raw files.
        """
        if self.active_subject is not None:
            self.active_subject._working_file = None
            if len(self.active_subject._epochs) > 0:
                for value in self.active_subject._epochs.values():
                    value._raw = None
            if len(self.active_subject._evokeds) > 0:
                for value in self.active_subject._evokeds.values():
                    value._raw = None
        
        
    def load_working_file(self, subject):
        """Loads raw file from subject folder and sets it on
        subject._working_file property.
        
        Keyword arguments:
        subject    -- Subject object
        """
        #files = os.listdir(self.active_subject_path)
        if subject._working_file is None:
            path = os.path.join(self._workspace, self._experiment_name, subject._subject_name)
            files = os.listdir(path)
            for f in files:
                file_path = os.path.join(path, f)
                if file_path in self._working_file_names.values():
                    raw = fileManager.open_raw(os.path.join(path, file_path))
                    # TODO: set channel names with whitespaces for the subject.working_file
                    # Not necessarily needed when loading from subject folder because
                    # whitespaces are already added when new subject is added.
                    subject._working_file = raw
        subject.find_stim_channel()
        subject.create_event_set()
        

    def load_epochs(self, subject):
        """Loads raw epoch files from subject folder and sets them on
        subject._epochs objects.
        """
        if os.path.exists(self.active_subject._epochs_directory) is False:
            self.active_subject.create_epochs_directory
        epoch_items = []
        files = os.listdir(subject._epochs_directory)
        for f in files:
            if f.endswith('.fif'):
                fname = os.path.join(subject._epochs_directory,
                                     f)
                
                name = f[:-4]
                epochs, params = fileManager.load_epochs(fname)
                subject.handle_new_epochs(name, epochs, params)
                item = QtGui.QListWidgetItem(name)
                # Change color of the item to red if no param file available.
                if params is None:
                    color = QtGui.QColor(255, 0, 0, 255)
                    brush = QtGui.QBrush()
                    brush.setColor(color)
                    item.setForeground(brush)
                epoch_items.append(item)
                # Raw needs to be set when activating already created subject.
                if subject._epochs[name]._raw is None:
                    subject._epochs[name]._raw = epochs
        return epoch_items


    def load_evokeds(self, subject):
        """Loads raw evoked files from subject folder and sets them on
        subject._evokeds objects.
        """
        evokeds_items = []
        files = os.listdir(subject._evokeds_directory)
        for file in files:
            if file.endswith('.fif'):
                evoked, categories = fileManager.load_evoked(subject._evokeds_directory,
                                                   file)
                subject.handle_new_evoked(file, evoked, categories)
                item = QtGui.QListWidgetItem(file)
                evokeds_items.append(item)
                # Raw needs to be set when activating already created subject.
                if subject._evokeds[file]._raw is None:
                    subject._evokeds[file]._raw = evoked

        return evokeds_items
            
                
    def get_subject_working_file(self, subject_name):
        """Returns working file of a given subject name.
        
        Keyword arguments:
        subject_name    -- name of the subject
        """
        return fileManager.open_raw(self._working_file_names[subject_name])
           
                
    def save_experiment_settings(self):
        """
        Saves (pickles) the experiment settings into a file in the root of
        the experiment directory structure.
        """
        experiment_directory = os.path.join(self._workspace, \
                                            self._experiment_name)
        
        # Make the directory if it doesn't exist
        if not os.path.isdir(experiment_directory):
            try:
                os.mkdir(experiment_directory)
                print 'Meggie: Creating experiment settings ... \n'
            except OSError:
                raise Exception('No rights to save to the chosen path or' + 
                                ' experiment name already exists. \n')
                return
        
        # String conversion, because shutil doesn't accept QStrings
        settingsFileName = str(self._experiment_name + '.exp')
        
        # Actually a file object
        settingsFile = open(os.path.join(experiment_directory, 
                            settingsFileName), 'wb')
        
        # Protocol 2 used because of file object being pickled
        pickle.dump(self, settingsFile, 2)
        print '[done]'
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
        self._active_subject_name = odict['_active_subject_name']
        
        
        self.__dict__.update(odict)    
        """
        rawFullPath = odict['_raw_data_path']
        workingFullPath = odict['_working_file_path']
        raw = mne.io.RawFIFF(rawFullPath, preload=True)
        self.raw_data = raw
        self.working_file = workingFullPath
        """
        
        
        
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
        # Releases memory from the previously open experiment
        #self.parent._experiment = None
        gc.collect()
        try:
            experiment = Experiment()
            experiment.author = expDict['author']
            experiment.experiment_name = expDict['name']
            experiment.description = expDict['description']
            experiment.subject_paths = []
        except AttributeError:
            message = 'Cannot assign attribute to experiment.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return None
        
        try:
            workspace = self.parent.preferencesHandler.working_directory
            experiment.workspace = workspace
        except Exception, err:
            self.messageBox = messageBoxes.shortMessageBox(str(err))
            self.messageBox.show()
            return None
        
        # Give control of the experiment to the main window of the application
        #self.parent.experiment = experiment
        
        try:
            experiment.save_experiment_settings()
        except Exception, err:
            self.messageBox = messageBoxes.shortMessageBox(str(err))
            self.messageBox.show()
            return None
        
        # Tell the preferencesHandler that this is the experiment we've had
        # open last.
        self.parent.preferencesHandler.previous_experiment_name = \
            expDict['name']
        self.parent.preferencesHandler.write_preferences_to_disk()
        
        # Update the main UI to be less empty and allow actions for a new
        # experiment. Also tell the MVC models they can initialize themselves.
        #self.parent.add_tabs()
        #self.parent._initialize_ui() 
        #self.parent.reinitialize_models() 
        return experiment
        
        
    def open_existing_experiment(self, name):
        """
        Opens an existing experiment, which is assumed to be in the working
        directory.
        
        Keyword arguments:
        
        name        -- name of the existing experiment to be opened
        """
        
        if name is not '':
            print "Opening experiment " + name
            try:
                path = os.path.join(
                            self.parent.preferencesHandler.working_directory, 
                            name)
            except IOError:
                mBox = messageBoxes.shortMessageBox("Error opening the expriment.")
                mBox.exec_()
                return
        else:
            return
        
        fname = os.path.join(path, path.split('/')[-1] + '.exp')
        if os.path.exists(path) and os.path.isfile(fname):
            caller = Caller.Instance()
            # Releases memory from the previously open experiment
            caller._experiment = None
            gc.collect()
            print "Opening file " + fname
            try:
                output = open(fname, 'rb')
                caller._experiment = pickle.load(output)
            except Exception as e:
                print str(e)
                return
            finally:
                print "Closing"
                output.close()
            caller.experiment.create_subjects(caller._experiment, caller._experiment._subject_paths)
            caller.activate_subject(caller._experiment._active_subject_name)
            self.parent.add_tabs()
            self.parent._initialize_ui()
            self.parent.reinitialize_models() 

            self.parent.preferencesHandler.previous_experiment_name = caller.experiment._experiment_name
            self.parent.preferencesHandler.write_preferences_to_disk()
        