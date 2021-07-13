import os
import shutil
import tempfile
import mne

from meggie.mainwindow.preferences import PreferencesHandler

from meggie.experiment import initialize_new_experiment
from meggie.experiment import open_existing_experiment

def test_experiment_and_subject():
    with tempfile.TemporaryDirectory() as dirpath:
        sample_folder = mne.datasets.sample.data_path()
        sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

        # Create preferences object to store working directory
        # Also set prefs_path inside tempdir
        prefs = PreferencesHandler()
        prefs.workspace = dirpath
        prefs.prefs_path = os.path.join(dirpath, '.meggieprefs')

        # create experiment (creates experiment directory inside working directory,
        # also saves prefs (previous_experiment is set) and saves .exp file)
        name = 'Test experiment äö€ê*ë'
        author = 'Author'
        experiment = initialize_new_experiment(name, author, prefs)

        # add two subjects based on sample_audvis_raw
        # (makes copy of the file and adds it into subject directory inside experiment directory,
        # also creates and adds subject objects to the experiment object)
        experiment.create_subject('subject_1', sample_fname)
        experiment.create_subject('subject_2', sample_fname)

        # save experiment
        experiment.save_experiment_settings()

        loaded_experiment = open_existing_experiment(prefs, 
            path=experiment.path)

        assert(experiment.name == loaded_experiment.name)
        assert(set(experiment.subjects.keys()) == set(loaded_experiment.subjects.keys()))
        assert(experiment.subjects['subject_1'].name == loaded_experiment.subjects['subject_1'].name)

