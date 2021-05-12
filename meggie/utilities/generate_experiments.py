"""Provides functions to generate experiments from sample data.
"""

import os
import sys
import shutil
import tempfile

import mne
import numpy as np

from meggie.subject import Subject
from meggie.mainwindow.preferences import PreferencesHandler

from meggie.experiment import initialize_new_experiment
from meggie.experiment import open_existing_experiment


def create_experiment(experiment_folder, experiment_name, subjects_raw, overwrite=False):
    """Creates experiment from list of raw objects.

    Parameters
    ----------
    experiment_folder : str
        Where the experiment is stored.
    experiment_name : str
        Name of the experiment.
    subjects_raw : list
        List of raws, one for each subject.
    overwrite : bool
        Whether to overwrite previous experiment with a same name. 

    Returns
    -------
    meggie.experiment.Experiment
        An experiment object containing the subjects.
    """

    if os.path.exists(os.path.join(experiment_folder, experiment_name)):
        if overwrite:
            shutil.rmtree(os.path.join(experiment_folder, experiment_name))
        else:
            raise Exception('Experiment already exists')

    # Create preferences object to store working directory
    prefs = PreferencesHandler()
    prefs.workspace = experiment_folder

    # create experiment (creates experiment directory inside working directory)
    name = experiment_name
    author = 'Test'
    experiment = initialize_new_experiment(name, author, prefs, set_previous_experiment=False)

    for subject_idx, raw in enumerate(subjects_raw):
        with tempfile.TemporaryDirectory() as sample_folder:

            fname = 'sample_' + str(subject_idx+1).zfill(2) + '-raw.fif'

            raw_path = os.path.join(sample_folder, fname)
            raw.save(raw_path)

            subject_name = fname.split('.fif')[0]
            experiment.create_subject(subject_name, 
                                      raw_path)

    experiment.save_experiment_settings()
    return experiment


def create_evoked_conditions_experiment(experiment_folder, experiment_name, overwrite=False, n_subjects=35):
    """Generate multisubject experiment based on sample_audvis_raw for testing purposes.

    Subjects are generated so that each will contain different versions of two LA and RA auditory responses.

    Parameters
    ----------
    experiment_folder : str
        Where the experiment is stored.
    experiment_name : str
        Name of the experiment.
    overwrite : bool
        Whether to overwrite previous experiment with a same name. 
    n_subjects : int
        How many subjects to add.

    Returns
    -------
    meggie.experiment.Experiment
        An experiment object containing the subjects.
    """
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

    subjects_raw = []

    # generate data
    raw = mne.io.read_raw_fif(sample_fname, preload=True)
    events = mne.find_events(raw)

    la_events = [ev for ev in events if ev[2] == 1]
    ra_events = [ev for ev in events if ev[2] == 2]

    for subject_idx in range(n_subjects):
        data = []
        combined_events = la_events[subject_idx*2:subject_idx*2+2]
        combined_events.extend(ra_events[subject_idx*2:subject_idx*2+2])

        if len(combined_events) != 4:
            raise Exception('Something wrong with event counts')

        data = []
        for event in combined_events:
            tidx = event[0]
            try:
                ev_before = [ev for ev in events if ev[0] < tidx][-1]
                tmin = (ev_before[0] - raw.first_samp + 20) / raw.info['sfreq']
            except:
                tmin=0.0

            try:
                ev_after = [ev for ev in events if ev[0] > tidx][0]
                tmax = (ev_after[0] - raw.first_samp - 20) / raw.info['sfreq']
            except:
                tmax=None

            data.append(raw.copy().crop(tmin,tmax)._data)

        subject_raw = mne.io.RawArray(
            np.concatenate(data, axis=1),
            raw.info,
            first_samp=0)

        subjects_raw.append(subject_raw)

    return create_experiment(experiment_folder, experiment_name, subjects_raw, overwrite=overwrite)


# allow creating experiment from the command line
if __name__ == '__main__':
    type_, experiment_folder, experiment_name = sys.argv[1:]

    if type_ == 'evoked_conditions':
        create_evoked_conditions_experiment(experiment_folder, experiment_name)

