import mne
import pylab as pl

fname = '/home/jaeilepp/Downloads/MNE-sample-data/MEG/sample/sample_audvis_raw.fif'
raw = mne.fiff.Raw(fname, False, True)
picks = mne.fiff.pick_types(raw.info, meg=True, eeg=True, eog=True)
event_id, tmin, tmax = 1, -0.2, 0.5
start, stop = raw.time_as_index([0,15])
data, times = raw[picks[:5], start:(stop+1)]
events = mne.find_events(raw, stim_channel='STI 014')
epochs = mne.Epochs(raw, events, event_id, tmin, tmax, proj=True, picks=picks, preload=True,)
evoked = epochs.average()
evoked.plot()
"""
pl.plot(times, data.T)
pl.xlabel('time (s)')
pl.ylabel('MEG data (T)')
pl.show()
"""
#picks = mne.fiff.pick_types(evoked.info, meg='mag')
#evoked.plot(picks=picks)
"""
evoked = mne.fiff.Evoked('/home/jaeilepp/Downloads/MNE-sample-data/MEG/sample/sample_audvis-ave.fif', setno=2)

evoked.plot()
"""