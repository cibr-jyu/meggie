"""
"""

import os
import logging

import matplotlib.pyplot as plt
import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.utils.units import get_scaling

from meggie.ui.utils.decorators import threaded


def read_projections(fname):
    """
    """
    projs = mne.read_proj(fname)
    return projs


def preview_projections(raw, projs):
    """
    """
    raw = raw.copy()
    raw.apply_proj()
    raw.info['projs'] = []

    raw.add_proj(projs)
    raw.plot()

def plot_projs_topomap(experiment, raw):
    fig = raw.plot_projs_topomap()
    name = experiment.active_subject.subject_name
    fig.canvas.set_window_title('Projections for ' + name)

@threaded
def apply_exg(kind, experiment, raw, directory, projs):
    """
    Applies ECG or EOG projections for MEG-data.
    Keyword arguments:
    kind          -- String to indicate type of projectors ('eog, or 'ecg')
    raw           -- Data to apply to
    directory     -- Directory of the projection file
    projs         -- List of projectors.

    Performed in a worker thread.
    """

    fname = os.path.join(directory, experiment.active_subject.working_file_name)

    for new_proj in projs:  # first remove projs
        for idx, proj in enumerate(raw.info['projs']):
            if str(new_proj) == str(proj):
                raw.info['projs'].pop(idx)
                break

    raw.add_proj(projs)

    if kind == 'eeg':
        projs = raw.info['projs']
        for idx, proj in enumerate(projs):
            names = ['ECG', 'EOG', 'EEG']
            if [name for name in names if name in proj['desc']]:
                continue
            raw.info['projs'][idx]['desc'] = 'Ocular-' + proj['desc']

    fileManager.save_raw(experiment, raw, fname, overwrite=True)

    return True


def call_ecg_ssp(dic, subject, update_ui=(lambda: None)):
    """
    Creates ECG projections using SSP for given data.
    Keyword arguments:
    dic           -- dictionary of parameters including the MEG-data.
    subject       -- The subject to perform the action on.
    """
    _call_ecg_ssp(dic, subject, do_meanwhile=update_ui)


@threaded
def _call_ecg_ssp(dic, subject):
    """Performed in a worker thread."""
    raw_in = subject.get_working_file()
    tmin = dic.get('tmin')
    tmax = dic.get('tmax')
    ecg_low_freq = dic.get('ecg-l-freq')
    ecg_high_freq = dic.get('ecg-h-freq')
    grad = dic.get('n-grad')
    mag = dic.get('n-mag')
    eeg = dic.get('n-eeg')
    filter_low = dic.get('l-freq')
    filter_high = dic.get('h-freq')

    rej_grad = dic.get('rej-grad')
    rej_mag = dic.get('rej-mag')
    rej_eeg = dic.get('rej-eeg')
    rej_eog = dic.get('rej-eog')

    reject = {
        'grad': float(rej_grad) / get_scaling('grad'), 
        'mag': float(rej_mag) / get_scaling('mag'),
        'eeg': float(rej_eeg) / get_scaling('eeg'), 
        'eog': float(rej_eog) / get_scaling('eog'),
    }

    qrs_threshold = dic.get('qrs')
    start = dic.get('tstart')
    taps = dic.get('filtersize')
    excl_ssp = dic.get('no-proj')
    comp_ssp = dic.get('average')
    ch_name = dic.get('ch_name')

    prefix = os.path.join(subject.subject_path, subject.subject_name)

    ecg_event_fname = prefix + '_ecg-eve.fif'

    if comp_ssp:
        ecg_proj_fname = prefix + '_ecg_avg_proj.fif'
    else:
        ecg_proj_fname = prefix + '_ecg_proj.fif'

    # To avoid casualities
    n_jobs = 1
    projs, events = mne.compute_proj_ecg(raw=raw_in, tmin=tmin, tmax=tmax,
        n_grad=grad, n_mag=mag, n_eeg=eeg, l_freq=filter_low, 
        h_freq=filter_high, average=comp_ssp, filter_length=taps, 
        n_jobs=n_jobs, ch_name=ch_name, reject=reject,
        no_proj=excl_ssp, ecg_l_freq=ecg_low_freq,
        ecg_h_freq=ecg_high_freq, tstart=start, qrs_threshold=qrs_threshold)

    if not projs:
        raise Exception('No ECG events found. Change settings.')

    message = "Writing ECG projections in %s" % ecg_proj_fname
    logging.getLogger('ui_logger').info(message)
    mne.write_proj(ecg_proj_fname, projs)

    message = "Writing ECG events in %s" % ecg_event_fname
    logging.getLogger('ui_logger').info(message)
    mne.write_events(ecg_event_fname, events)

def plot_ecg_events(experiment, params):
    raw = experiment.active_subject.get_working_file()
    
    events, _, _ = mne.find_ecg_events(raw,
        ch_name=params['ch_name'], event_id=1, l_freq=params['ecg-l-freq'],
        h_freq=params['ecg-h-freq'], tstart=params['tstart'],
        qrs_threshold=params['qrs'], filter_length=params['filtersize'])
    
    picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False,
        eog=False, include=[params['ch_name']])
    epochs = mne.Epochs(raw, events=events, event_id=1,
        tmin=params['tmin'], tmax=params['tmax'], picks=picks, proj=False)
    
    data = epochs.get_data()
    message = "Number of detected ECG artifacts : %d" % len(data)
    logging.getLogger('ui_logger').info(message)
    
    plt.plot(1e3 * epochs.times, np.squeeze(data).T)
    plt.xlabel('Times (ms)')
    plt.ylabel('ECG')
    subject_name = experiment.active_subject.subject_name
    plt.gcf().canvas.set_window_title('_'.join(['ECG_events', subject_name,
                                                params['ch_name']]))
    plt.show()

def call_eog_ssp(dic, subject, update_ui=(lambda: None)):
    """
    Creates EOG projections using SSP for given data.
    Keyword arguments:
    dic           -- dictionary of parameters including the MEG-data.
    subject       -- The subject to perform action on.
    """
    _call_eog_ssp(dic, subject, do_meanwhile=update_ui)

@threaded
def _call_eog_ssp(dic, subject):
    """Performed in a worker thread."""
    raw_in = subject.get_working_file()
    tmin = dic.get('tmin')
    tmax = dic.get('tmax')
    eog_low_freq = dic.get('eog-l-freq')
    eog_high_freq = dic.get('eog-h-freq')
    grad = dic.get('n-grad')
    mag = dic.get('n-mag')
    eeg = dic.get('n-eeg')
    filter_low = dic.get('l-freq')
    filter_high = dic.get('h-freq')

    rej_grad = dic.get('rej-grad')
    rej_mag = dic.get('rej-mag')
    rej_eeg = dic.get('rej-eeg')
    rej_eog = dic.get('rej-eog')

    start = dic.get('tstart')
    taps = dic.get('filtersize')
    excl_ssp = dic.get('no-proj')
    comp_ssp = dic.get('average')
    reject = {
        'grad': float(rej_grad) / get_scaling('grad'), 
        'mag': float(rej_mag) / get_scaling('mag'),
        'eeg': float(rej_eeg) / get_scaling('eeg'), 
        'eog': float(rej_eog) / get_scaling('eog'),
    }

    prefix = os.path.join(subject.subject_path, subject.subject_name) 
    eog_event_fname = prefix + '_eog-eve.fif'

    if comp_ssp:
        eog_proj_fname = prefix + '_eog_avg_proj.fif'
    else:
        eog_proj_fname = prefix + '_eog_proj.fif'

    # To avoid casualities
    n_jobs = 1        
    projs, events = mne.compute_proj_eog(raw=raw_in, tmin=tmin, tmax=tmax,
        n_grad=grad, n_mag=mag, n_eeg=eeg, l_freq=filter_low, 
        h_freq=filter_high, average=comp_ssp, filter_length=taps, 
        n_jobs=n_jobs, reject=reject, no_proj=excl_ssp, 
        eog_l_freq=eog_low_freq, eog_h_freq=eog_high_freq, tstart=start)

    message = "Writing EOG projections in %s" % eog_proj_fname
    logging.getLogger('ui_logger').info(message)
    mne.write_proj( eog_proj_fname, projs)

    message = "Writing EOG events in %s" % eog_event_fname
    logging.getLogger('ui_logger').info(message)
    mne.write_events(eog_event_fname, events)

def plot_eog_events(experiment, params):
    raw = experiment.active_subject.get_working_file()
    
    picks = mne.pick_types(raw.info, meg=False, eeg=False, stim=False,
                           eog=True)

    try:
        ch_name = [ch_name for idx, ch_name 
                   in enumerate(raw.info['ch_names']) if idx in picks][0]
    except IndexError:
        raise Exception("No EOG channel found")

    events = mne.find_eog_events(raw, event_id=1, 
        l_freq=params['eog-l-freq'], h_freq=params['eog-h-freq'], 
        filter_length=params['filtersize'], ch_name=ch_name, 
        tstart=params['tstart'])

    epochs = mne.Epochs(raw, events=events, event_id=1,
        tmin=params['tmin'], tmax=params['tmax'], picks=picks, proj=False)
    
    data = epochs.get_data()

    message = "Number of detected EOG artifacts : %d" % len(data)
    logging.getLogger('ui_logger').info(message)
    
    plt.plot(1e3 * epochs.times, np.squeeze(data).T)
    plt.xlabel('Times (ms)')
    plt.ylabel('EOG')
    subject_name = experiment.active_subject.subject_name
    plt.gcf().canvas.set_window_title('EOG_events_' + subject_name)
    plt.show()


def call_eeg_ssp(dic, subject, update_ui=(lambda: None)):
    """
    Creates EEG projections using SSP for given data.
    Keyword arguments:
    dic           -- dictionary of parameters including the MEG-data.
    subject       -- The subject to perform action on.
    """
    _call_eeg_ssp(dic, subject, do_meanwhile=update_ui)
    
@threaded
def _call_eeg_ssp(dic, subject):
    raw = subject.get_working_file()
    events = dic['events']
    tmin = dic['tmin']
    tmax = dic['tmax']
    n_eeg = dic['n_eeg']
    
    eog_epochs = mne.Epochs(raw, events, tmin=tmin, tmax=tmax)
    
    
    eog_evoked = eog_epochs.average()
    
    # Compute SSPs
    projs = mne.compute_proj_evoked(eog_evoked, n_eeg=n_eeg)

    prefix = os.path.join(subject.subject_path, subject.subject_name) 
    eeg_event_fname = prefix + '_eeg-eve.fif'
    eeg_proj_fname = prefix + '_eeg_proj.fif'
    
    message = "Writing ocular projections in %s" % eeg_proj_fname
    logging.getLogger('ui_logger').info(message) 
    mne.write_proj(eeg_proj_fname, projs)

    message = "Writing ocular events in %s" % eeg_event_fname
    logging.getLogger('ui_logger').info(message) 
    mne.write_events(eeg_event_fname, events)

def plot_average_epochs(experiment, events, tmin, tmax):
    """ Plot average eog epochs
    """
    raw = experiment.active_subject.get_working_file()
    logging.getLogger('ui_logger').info("Plotting averages...")
    eog_epochs = mne.Epochs(raw, events,
                    tmin=tmin, tmax=tmax)
    
    # Average EOG epochs
    eog_evoked = eog_epochs.average()
    fig = eog_evoked.plot()
    subject_name = experiment.active_subject.subject_name
    fig.canvas.set_window_title('avg_epochs_' + subject_name)

@threaded
def find_eog_events(experiment, params):
    raw = experiment.active_subject.get_working_file()
    eog_events = mne.find_eog_events(raw, l_freq=params['l_freq'], 
        h_freq=params['h_freq'], filter_length=params['filter_length'],
        ch_name=params['ch_name'], tstart=params['tstart'])
    return eog_events


