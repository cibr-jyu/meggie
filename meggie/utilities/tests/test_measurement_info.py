import os 

import mne
import numpy as np

from meggie.utilities.measurement_info import MeasurementInfo


def test_measurement_info():
    sample_folder = mne.datasets.sample.data_path()
    sample_fname = os.path.join(sample_folder, 'MEG', 'sample', 'sample_audvis_raw.fif')
    raw = mne.io.read_raw_fif(sample_fname, preload=True)

    meas_info = MeasurementInfo(raw)

    assert(meas_info.high_pass == 0.1)
    assert(meas_info.low_pass == 172.18)
    assert(meas_info.sampling_freq == 600.61)
    assert(meas_info.date == '2002-12-03')
    assert(meas_info.subject_name == '')

