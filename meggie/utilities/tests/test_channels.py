import os

import mne
import matplotlib.pyplot as plt

from meggie.utilities.channels import get_triplet_from_mag
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.channels import get_default_channel_groups
from meggie.utilities.channels import clean_names
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import average_to_channel_groups


def test_get_triplet_from_mag():
    assert(get_triplet_from_mag('MEG2031') == ['MEG2031', 'MEG2032', 'MEG2033'])


def test_get_channels_by_type():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')
    info = mne.io.read_raw_fif(sample_fname).info

    chs = get_channels_by_type(info)
    assert(set(chs.keys()) == set(['grad', 'mag', 'eeg']))
    assert(len(chs['eeg']) == 59)
    assert(len(chs['grad']) == 203)
    assert(len(chs['mag']) == 102)


def test_default_channel_groups():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

    raw = mne.io.read_raw_fif(sample_fname)

    assert(get_default_channel_groups(raw, 'eeg')['Left-frontal'] ==
           ['EEG 001', 'EEG 004', 'EEG 005', 'EEG 009', 'EEG 010', 'EEG 011', 'EEG 012'])


def test_clean_names():
    assert(clean_names(['EEG 012']) == clean_names(['EEG012']) == ['EEG012'])


def test_iterate_topography():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')
    info = mne.io.read_raw_fif(sample_fname).info

    fig = plt.figure()

    ch_names = info['ch_names'][::2]

    def on_pick(ax, info_idx, names_idx):
        pass

    iterated = []
    for ax, info_idx, names_idx in iterate_topography(fig, info, ch_names, on_pick):
        iterated.append((info_idx, names_idx))

    assert(iterated[0] == (0,0))
    assert(iterated[-1] == (304, 152))


def test_average_to_channel_groups():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')

    raw = mne.io.read_raw_fif(sample_fname, preload=True)
    info = raw.info
    data = raw._data

    ch_names = info['ch_names'][:20]

    meg_channel_groups = get_default_channel_groups(raw, 'meg')
    eeg_channel_groups = get_default_channel_groups(raw, 'eeg')

    # find out to which channel group each of the channels belongs to
    results = []
    for ch_name in ch_names:
        for ch_group_name, ch_group in meg_channel_groups.items():
            if ch_name in ch_group:
                results.append((ch_name, ch_group_name))

    labels, averaged_data = average_to_channel_groups(raw._data[:, 0:100], info, 
        ch_names, {'meg': meg_channel_groups, 'eeg': eeg_channel_groups})

    # check that the localization of data is same before and after averaging
    assert(set([result[1] for result in results]) == set([label[1] for label in labels]))

