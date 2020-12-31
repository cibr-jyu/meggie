import os 

import mne
import numpy as np

from meggie.utilities.events import find_events
from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import update_stim_channel


def test_find_events():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')
    raw = mne.io.read_raw_fif(sample_fname, preload=True)

    id_ = 1
    mask = 32 + 16 + 8 + 4 + 2 + 1
    events_all_with_mask = find_events(raw, mask=mask, id_=1)

    events_all = find_events(raw)

    events_1 = find_events(raw, id_=1)

    assert(len(events_all_with_mask) == len(events_all) == 320)
    assert(len(events_1) == 72)
    assert(np.array_equal(events_1[:, 2], [1]*len(events_1)))


def test_find_stim_channel():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')
    raw = mne.io.read_raw_fif(sample_fname, preload=True)

    stim_channel = find_stim_channel(raw)
    assert(stim_channel == 'STI 014')


def test_update_stim_channel():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')
    raw = mne.io.read_raw_fif(sample_fname, preload=True)

    events_before = find_events(raw)

    update_stim_channel(raw, [[100, 0, 1]])

    events_after = find_events(raw)

    assert(len(events_after) == len(events_before) + 1)

