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

from PyQt4.QtCore import QObject
from PyQt4 import QtGui,QtCore

import os, sys
import glob

import numpy as np
import mne

from measurementInfo import MeasurementInfo
import fileManager
from epochs import Epochs
from evoked import Evoked
from forwardModels import ForwardModels
import messageBox

class Subject(QObject):
    
    def __init__(self, experiment, subject_name):
        """
        Constructor for the subject class.
        
        Keyword arguments:
        working_file        -- the raw data file of the subject
        subject_name    -- the name of the subject
        """
        QObject.__init__(self)
        # Either user defined or the name of the data file.
        self._subject_name = subject_name
        #TODO: ID-juttuja.
        #self._subject_ID = ''
        self._event_set = None
        self._stim_channel = None
        self._working_file = None
        self._working_file_path = 'no path defined'
        self._experiment = experiment
        # Dictionary for epochs where key is the name of the collection
        # and value is the epochs object. Similar approach with evoked and
        # forward model objects.
        self._epochs = dict()
        self._evokeds = dict()
        self._forwardModels = dict()
        self._ecg_params = dict()
        self._subject_path = os.path.join(self._experiment.workspace,
                                          self._experiment.experiment_name,
                                          self._subject_name)
        self._epochs_directory = os.path.join(self._subject_path, 'epochs')
        self._evokeds_directory = os.path.join(self._epochs_directory, 'average')
        self._source_analysis_directory = os.path.join(self._subject_path, \
                                                     'sourceAnalysis')
        self._forwardModels_directory = os.path.join(self._subject_phath, \
                                                     'forwardModels')
        self._mri_directory = os.path.join(self._source_analysis_directory, 
                                           'mri')
        
    @property
    def raw_data(self):
        """
        Returns the raw data file of the subject.
        """
        return self._raw_data
    
    @raw_data.setter
    def raw_data(self, raw_data):
        """
        Sets the raw data file for the subject.
        Raises an exception if the given data type is wrong. 
        Keyword arguments:
        raw_data        -- the raw data file of the measured data
        """
        if (isinstance(raw_data, mne.fiff.Raw)):
            self._raw_data = raw_data
        else:
            raise Exception('Wrong data type')
        
    @property
    def subject_name(self):
        """
        Returns the subject_name of the subject.
        """
        return self._subject_name
    
    @subject_name.setter
    def subject_name(self, subject_name):
        """
        Sets the subject_name for the subject.
        """
        self._subject_name = subject_name
        
    @property
    def subject_path(self):
        """
        Returns the subject_path of the subject.
        """
        return self._subject_path
    
    @subject_path.setter
    def subject_path(self, subject_path):
        """
        Sets the subject_path for the subject.
        """
        self._subject_path = subject_path
                
    @property
    def working_file(self):
        """
        Returns the current working file.
        """
        return self._working_file
    
    @working_file.setter
    def working_file(self, raw):
        """
        Sets the current working file and notifies the main window to show it.
        Keyword arguments:
        raw         -- raw data file.
        """
        if (isinstance(raw, mne.fiff.Raw)):
            self._working_file = raw
        else:
            raise Exception('Wrong data type')

    @property
    def ecg_params(self):
        """Returns ecg_params.
        """
        return self._ecg_params

    @ecg_params.setter
    def ecg_params(self, ecg_params):
        """Sets ecg_params.
        
        Keyword arguments:
        ecg_params    -- dictionary of ecg parameters
        """
        self._ecg_params = ecg_params

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
        self._stim_channel = stim_ch
    
    def save_raw(self, file_name, path):
        """
        Saves the raw data file into the subject directory.
        Keyword arguments:
        file_name      -- the full path and name of the chosen raw data file
        path           -- path to the experiment directory
        """
        # See old version in save_raw method of original experiment.
        try:
            os.mkdir(path)
        except OSError:
            raise Exception('No rights to save to the chosen path or' + 
                            ' subject/experiment name already exists')
            return
        if os.path.exists(path):
            # TODO: Check if the file is saved with .fif suffix,
            # if not, save the file with .fif suffix.
            mne.fiff.Raw.save(self._working_file, os.path.join(path, \
                              str(os.path.basename(file_name))))
            self.create_epochs_directory()
            self.create_evokeds_directory()
            
            # Save channel names list under subject folder
            fileManager.pickle(self._working_file.ch_names, os.path.join(self._subject_path, 'channels'))
        else:
            raise Exception('No rights to save the raw file to the chosen ' + 
                            'path or bad raw file name.')

        
    def create_epochs_directory(self):
        """
        Create a directory for saving epochs under the subject directory.
        TODO possibly move this and following methods to fileManager.
        """
        try:
            os.mkdir(self._epochs_directory)
        except OSError:
            raise OSError('can\'t create epochs directory to' + \
                          ' the chosen path')                


    def create_evokeds_directory(self):
        """
        Create a directory for saving evokeds under the epochs directory.
        """
        try:
            os.mkdir(self._evokeds_directory)
        except OSError:
            raise OSError('can\'t create evokeds directory to' + \
                          ' the chosen path')                

    def create_forwardModels_directory(self):
        """
        Create a directory for saving forward models under the appropriate
        directory.
        """
        try:
            os.mkdir(self._forwardModels_directory)
        except OSError:
            raise OSError('can\'t create forward models directory to' + \
                          ' the chosen path')
        
    def create_sourceAnalysis_directory(self):
        try:
            os.mkdir(self._source_analysis_directory)
        except OSError:
            raise OSError('can\'t create source analysis directory to' + \
                          ' the chosen path')
        
    def create_mri_directory(self):
        
        try:
            os.mkdir(self._mri_directory)
        except OSError:
            raise OSError('can\'t create mri directory to' + \
                          ' the chosen path')
    
    def find_stim_channel(self):
        """
        Finds the correct stimulus channel for the data.
        """
        channels = self._working_file.info.get('ch_names')
        if any('STI101' in channels for x in channels):
            self._stim_channel = 'STI101'
        elif any('STI 014' in channels for x in channels):
            self._stim_channel = 'STI 014'

    def create_event_set(self):
        """
        Creates an event set where the first element is the id
        and the second element is the number of the events.
        Raises type error if the working_file attribute is not set or
        if the data is not of type mne.fiff.Raw.
        """
        if not isinstance(self._working_file, mne.fiff.Raw):
            raise TypeError('Nt a raw object')
        if self.stim_channel == None:
            return
        events = mne.find_events(self._working_file,
                                 stim_channel=self._stim_channel)
        bins = np.bincount(events[:,2]) #number of events stored in an array
        d = dict()
        for i in set(events[:,2]):
            d[i] = bins[i]
        self._event_set = d

    def add_epochs(self, epochs):
        """
        Adds Epochs object to the epochs dictionary.
        
        Keyword arguments:
        epochs      -- Epochs object including raw.fif, param.fif and
                       collection_name
        """
        self._epochs[epochs._collection_name] = epochs
        
    def handle_new_epochs(self, name, epochs_raw, params):
        """
        Creates Epochs object and adds it to the self._epochs dictionary.
        Does nothing if given collection name exists in epochs dictionary.
        
        Keyword arguments
        name        -- name of the epoch collection
        epochs_raw  -- raw epochs file
        params      -- epochs parameters
        """
        # Checks if epochs with given name exists.
        if self._epochs.has_key(name):
            return
        #toPyObject turns the dict keys into QStrings so convert them back to
        #strings.
        #params_str = dict((str(k), v) for k, v in parameters.iteritems())
        epochs = Epochs()
        epochs._collection_name = name
        epochs._raw = epochs_raw
        epochs._params = params
        self.add_epochs(epochs)
    
    @QtCore.pyqtSlot(dict, QtGui.QListWidget)  
    def modify_epochs(self, epoch_params, epoch_widget):
        """Overwrite the existing epoch_item with new epochs.
        The signal is emitted by epoch_params_ready on eventSelectionDialogMain
        accept method. The signal is connected to this method only on 
        on_pushButtonModifyEpochs_clicked method. 
        
        Returns item including epoch params and raw.
        
        Keyword arguments:
        epoch_params     -- A dict containing the parameter values for the
                            epochs.
        epoch_widget     -- QListWidget object containing epoch items
        """
        current_collection = str(epoch_widget.currentItem().text())
        # Removes Epochs object and item.
        self.remove_epochs(current_collection)
        epoch_widget.remove_item(epoch_widget.currentItem())
        e = Epochs()
        epochs = e.create_epochs_from_dict(epoch_params, self._experiment.\
                                           active_subject.\
                                           working_file)
        epoch_params['raw'] = self._experiment.active_subject_raw_path #working_file_path
        #Create a QListWidgetItem and add the actual epochs to slot 32.
        item = QtGui.QListWidgetItem(epoch_params['collectionName'])
        # TODO: remove setData
        item.setData(32, epochs)
        item.setData(33, epoch_params)
        self.create_epochs_object_from_item(epoch_params['collectionName'], item)
        epoch_widget.addItem(item)
        epoch_widget.setCurrentItem(item)
        
    def remove_epochs(self, collection_name):
        """
        Removes epochs from epochs dictionary.
        Removes the files with collection_name.
        
        Keyword arguments:
        collection_name    -- name of the epochs collection (QString)
        """
        collection_name = str(collection_name)
        del self._epochs[collection_name]
        
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
        
        if fileManager.delete_file_at(self._epochs_directory, files_to_delete) == False:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Epochs could not be deleted from epochs folder.')
            self.messageBox.show()
        
    def handle_new_evoked(self, name, evoked, categories):
        """
        Creates new Evoked object and adds it to the self._evokeds dictionary.
        Does nothing if given evoked name that is in self._evokeds.keys().
        
        Keyword arguments
        name       -- name of the evoked in QString
        evoked     -- raw evoked file
        categories -- dict() of events in epochs.event_id
        """
        # Checks if evoked with given name exists.
        if self._evokeds.has_key(str(name)):
            return
        #evoked_object = self.create_evoked_object(name, evoked, categories)
        
        evoked_object = Evoked()
        if evoked is None:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Evoked is None.')
            self.messageBox.show()
            return
        evoked_object._raw = evoked
        evoked_object._name = str(name)
        evoked_object._categories = categories
        self.add_evoked(name, evoked_object)
    
    def add_evoked(self, name, evoked_object):
        """
        Adds Evoked object to the evokeds dictionary.
        
        Keyword arguments:
        evoked_object  -- Evoked object
        """
        self._evokeds[str(name)] = evoked_object
        
    def remove_evoked(self, name):
        """
        Removes evoked object from the evoked dictionary.
        
        
        Keyword arguments:
        name    -- name of the evoked in QString
        """
        # TODO should not do this if f.delete_file_at fails
        del self._evokeds[str(name)]
        
        if fileManager.delete_file_at(self._evokeds_directory, name) == False:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Evoked could not be deleted from average folder.')
            self.messageBox.show()
        
        
    def add_forwardModel(self, name, fmodel):
        """
        Adds a ForwardModels object to the forwardModels dictionary.
        """
        self._evokeds[str(name)] = fmodel
        
        
    def remove_forwardModel(self, name):
        """
        Removes a ForwardModels object from the forwardModels dictionary.
        """
        if fileManager.delete_file_at(self._forwardModels_directory, name) == False:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText \
            ('Forward model could not be deleted from forwardModels folder')
            self.messageBox.show()
            return
        del self._forwardModels[str(name)]
    
    
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
        fmodels._fmodel_name = name
        fmodel._params = params
        self.add_forwardModel(name, fmodel)
    
        
    def check_ecg_projs(self):
        """
        Checks the subject folder for ECG projection files.
        Returns True if projections found.
        """
        path = self._subject_path
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
        path = self._subject_path
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
        path = self._subject_path
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
        path = self._subject_path
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
        path = self._subject_path
        #Check whether sss/tsss method is applied.
        files = filter(os.path.isfile, glob.glob(path + '/*sss*'))
        if len(files) > 0:
            return True
        return False
