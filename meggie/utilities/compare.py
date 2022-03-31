"""Contains functions to compare two raws."""

from copy import deepcopy

import mne
import numpy as np


def _prepare_raw_for_changes(raw_from, raw_to):
    """ Creates a new raw with channels interleaved from the two input raws

    """
    raw_to = raw_to.copy()
    raw_from = raw_from.copy()

    raw_to.drop_channels(raw_to.info['bads'])
    raw_from.drop_channels(raw_from.info['bads'])

    ch_names = []
    ch_types = []
    for ch_idx, ch_name in enumerate(raw_from.info['ch_names']):
        ch_type = mne.io.pick.channel_type(raw_from.info, ch_idx)
        ch_names.append(ch_name.strip())
        ch_types.append(ch_type)
        ch_names.append(ch_name.strip() + '*')
        ch_types.append(ch_type)

    new_info = mne.create_info(ch_names, 
                               raw_from.info['sfreq'], 
                               ch_types=ch_types)

    new_info['bads'] = [name for idx, name in enumerate(new_info['ch_names'])
                        if idx % 2 == 0]

    new_data = np.zeros((raw_from._data.shape[0] * 2, raw_from._data.shape[1]))
    new_data[0::2, :] = raw_from._data
    new_data[1::2, :] = raw_to._data

    new_raw = mne.io.RawArray(new_data, 
                              new_info, 
                              first_samp=raw_from.first_samp)

    return new_raw

def compare_raws(raw_from, raw_to):
    """Creates and plots a new raw object with channels from two raws
    interleaved. Can be used to analyse how some action changes
    the raw data.

    Parameters
    ----------
    raw_from : mne.io.Raw
        The original raw.
    raw_to : mne.io.Raw
        The changed raw.

    """
    changes_raw = _prepare_raw_for_changes(raw_from, raw_to)
    changes_raw.plot(color='red', bad_color='blue', title='Comparison plot')
