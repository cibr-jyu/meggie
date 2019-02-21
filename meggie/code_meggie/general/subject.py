# coding: utf-8

"""
"""

import os
import shutil
import glob

import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.structures.events import Events

class Subject(object):
    
    def __init__(self, experiment, subject_name, working_file_name,
                  ica_applied=False, rereferenced=False):
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

        self._ica_applied = ica_applied
        self._rereferenced = rereferenced

        self._epochs = dict()
        self._evokeds = dict()
        self._spectrums = dict()
        self._tfrs = dict()
        self._stcs = dict()
        self._subject_path = os.path.join(experiment.workspace,
                                          experiment.experiment_name,
                                          subject_name)

        self._mri_subject_name = 'reconFiles'
        
        self._epochs_directory = os.path.join(self._subject_path, 'epochs')

        self._evokeds_directory = os.path.join(self._epochs_directory, 
                                               'average')

        self._source_analysis_directory = os.path.join(self._subject_path, 
                                                       'sourceAnalysis')
        self._reconfiles_directory = os.path.join(
            self._source_analysis_directory, self._mri_subject_name)

        self._forward_solutions_directory = os.path.join(
            self._source_analysis_directory, 'forwardSolutions')

        self._stc_directory = os.path.join(self._source_analysis_directory, 
                                           'stc')

        self._transfile_path = os.path.join(self._source_analysis_directory, 
                                            'mri_meg-trans.fif')

        self._cov_directory = os.path.join(self._source_analysis_directory, 
                                           'cov')

        self._spectrums_directory = os.path.join(self._subject_path, 
                                                 'spectrums')

        self._tfr_directory = os.path.join(self._subject_path, 
                                           'tfrs')

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
    def inverse_operators_directory(self):
        return self._inverse_operators_directory  

    @property
    def stc_directory(self):
        return self._stc_directory

    @property
    def transfile_path(self):
        return self._transfile_path

    @property
    def cov_directory(self):
        return self._cov_directory

    @property
    def spectrums_directory(self):
        return self._spectrums_directory

    @property
    def tfr_directory(self):
        return self._tfr_directory

    @property
    def mri_subject_name(self):
        return self._mri_subject_name

    @property
    def ica_applied(self):
        """
        """
        return self._ica_applied

    @ica_applied.setter
    def ica_applied(self, value):
        """
        """
        self._ica_applied = value

    @property
    def rereferenced(self):
        """
        """
        return self._rereferenced

    @rereferenced.setter
    def rereferenced(self, value):
        """
        """
        self._rereferenced = value

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

    @property
    def spectrums(self):
        return self._spectrums

    @property
    def tfrs(self):
        return self._tfrs

    @property
    def stcs(self):
        return self._stcs
    
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
        
    def add_epochs(self, epochs):
        """
        Adds Epochs object to the epochs dictionary.

        """
        self._epochs[epochs.collection_name] = epochs

    def remove_epochs(self, collection_name):
        """
        Removes epochs from epochs dictionary.
        Removes the files with collection_name.

        Keyword arguments:
        collection_name    -- name of the epochs collection (QString)
        """

        self._epochs.pop(str(str(collection_name)), None)

        files_to_delete = list(filter(os.path.isfile, 
            glob.glob(os.path.join(self._epochs_directory, 
                                   collection_name + '.fif'))))

        for i in range(len(files_to_delete)):
            files_to_delete[i] = os.path.basename(files_to_delete[i])

        try:
            fileManager.delete_file_at(self._epochs_directory, files_to_delete)
        except OSError:
            raise IOError('Epochs could not be deleted from epochs folder.')

    def add_spectrum(self, spectrum):
        self._spectrums[spectrum.name] = spectrum

    def remove_spectrum(self, name):

        spectrum = self._spectrums.pop(str(name), None)
        try:
            spectrum.delete_data()
        except OSError:
            raise IOError('Spectrum could not be deleted from folders.')

    def add_tfr(self, tfr):
        self._tfrs[tfr.name] = tfr

    def remove_tfr(self, name):

        tfr = self._tfrs.pop(str(name), None)
        try:
            tfr.delete_tfr()
        except OSError:
            raise IOError('TFR could not be deleted from folders.')

    def add_evoked(self, evoked):
        """
        Adds Evoked object to the evokeds dictionary.

        Keyword arguments:
        evoked  -- Evoked object
        """
        self._evokeds[evoked.name] = evoked

    def remove_evoked(self, name):
        """
        Removes evoked object from the evoked dictionary and file system

        Keyword arguments:
        name    -- name of the evoked in QString
        """
        self._evokeds.pop(str(name), None)

        try:
            fileManager.delete_file_at(self._evokeds_directory, name)
        except OSError:
            raise IOError('Evoked could not be deleted from average folder.')

    def add_stc(self, stc):
        """
        Adds SourceEstimate object to the stcs dictionary.

        """
        if not stc.name in self._stcs:
            self._stcs[stc.name] = stc

    def remove_stc(self, name):
        """
        """
        self._stcs.pop(str(name), None)

        path = os.path.join(self.stc_directory, name)
        try:
            shutil.rmtree(path)
        except OSError:
            raise IOError('Source estimate could not be removed from the file system')

    def check_ecg_projs(self):
        """
        Checks the subject folder for ECG projection files.
        Returns True if projections found.
        """
        path = self.subject_path
        # check whether ECG projections are calculated
        files = list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_ecg_avg_proj*'))))
        files += list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_ecg_proj*'))))
        files += list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_ecg-eve*'))))
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
        files = list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_eog_avg_proj*'))))
        files += list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_eog_proj*'))))
        files += list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_eog-eve*'))))
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
        files = list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_eeg_proj*'))))
        files += list(filter(os.path.isfile, glob.glob(os.path.join(path, '*_eeg-eve*'))))
        if len(files) > 1:
            return True
        return False
        
    def check_sss_applied(self):
        """
        Checks the subject folder for sss/tsss applied file.
        Returns True if sss/tsss found.
        """

        raw = self.get_working_file()
        for item in raw.info['proc_history']:
            if 'maxfilter' in item['creator']:
                return True

        return False

    def check_transfile_exists(self):
        path = self.transfile_path

        if os.path.isfile(path):
            return True

        return False

    def check_reconFiles_copied(self):
        reconDir = self.reconfiles_directory
        mriDir = os.path.join(reconDir, 'mri') 
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
        mriDir = os.path.join(reconDir, 'mri') 
        T1NeuroMagDir = os.path.join(mriDir, 'T1-neuromag')
        brainNeuroMagDir = os.path.join(mriDir, 'brain-neuromag')
        if os.path.isdir(T1NeuroMagDir) and os.path.isdir(brainNeuroMagDir):
            return True
        else:
            return False

    def get_forward_solution_names(self):
        names = list(filter(lambda x: x.endswith('fwd.fif'), 
                            os.listdir(self.forward_solutions_directory)))
        return names

    def get_covfiles(self):
        fnames = list(filter(lambda x: x.endswith('-cov.fif'),
                             os.listdir(self.cov_directory)))
        return fnames

    def get_inverse_operator_names(self):
        names = list(filter(lambda x: x.endswith('inv.fif'), 
                            os.listdir(self.inverse_operators_directory)))
        return names

    def ensure_folders(self):
        try:
            fileManager.ensure_folders([
                self.subject_path,
                self.epochs_directory,
                self.evokeds_directory,
                self.source_analysis_directory,
                self.forward_solutions_directory,
                self.reconfiles_directory,
                self.spectrums_directory,
                self.tfr_directory,
                self.cov_directory,
                self.stc_directory
            ])
        except OSError:
            raise OSError("Couldn't create all the necessary folders. "
                          "Do you have the necessary permissions?")
