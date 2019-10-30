# coding: utf-8

"""
"""

import copy
import logging

import numpy as np
import mne

from meggie.utilities.units import get_scaling
from meggie.utilities.events import find_stim_channel

from meggie.datatypes.epochs.epochs import Epochs
from meggie.utilities.events import Events


def create_epochs_from_events(params, subject):
    """ Epochs are created in a way that one collection consists of such
    things that belong together. We wanted multiple collections because
    mne epochs did not allow multiple id's for one event name.
    """
    raw = subject.get_raw()

    params = copy.deepcopy(params)
    event_params = params['events']
    reject_params = params['reject']

    # convert data from human readable units to standard units
    for key in reject_params:
        reject_params[key] /= get_scaling(key)

    events = []
    category = {}

    stim_channel = find_stim_channel(raw)

    # event_id should not matter after epochs are created,
    # so we just add placeholders as 1, 2, 3...
    if len(event_params) > 0:
        for idx, item in enumerate(event_params):
            event_id = item['event_id']
            mask = item['mask']
            category_id = (
                'id_' + str(event_id) + '_mask_' + str(mask))

            new_events = Events(raw, stim_channel, mask, 
                                event_id).events

            if len(new_events) == 0:
                logging.warning('No events found with setting ' + 
                                str(category_id))

            category[category_id] = idx + 1
            new_events[:, 2] = idx + 1
            events.extend([event for event in new_events])

    if len(events) == 0:
        raise ValueError(
            'No events found.')

    # prepare parameters for pick_types
    if params['mag'] and params['grad']:
        meg = True
    elif params['mag']:
        meg = 'mag'
    elif params['grad']:
        meg = 'grad'
    else:
        meg = False

    eeg = params['eeg']

    # find all proper picks, dont exclude bads
    picks = mne.pick_types(raw.info, meg=meg, eeg=eeg, exclude=[])

    if len(picks) == 0:
        raise ValueError('You should select channel types to go on with')

    mne_epochs = mne.Epochs(raw, np.array(events),
                            category, params['tmin'], params['tmax'],
                            baseline=(params['bstart'], params['bend']),
                            picks=picks, reject=reject_params)

    if len(mne_epochs.get_data()) == 0:
        raise ValueError('Could not find any data. Perhaps the ' +
                         'rejection thresholds are too strict...')

    epochs_directory = subject.epochs_directory
    epochs = Epochs(params['collection_name'],
                    epochs_directory, 
                    params,
                    content=mne_epochs)

    epochs.save_content()
    subject.add(epochs, 'epochs')

