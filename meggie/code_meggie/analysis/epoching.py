# coding: utf-8
"""
"""

import re
import copy
import logging

from PyQt4 import QtGui

import numpy as np
import matplotlib.pyplot as plt

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.code_meggie.analysis.utils import color_cycle

from meggie.ui.utils.decorators import threaded
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.epoching.events import Events
from meggie.code_meggie.utils.units import get_scaling
from meggie.code_meggie.utils.units import get_unit


def create_epochs(experiment, params, subject):
    """ Epochs are created in a way that one collection consists of such 
    things that belong together. We wanted multiple collections because 
    MNE Epochs don't allow multiple id's for one event name, so doing 
    subselections for averaging and visualizing purposes from one collection
    is not feasible.
    """
    params_copy = copy.deepcopy(params)
    reject_data = params_copy['reject']

    # convert data from human readable units to standard units
    for key in ['grad', 'mag', 'eog', 'eeg']:
        if key in reject_data:
            reject_data[key] /= get_scaling(key)
    
    raw = subject.get_working_file()
         
    events = []
    event_params = params_copy['events']
    fixed_length_event_params = params_copy['fixed_length_events']
    category = {}

    # event_id should not matter after epochs are created.
    # counter is used so that no collisions would happen.
    event_id_counter = 0

    if len(event_params) > 0:
        for event_params_dic in event_params:
            event_id = event_params_dic['event_id']
            
            category_id = 'id_' + str(event_id)
            if event_params_dic['mask']:
                category_id += '_mask_' + str(event_params_dic['mask'])
            
            category[category_id] = event_id_counter + 1
            new_events = np.array(create_eventlist(
                experiment, event_params_dic, subject))

            if len(new_events) == 0:
                raise ValueError('No events found with selected id.')
            
            new_events[:, 2] = event_id_counter + 1
            events.extend([event for event in new_events])
            event_id_counter += 1
            

    if len(fixed_length_event_params) > 0:
        for idx, event_params_dic in enumerate(fixed_length_event_params):
            category['fixed_' + str(idx + 1)] = event_id_counter + 1
            event_params_dic['event_id'] = event_id_counter + 1
            events.extend(mne.make_fixed_length_events(raw, 
                event_params_dic['event_id'],
                event_params_dic['tmin'],
                event_params_dic['tmax'], 
                event_params_dic['interval']
            ))
            event_id_counter += 1

    if len(events) == 0:
        raise ValueError('Could not create epochs for subject: No events found with given params.')

    if not isinstance(raw, mne.RAW_TYPE):
        raise TypeError('Not a Raw object')

    if params_copy['mag'] and params_copy['grad']:
        params_copy['meg'] = True
    elif params_copy['mag']:
        params_copy['meg'] = 'mag'
    elif params_copy['grad']:
        params_copy['meg'] = 'grad'
    else:
        params_copy['meg'] = False
    
    # find all proper picks
    picks = mne.pick_types(raw.info, meg=params_copy['meg'],
        eeg=params_copy['eeg'], eog=params_copy['eog'])
    
    if len(picks) == 0:
        raise ValueError('Picks cannot be empty. Select picks by ' + 
                         'checking the checkboxes.')

    epochs = mne.Epochs(raw, np.array(events), 
        category, params_copy['tmin'], params_copy['tmax'], 
        picks=picks, reject=params_copy['reject'])
        
    if len(epochs.get_data()) == 0:
        raise ValueError('Could not find any data. Perhaps the ' + 
                         'rejection thresholds are too strict...')
    
    epochs_object = Epochs(params['collection_name'], subject, params, epochs)
    fileManager.save_epoch(epochs_object, overwrite=True)
    subject.add_epochs(epochs_object)
    
    events = epochs.event_id
    events_str = ''
    for event_name, event_id in events.items():
        events_str += event_name + ' [' + str(len(epochs[event_name])) + ' events found]\n'
    
    return subject.subject_name + ', ' + params['collection_name'] + ':\n' + events_str

def create_eventlist(experiment, params, subject):
    """
    Pick desired events from the raw data.
    """
    stim_channel = subject.find_stim_channel()
    raw = subject.get_working_file()
    e = Events(experiment, raw, stim_channel, params['mask'], params['event_id'])

    return e.events


def draw_evoked_potentials(experiment, evokeds, title=None):
    """
    Draws a topography representation of the evoked potentials.

    """
    layout = fileManager.read_layout(experiment.layout)
    colors = color_cycle(len(evokeds))

    fig = mne.plot_evoked_topo(evokeds, layout,
        color=colors, title=title, fig_facecolor='w', axis_facecolor='w',
        font_color='k')

    conditions = [e.comment for e in evokeds]
    positions = np.arange(0.025, 0.025 + 0.04 * len(evokeds), 0.04)
            
    for cond, col, pos in zip(conditions, colors, positions):
        plt.figtext(0.775, pos, cond, color=col, fontsize=12)
        
    window_title = '_'.join(conditions)
    fig.canvas.set_window_title(window_title)
    fig.show()
    
    def onclick(event):
        channel = plt.getp(plt.gca(), 'title')
        plt.gcf().canvas.set_window_title('_'.join([window_title, channel]))
        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)

def average_channels(experiment, instance, lobeName, channelSet=[], 
                     update_ui=(lambda: None)):
    """
    """
    
    if channelSet:
        channels = channelSet
        title = 'selected set of channels'
    else:
        channels = mne.read_selection(lobeName)
        title = lobeName
        
    message = "Calculating channel averages for " + title
    logging.getLogger('ui_logger').info(message)

    dataList, epochs_name = _average_channels(experiment,
        instance, channels, do_meanwhile=update_ui)

    # Plotting:
    plt.clf()
    fig = plt.figure()
    subject_name = experiment.active_subject.subject_name
    fig.canvas.set_window_title('_'.join([epochs_name, 
        'channel_avg', title]))
    fig.suptitle('Channel average for ' + title, y=1.0025)

    # Draw a separate plot for each event type
    for index, (times, eventName, data) in enumerate(dataList):
        ca = fig.add_subplot(len(dataList), 1, index + 1) 
        ca.set_title(eventName)

        if eventName.endswith('grad'):
            ch_type = 'grad'
        elif eventName.endswith('mag'):
            ch_type = 'mag'
        elif eventName.endswith('eeg'):
            ch_type = 'eeg'

        label = get_unit(ch_type)
        data *= get_scaling(ch_type)

        ca.plot(times, data)

        ca.set_xlabel('Time (s)')
        ca.set_ylabel(label)

    plt.tight_layout()
    fig.show()

@threaded
def _average_channels(experiment, instance, channelsToAve):
    """Performed in a worker thread."""

    if isinstance(instance, str):
        _epochs = experiment.active_subject.epochs.get(instance)
        epochs = _epochs.raw
        epochs_name = _epochs.collection_name
        if epochs is None:
            raise Exception('No epochs found.')
        category = epochs.event_id

        # Creates evoked potentials from the given events (variable 'name' 
        # refers to different categories).
        evokeds = [epochs[name].average() for name in category.keys()]
    elif isinstance(instance, mne.EVOKED_TYPE):
        evokeds = [instance]
        epochs_name = evokeds[0].comment
    elif isinstance(instance, list) or isinstance(instance, np.ndarray):
        evokeds = instance
        epochs_name = 'List_of_epochs'

    # Channel names in Evoked objects may or may not have whitespaces
    # depending on the measurements settings,
    # need to check and adjust channelsToAve accordingly.
    
    channelNameString = evokeds[0].info['ch_names'][0]
    if re.match("^MEG[0-9]+", channelNameString):
        channelsToAve = mne._clean_names(channelsToAve, remove_whitespace=True)

    dataList = []

    for evoked in evokeds:
        evokedToAve = mne.pick_channels_evoked(evoked, list(channelsToAve))

        ch_names = evokedToAve.ch_names
        gradsIdxs = mne._pair_grad_sensors_from_ch_names(ch_names)

        magsIdxs = mne.pick_channels_regexp(ch_names, regexp='MEG.{3,4}1$')

        eegIdxs = mne.pick_types(evokedToAve.info, meg=False, eeg=True,
                                   ref_meg=False)

        # Merges the grad channel pairs in evokedToAve
        if len(gradsIdxs) > 0:
            gradData = mne._merge_grad_data(evokedToAve.data[gradsIdxs])

            # Averages the gradData
            averagedGradData = np.mean(gradData, axis=0)

            # Links the event name and the corresponding data
            dataList.append((
                evokedToAve.times, 
                evokedToAve.comment + '_grad',
                averagedGradData
            ))
        if len(magsIdxs) > 0:
            mag_data = evokedToAve.data[magsIdxs]
            averagedMagData = np.mean(mag_data, axis=0)
            dataList.append((
                evokedToAve.times,
                evokedToAve.comment + '_mag', 
                averagedMagData
            ))
        if len(eegIdxs) > 0:
            eeg_data = evokedToAve.data[eegIdxs]
            averagedEegData = np.mean(eeg_data, axis=0)
            dataList.append((
                evokedToAve.times,
                evokedToAve.comment + '_eeg', 
                averagedEegData
            ))

    return dataList, epochs_name

def group_average(experiment, evoked_name, update_ui=(lambda: None)):
    """
    """
    count = 0
    group_info = {}
    for subject in experiment.subjects.values():
        if subject.evokeds.get(evoked_name):
            count += 1
            evoked = subject.evokeds.get(evoked_name)
            group_info[subject.subject_name] = evoked.info

    if count == 0:
        raise ValueError('No evoked responses found from any subject.')
    
    if count > 0 and count < len(experiment.subjects):
        
        message = ("Evoked responses not found from every subject. " + 
                   "(" + str(count) + " responses found.)")
        logging.getLogger('ui_logger').warning(message)
    
    evokeds = _group_average(experiment,
       evoked_name, do_meanwhile=update_ui
    )

    return evokeds, group_info

@threaded
def _group_average(experiment, evoked_name):
    """Performed in a worker thread."""

    subjects = experiment.subjects.values()
    responses = [subject.evokeds.get(evoked_name) for subject in subjects]
    responses = filter(bool, responses)

    # assumme all have same same amount of evokeds
    evoked_groups = {}
    
    for response in responses:
        for key, value in response.mne_evokeds.items():
            if evoked_groups.get(key):
                evoked_groups[key].append(value)
            else:
                evoked_groups[key] = [value]

    grand_averages = {}

    for key, evokeds in evoked_groups.items():
        grand_averaged = mne.grand_average(evokeds)
        grand_averaged.comment = key
        grand_averages[key] = grand_averaged

    return grand_averages
