""" Contains controlling logic for the epochs creation.
"""

import copy
import logging

import numpy as np
import mne

from meggie.utilities.units import get_scaling
from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events

from meggie.datatypes.epochs.epochs import Epochs


def create_epochs_from_events(subject, params):
    """ Creates epochs based on events.
    """
    raw = subject.get_raw()

    params = copy.deepcopy(params)
    event_params = params['events']
    reject_params = params['reject']

    # convert reject params from human readable units to standard units
    for key in reject_params:
        reject_params[key] /= get_scaling(key)

    # remove params that don't match with the channel types present in raw
    if mne.pick_types(raw.info, meg='grad', eeg=False).size == 0:
        reject_params.pop('grad', None)
    if mne.pick_types(raw.info, meg='mag', eeg=False).size == 0:
        reject_params.pop('mag', None)
    if mne.pick_types(raw.info, meg=False, eeg=True).size == 0:
        reject_params.pop('eeg', None)

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

            new_events = find_events(raw, stim_channel, mask, event_id)

            if len(new_events) == 0:
                logging.warning('No events found with setting ' +
                                str(category_id))
                continue

            category[category_id] = idx + 1
            new_events[:, 2] = idx + 1

            events.extend([[event[0] + int(round(raw.info['sfreq']*params['delay'])), 
                            event[1], event[2]] 
                           for event in new_events])

    if len(events) == 0:
        raise ValueError(
            'No matching events found. Please check rejection limits and other parameters.')

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
        raise ValueError('You should select at least one channel type')

    mne_epochs = mne.Epochs(raw, np.array(events),
                            category, params['tmin'], params['tmax'],
                            baseline=(params['bstart'], params['bend']),
                            picks=picks, reject=reject_params)

    if len(mne_epochs.get_data()) == 0:
        raise ValueError('Could not find any data. Perhaps the ' +
                         'rejection thresholds are too strict...')

    n_dropped = len(events) - len(mne_epochs.get_data())

    if n_dropped > 0:
        logging.getLogger('ui_logger').info(str(n_dropped) + ' epochs dropped.')

    epochs_directory = subject.epochs_directory
    epochs = Epochs(params['collection_name'],
                    epochs_directory,
                    params,
                    content=mne_epochs)

    epochs.save_content()
    subject.add(epochs, 'epochs')

