'''
Created on Feb 28, 2013

@author: jaeilepp
'''
"""
def eventlist(events, eog_events):
    array = []
    for i in range(len(events)):
        for j in range(len(eog_events)):
            if (events[i][0] - 200) <= eog_events[j][0] and (events[i][0] + 500) >= eog_events[j][0]:
                break
            elif events[i][0] + 500 < eog_events[j][0]:
                array.append(events[i])
                break
    return np.vstack(array)
"""
import mne
import pylab as pl
import numpy as np


def drawEOGEpochs(tminInput, tmaxInput, eventStimChannel):
    fname = '../../koodikikkailua/sample_audvis_raw.fif'
    
    tmin = tminInput
    tmax = tmaxInput
    
    #TODO check if tmin and tmax are sane
    if (tmin<-5 or tmax>10):
        tmin, tmax = -0.2, 0.5
    
    raw = mne.fiff.Raw(fname)
    
    # Alunperin stimchannelina 'STI 001'
    # TODO: stimchannel valittava listasta
    events = mne.find_events(raw, stim_channel=[eventStimChannel])
    
    
    
    event_id = 998
    #eog_events = mne.preprocessing.find_eog_events(raw, event_id)
    """print events
    print '---------------------------------------------------------------------------------------------------------------------------------------------'
    print eog_events"""
    
    picks = mne.fiff.pick_types(raw.info, meg=True, eeg=False, stim=False, eog=False, exclude=raw.info['bads'])
    
    #start, stop = raw.time_as_index([0, 15])
    #_, times = raw[picks, start:(stop + 1)]
    
    
    #el = eventlist(events, eog_events)
    #print len(events)
    #epochs = mne.Epochs(raw, events, event_id, tmin, tmax, picks=picks)
    #reject = dict(grad=4000e-13, mag=4e-12, eog=150e-6)
    baseline = (None, 0)
    epochs = mne.Epochs(raw, events, 5, tmin, tmax, proj=True, picks=picks, baseline=baseline, preload=False)
    #epochs.drop_bad_epochs()
    #list = mne.compute_proj_epochs(epochs)
    #print list
    
    evoked = epochs.average()
    evoked.plot()
    #print '-------------------------------------------------------------------------------------'
    pl.subplot(999)
    #data = epochs.get_data()
    #times = epochs.times
    #print data.T[200]
    #pl.plot(times, np.squeeze(data.T))
    #pl.show()
    #./mne_compute_proj_eog.py -i /home/jaeilepp/Downloads/MNE-sample-data/MEG/sample/sample_audvis_raw.fif --l-freq 1 --h-freq 35 --rej-grad 3000 --rej-mag 4000 --rej-eeg 100 --proj /home/jaeilepp/Downloads/MNE-sample-data/MEG/sample/sample_audvis_eog_proj.fif
    
