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

import os, sys
import glob

import numpy as np
import mne

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
        # and value is the epochs object.
        self._epochs = dict()
        self._subject_path = os.path.join(self._experiment.workspace,
                                          self._experiment.experiment_name,
                                          self._subject_name)
        self._epochs_directory = os.path.join(self._subject_path, 'epochs')
        
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
    def working_file(self, fname):
        """
        Sets the current working file and notifies the main window to show it.
        Keyword arguments:
        fname         -- Name of the new working file.
        """
        if (isinstance(fname, mne.fiff.Raw)):
            self._working_file = fname
        else:
            raise Exception('Wrong data type')

        
        #self._working_file = mne.fiff.Raw(fname, preload=True)
        #self.working_file_path = fname

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
        else:
            raise Exception('No rights to save the raw file to the chosen ' + 
                            'path or bad raw file name.')
        
    def create_epochs_directory(self):
        """Create a directory for saving epochs under the subject directory.
        """
        try:
            os.mkdir(self._epochs_directory)
        except OSError:
            raise OSError('no rights to save to the chosen path')                
    
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
        
    def add_epochs(self, epochs, name):
        """
        Creates epochs object and adds it to the epochs list.
        
        Keyword arguments:
        epochs    -- raw epochs file
        name      -- name of the collection
        """
        
        # TODO: Create epochs object here before adding?
        # In that case you should give this method params, raw and
        # collection_name to create epochs object.
        self._epochs[name] = epochs
        
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
