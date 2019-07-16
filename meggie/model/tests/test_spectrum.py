import os.path as op

from numpy.testing import assert_array_equal

import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.code_meggie.structures.spectrum import Spectrum
from meggie.code_meggie.analysis.spectral import group_average_psd

from meggie.code_meggie.tests.mock import get_experiment


data_dir = op.join(op.dirname(__file__), '..', '..', 'data')


def _get_example_spectrum(subject):
    """ Creates and returns meggie spectrum object with mock data """
    raw_fname = op.join(data_dir, 'sample_audvis_raw.fif')
    info = mne.read_raw_fif(raw_fname).info

    name = 'test_spectrum'
    ch_names = [ch_name for ch_name in info['ch_names']
                if ch_name.startswith('MEG')]
    log_transformed = False
    freqs = np.array([4, 5])
    data = {'condition_1': np.random.rand(len(ch_names), len(freqs)),
            'condition_2': np.random.rand(len(ch_names), len(freqs))}

    spectrum = Spectrum(name, subject, log_transformed, data, freqs, ch_names)

    subject.spectrums[name] = spectrum

    return spectrum


def test_group_average_psd():
    """ Tests trivial case of only one subject for psd group average
    """
    experiment = get_experiment()
    subject = experiment.active_subject

    spectrum = _get_example_spectrum(subject)

    groups = {'test_group': [subject.subject_name]}

    group_average_psd(experiment, 'test_spectrum', groups)
    group_average = experiment.active_subject.spectrums.get('group_test_spectrum')

    # check if data in corresponding keys is equal
    for spectrum_key in spectrum.data.keys():
        for group_average_key in group_average.data.keys():
            if group_average_key.startswith(spectrum_key):
                assert_array_equal(group_average.data[group_average_key], 
                                   spectrum.data[spectrum_key])
                break
