import os
import tempfile

import mne
import matplotlib.pyplot as plt

from meggie.datatypes.evoked.evoked import Evoked

from meggie.utilities.stats import prepare_data_for_permutation
from meggie.utilities.stats import permutation_analysis
from meggie.utilities.generate_experiments import create_evoked_conditions_experiment


def test_permutation_analysis():
    """
    """
    with tempfile.TemporaryDirectory() as dirpath:
        # generate dataset with generate_datasets to tmp folder (n=10)
        experiment = create_evoked_conditions_experiment(
            dirpath, 'permutation_test_experiment', n_subjects=10)

        for subject_name, subject in experiment.subjects.items():
            raw = subject.get_raw()

            raw.resample(100)
            subject.save()

            events = mne.find_events(raw)
            evoked_la = mne.Epochs(raw, events, event_id=1).average()
            evoked_ra = mne.Epochs(raw, events, event_id=2).average()
            content = {'la': evoked_la, 'ra': evoked_ra}
            meggie_evoked = Evoked('Evoked', subject.evoked_directory, {}, content=content)
            subject.add(meggie_evoked, 'evoked')

        experiment.activate_subject(subject_name)

        design = 'within-subjects'
        conditions = ['la', 'ra']
        groups = {'1': list(experiment.subjects.keys())}
        location_limits = ('ch_type', 'grad')
        time_limits = None
        threshold = 0.01
        n_permutations = 1000
        info, data, adjacency = prepare_data_for_permutation(
            experiment=experiment, 
            design=design, 
            groups=groups,
            item_type='evoked', 
            item_name='Evoked',
            location_limits=location_limits,
            time_limits=time_limits,
            frequency_limits=None,
            data_format=('locations', 'times'),
            no_threading=True)

        results = permutation_analysis(
            data=data, 
            design=design, 
            conditions=conditions, 
            groups=groups, 
            threshold=threshold, 
            adjacency=adjacency, 
            n_permutations=n_permutations,
            no_threading=True,
            random_state=10)

        # Correct cluster shape
        assert(results['1'][0].shape == (71, 202))


