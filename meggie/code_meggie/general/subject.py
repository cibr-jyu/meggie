# coding: utf-8

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

from PyQt4.QtCore import QObject
from PyQt4 import QtGui
from PyQt4 import QtCore

import os
import glob

import numpy as np
import mne

from meggie.code_meggie.general import fileManager
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.epoching.evoked import Evoked
from meggie.code_meggie.sourceModeling.forwardModels import ForwardModels

from meggie.ui.utils.decorators import messaged

class Subject(QObject):
    
    def __init__(self, experiment, subject_name, working_file_name):
        """
        Constructor for the subject class.
        
        Keyword arguments:
        experiment        -- experiment for the subject
        subject_name      -- the name of the subject
        working_file_name -- the name of the subject's working file that can be
                             different from subject_name
        """
        QObject.__init__(self)
        # Either user defined or the name of the data file.
        self._subject_name = subject_name
        self._working_file = None
        self._working_file_name = working_file_name

        # Dictionary for epochs where key is the name of the collection
        # and value is the epochs object. Similar approach with evoked and
        # forward model objects.
        self._epochs = dict()
        self._evokeds = dict()
        self._subject_path = os.path.join(experiment.workspace,
                                          experiment.experiment_name,
                                          subject_name)
        
        self._epochs_directory = os.path.join(self._subject_path, 'epochs')
        self._evokeds_directory = os.path.join(self._epochs_directory, 'average')  # noqa
        self._source_analysis_directory = os.path.join(self._subject_path, 'sourceAnalysis')  # noqa
        self._reconFiles_directory = os.path.join(self._source_analysis_directory, 'reconFiles')  # noqa
        self._forwardModels_directory = os.path.join(self._source_analysis_directory, 'forwardModels')  # noqa

        # Models for various types of data stored in subject
        self._forwardModelModel = None   

    @property
    def epochs_directory(self):
        return self._epochs_directory

    @property
    def evokeds_directory(self):
        return self._evokeds_directory
    
    @property
    def source_analysis_directory(self):
        return self._source_analysis_directory
    
    @property
    def reconFiles_directory(self):
        return self._reconFiles_directory
    
    @property
    def forwardModels_directory(self):
        return self._forwardModels_directory  

    @property
    def subject_name(self):
        """
        Returns the subject_name of the subject.
        """
        return self._subject_name
        
    @property
    def subject_path(self):
        """
        Returns the subject_path of the subject.
        """
        return self._subject_path
    
    @property
    def working_file_path(self):
        path = os.path.join(self._subject_path,
                            self._working_file_name)
        return path
    
    @property
    def working_file_name(self):
        return self._working_file_name

    def set_working_file(self, working_file):
        self._working_file = working_file

    def get_working_file(self, preload=True):
        """
        Returns the current working raw object.
        """
        if isinstance(self._working_file, mne.io.Raw):
            return self._working_file
        else:
            self._working_file = self.load_working_file(preload)
            return self._working_file

    @property
    def epochs(self):
        return self._epochs
    
    @property
    def evokeds(self):
        return self._evokeds
    
    def load_working_file(self, preload=True):
        """Loads raw file from subject folder and sets it on
        subject._working_file property.
         
        Keyword arguments:
        subject    -- Subject object
        """
        if self._working_file is None:
            path = self.subject_path
            try:
                return fileManager.open_raw(os.path.join(path, self.working_file_name))
            except OSError:
                raise IOError("Couldn't find raw file.")
            
    def release_memory(self):
        """Releases memory from previously processed subject by removing
        references from raw files.
        """
        if self.get_working_file() is not None:
            self.set_working_file(None)
            if len(self.epochs) > 0:
                for value in self.epochs.values():
                    value.raw = None
            if len(self.evokeds) > 0:
                for value in self.evokeds.values():
                    value.raw = None    

    def find_stim_channel(self):
        """
        Finds the correct stimulus channel for the data.
        """
        channels = self._working_file.info.get('ch_names')
        if 'STI101' in channels:
            return 'STI101'
        elif 'STI 101' in channels:
            return 'STI 101'
        elif 'STI 014' in channels:
            return 'STI 014'
        elif 'STI014' in channels:
            return 'STI014'
    
    def create_event_set(self):
        """
        Creates an event set where the first element is the id
        and the second element is the number of the events.
        Raises type error if the working_file attribute is not set or
        if the data is not of type mne.io.Raw.
        """
        if not isinstance(self._working_file, mne.io.Raw):
            raise TypeError('Not a raw object')

        events = self.get_events()
        
        bins = np.bincount(events[:,2]) #number of events stored in an array
        d = dict()
        for i in set(events[:,2]):
            d[i] = bins[i]
        return d

    def get_events(self):
        """Helper for reading the events."""
        
        stim_channel = self.find_stim_channel()
        
        try:
            events = mne.find_events(self._working_file)
        except Exception as e:
            print 'Warning: %s' % e
            print 'Reading events with minimum length of 1...'
            events = mne.find_events(self.working_file,
                                     stim_channel=stim_channel,
                                     shortest_event=1)
        return events

    def add_epochs(self, epochs):
        """
        Adds Epochs object to the epochs dictionary.

        Keyword arguments:
        epochs      -- Epochs object including param.fif and collection_name
        """
        self._epochs[epochs.collection_name] = epochs

    @messaged
    def remove_epochs(self, collection_name):
        """
        Removes epochs from epochs dictionary.
        Removes the files with collection_name.

        Keyword arguments:
        collection_name    -- name of the epochs collection (QString)
        """
        files_to_delete = filter(os.path.isfile, glob.\
                                 glob(os.path.join(self._epochs_directory, \
                                                   collection_name + '.fif')))
        files_to_delete += filter(os.path.isfile, glob.\
                                  glob(os.path.join(self._epochs_directory, \
                                                    collection_name + '.param')))
        files_to_delete += filter(os.path.isfile, glob.\
                                  glob(os.path.join(self._epochs_directory, \
                                                    collection_name + '.csv')))
        for i in range(len(files_to_delete)):
            files_to_delete[i] = os.path.basename(files_to_delete[i])
        self._epochs.pop(str(str(collection_name)), None)
        try:
            fileManager.delete_file_at(self._epochs_directory, files_to_delete)
        except OSError:
            raise IOError('Epochs could not be deleted from epochs folder.')

    def add_evoked(self, evoked):
        """
        Adds Evoked object to the evokeds dictionary.

        Keyword arguments:
        evoked  -- Evoked object
        """
        self._evokeds[evoked.name] = evoked

    @messaged
    def remove_evoked(self, name):
        """
        Removes evoked object from the evoked dictionary.

        Keyword arguments:
        name    -- name of the evoked in QString
        """
        self._evokeds.pop(str(name), None)
        try:
            fileManager.delete_file_at(self._evokeds_directory, name)
        except OSError:
            raise IOError('Evoked could not be deleted from average folder.')

    @messaged
    def remove_power(self, name):
        """
        Removes AVGPower object from the TFR dictionary.

        Keyword arguments:
        name    -- Name of the file as string.
        """
        path = os.path.join(self.subject_path, 'TFR')
        try:
            fileManager.delete_file_at(path, name)
        except OSError as err:
            raise IOError('The file could not be deleted from TFR folder.')

### Code related to source modeling ###

    def add_forwardModel(self, name, fmodel):
        """
        Adds a ForwardModels object to the forwardModels dictionary.
        """
        self._forwardModels[str(name)] = fmodel
    
    
    def handle_new_forwardModels(self, name, params):
        """
        Creates a forward model object and adds it to the 
        self._forwardModels dictionary.
        Does nothing if given collection name exists already in the dictionary.
        
        Keyword arguments
        name        -- name of the forward model
        params      -- forward model parameters
        """
        # Checks if forward model with given name exists.
        if self._forwardModels.has_key(name):
            return
        #toPyObject turns the dict keys into QStrings so convert them back to
        #strings.
        #params_str = dict((str(k), v) for k, v in parameters.iteritems())
        fmodel = ForwardModels()
        fmodel._fmodel_name = name
        fmodel._params = params
        self.add_forwardModel(name, fmodel)
    
### Code for checking the state of the subject ###   

    def check_ecg_projs(self):
        """
        Checks the subject folder for ECG projection files.
        Returns True if projections found.
        """
        path = self.subject_path
        #Check whether ECG projections are calculated
        files =  filter(os.path.isfile, glob.glob(path + '/*_ecg_avg_proj*'))
        files += filter(os.path.isfile, glob.glob(path + '/*_ecg_proj*'))
        files += filter(os.path.isfile, glob.glob(path + '/*_ecg-eve*'))
        if len(files) > 1:
            return True
        return False           
        
    def check_eog_projs(self):
        """
        Checks the subject folder for EOG projection files.
        Returns True if projections found.
        """
        path = self.subject_path
        #Check whether EOG projections are calculated
        files =  filter(os.path.isfile, glob.glob(path + '/*_eog_avg_proj*'))
        files += filter(os.path.isfile, glob.glob(path + '/*_eog_proj*'))
        files += filter(os.path.isfile, glob.glob(path + '/*_eog-eve*'))
        if len(files) > 1:
            return True
        return False
        
    def check_ecg_applied(self):
        """
        Checks the subject folder for ECG applied file.
        Returns True if ecg_applied found.
        """
        path = self.subject_path
        #Check whether ECG projections are applied
        files = filter(os.path.isfile, glob.glob(path + '/*ecg_applied*'))
        if len(files) > 0:
            return True
        return False
        
    def check_eog_applied(self):
        """
        Checks the subject folder for EOG applied file.
        Returns True if eog_applied found.
        """
        path = self.subject_path
        #Check whether EOG projections are applied
        files = filter(os.path.isfile, glob.glob(path + '/*eog_applied*'))
        if len(files) > 0:
            return True
        return False

    def check_sss_applied(self):
        """
        Checks the subject folder for sss/tsss applied file.
        Returns True if sss/tsss found.
        """
        path = self.subject_path
        #Check whether sss/tsss method is applied.
        files = filter(os.path.isfile, glob.glob(path + '/*sss*'))
        if len(files) > 0:
            return True
        return False

    def check_reconFiles_copied(self):
        reconDir = self.reconFiles_directory
        mriDir = os.path.join(reconDir, 'mri/') 
        if os.path.isdir(mriDir):
            return True
        else: 
            return False

    def check_mne_setup_mri_run(self):
        reconDir = self.reconFiles_directory
        mriDir = os.path.join(reconDir, 'mri/') 
        T1NeuroMagDir = os.path.join(mriDir, 'T1-neuromag/')
        brainNeuroMagDir = os.path.join(mriDir, 'brain-neuromag/')
        if os.path.isdir(T1NeuroMagDir) and os.path.isdir(brainNeuroMagDir):
            return True
        else:
            return False
