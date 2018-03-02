# coding: utf-8

"""
Created on Oct 22, 2013

@author: jaolpeso
"""

import os
import glob

import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.epoching.events import Events

class Subject(object):
    
    def __init__(self, experiment, subject_name, working_file_name):
        """
        Constructor for the subject class.
        
        Keyword arguments:
        experiment        -- experiment for the subject
        subject_name      -- the name of the subject
        working_file_name -- the name of the subject's working file that can be
                             different from subject_name
        """
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
        self._reconfiles_directory = os.path.join(self._source_analysis_directory, 'reconFiles')  # noqa
        self._forward_solutions_directory = os.path.join(self._source_analysis_directory, 'forwardSolutions')  # noqa
        self._stc_directory = os.path.join(self._source_analysis_directory, 'stc')  # noqa

        self._transfile_path = os.path.join(self._source_analysis_directory, 
                                            'mri_meg-trans.fif')

        self._experiment = experiment

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
    def reconfiles_directory(self):
        return self._reconfiles_directory
    
    @property
    def forward_solutions_directory(self):
        return self._forward_solutions_directory  

    @property
    def stc_directory(self):
        return self._stc_directory

    @property
    def transfile_path(self):
        return self._transfile_path

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
    
    @working_file_name.setter
    def working_file_name(self, name):
        self._working_file_name = name

    def set_working_file(self, working_file):
        self._working_file = working_file

    def get_working_file(self, preload=True, temporary=False):
        """
        Returns the current working raw object.
        """
        if isinstance(self._working_file, mne.RAW_TYPE):
            if preload:
                self._working_file.load_data()
            return self._working_file
        else:
            raw = self.load_working_file(preload)
            if not temporary:
                self._working_file = raw
            return raw

    @property
    def layout(self):
        return self._layout
    
    @layout.setter
    def layout(self, layout):
        self._layout = layout

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
                return fileManager.open_raw(os.path.join(path, self.working_file_name), preload=preload)
            except OSError:
                raise IOError("Couldn't find raw file.")
            
    def release_memory(self):
        """Releases memory from previously processed subject by removing
        references from raw files.
        """
        try:
            working_file = self.get_working_file()
        except:
            working_file = None
        
        if working_file is not None:
            self.set_working_file(None)
            if len(self.epochs) > 0:
                for value in self.epochs.values():
                    value.raw = None
            if len(self.evokeds) > 0:
                for value in self.evokeds.values():
                    value.forget_evokeds()

    def find_stim_channel(self):
        """
        Finds the correct stimulus channel for the data.
        """
        channels = self.get_working_file().info.get('ch_names')
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
        events = self.get_events()
        if events is None:
            return
        bins = np.bincount(events[:,2]) #number of events stored in an array
        d = dict()
        for i in set(events[:,2]):
            d[i] = bins[i]
        return d

    def get_events(self):
        """Helper for reading the events."""
        
        stim_channel = self.find_stim_channel()
        if not stim_channel:
            return

        return Events(self._experiment, self.get_working_file(),
                      stim_ch=stim_channel).events
        
    def get_cov(self):
        """Helper method for getting the current covariance matrix."""
        sa_dir = self._source_analysis_directory
        files = os.listdir(sa_dir)
        cov_file = [f for f in files if f.endswith('-cov.fif')]
        if len(cov_file) == 0:
            raise ValueError('No covariance file found.')
        elif len(cov_file) > 1:
            raise ValueError('Multiple covariance files found. Remove the '
                             'other one!')
        else:
            cov_file = cov_file[0]
        return mne.read_cov(os.path.join(sa_dir, cov_file))

    def add_epochs(self, epochs):
        """
        Adds Epochs object to the epochs dictionary.

        Keyword arguments:
        epochs      -- Epochs object including param.fif and collection_name
        """
        self._epochs[epochs.collection_name] = epochs

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
        for i in range(len(files_to_delete)):
            files_to_delete[i] = os.path.basename(files_to_delete[i])
        try:
            fileManager.delete_file_at(self._epochs_directory, files_to_delete)
        except OSError:
            raise IOError('Epochs could not be deleted from epochs folder.')
        self._epochs.pop(str(str(collection_name)), None)

    def add_evoked(self, evoked):
        """
        Adds Evoked object to the evokeds dictionary.

        Keyword arguments:
        evoked  -- Evoked object
        """
        self._evokeds[evoked.name] = evoked

    def remove_evoked(self, name):
        """
        Removes evoked object from the evoked dictionary.

        Keyword arguments:
        name    -- name of the evoked in QString
        """
        try:
            fileManager.delete_file_at(self._evokeds_directory, name)
        except OSError:
            raise IOError('Evoked could not be deleted from average folder.')
        self._evokeds.pop(str(name), None)


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
    
    def check_eeg_projs(self):
        """
        Checks the subject folder for EEG projection files.
        Returns True if projections found.
        """
        path = self.subject_path
        #Check whether EEG projections are calculated
        files =  filter(os.path.isfile, glob.glob(path + '/*_eeg_proj*'))
        files += filter(os.path.isfile, glob.glob(path + '/*_eeg-eve*'))
        if len(files) > 1:
            return True
        return False
        
    def check_ecg_applied(self):
        """
        Checks the subject folder for ECG applied file.
        Returns True if ecg_applied found.
        """
        raw = self.get_working_file()
        projs = raw.info['projs']
        return any('ECG' in str(proj) for proj in projs)
        
    def check_eog_applied(self):
        """
        Checks the subject folder for EOG applied file.
        Returns True if eog_applied found.
        """
        raw = self.get_working_file()
        projs = raw.info['projs']
        return any('EOG' in str(proj) for proj in projs)

    def check_eeg_applied(self):
        """
        Checks the subject folder for EEG applied file.
        Returns True if eeg_applied found.
        """
        raw = self.get_working_file()
        projs = raw.info['projs']
        return any('Ocular' in str(proj) for proj in projs)

    def check_sss_applied(self):
        """
        Checks the subject folder for sss/tsss applied file.
        Returns True if sss/tsss found.
        """
        path = self.subject_path
        #Check whether sss/tsss method is applied.
        files = []
        files = filter(os.path.isfile, glob.glob(path + '/*sss*'))
        files.extend(filter(os.path.isfile, glob.glob(path + '/*_mc*')))
        if len(files) > 0:
            return True
        return False

    def check_reconFiles_copied(self):
        reconDir = self.reconfiles_directory
        mriDir = os.path.join(reconDir, 'mri/') 
        if os.path.isdir(mriDir):
            return True
        else: 
            return False

    def check_bem_surfaces(self):
        rcdir = self.reconfiles_directory
        if not os.path.isfile(os.path.join(rcdir, 'bem', 'inner_skull.surf')):
            return False
        if not os.path.isfile(os.path.join(rcdir, 'bem', 'outer_skull.surf')):
            return False
        if not os.path.isfile(os.path.join(rcdir, 'bem', 'outer_skin.surf')):
            return False
        return True

    def check_mne_setup_mri_run(self):
        reconDir = self.reconfiles_directory
        mriDir = os.path.join(reconDir, 'mri/') 
        T1NeuroMagDir = os.path.join(mriDir, 'T1-neuromag/')
        brainNeuroMagDir = os.path.join(mriDir, 'brain-neuromag/')
        if os.path.isdir(T1NeuroMagDir) and os.path.isdir(brainNeuroMagDir):
            return True
        else:
            return False

    def get_forward_solution_names(self):
        names = filter(lambda x: x.endswith('fwd.fif'), 
                       os.listdir(self.forward_solutions_directory))
        return names
