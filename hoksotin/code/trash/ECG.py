'''
Created on Feb 27, 2013

@author: jaeilepp
'''
import mne
import pylab as pl
import numpy as np

fname = '/home/jaeilepp/Downloads/MNE-sample-data/MEG/sample/sample_audvis_raw.fif'
raw = mne.fiff.Raw(fname)

event_id = 999
ecg_events, _, _ = mne.preprocessing.find_ecg_events(raw, event_id, 'MEG 0131')
picks = mne.fiff.pick_types(raw.info, meg=False, eeg=False, stim=False, eog=False, include=['MEG 0131'])
tmin, tmax = -0.1, 0.1
epochs = mne.Epochs(raw, ecg_events, event_id, tmin, tmax, picks=picks, proj=False)
data = epochs.get_data()
pl.plot(1e3 * epochs.times, np.squeeze(data).T)
pl.xlabel('Times (ms)')
pl.ylabel('ECG')
pl.show()