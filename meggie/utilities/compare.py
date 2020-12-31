import logging
from copy import deepcopy

import numpy as np


def _prepare_raw_for_changes(raw_from, raw_to):
    """ Modifies first raw object in place so that the second raw object is
    interleaved to first one
    """
    raw_to = raw_to.copy()
    raw_from = raw_from.copy()

    raw_to.drop_channels(raw_to.info['bads'])
    raw_from.drop_channels(raw_from.info['bads'])

    new_info = raw_from.info.copy()
    new_info['nchan'] = 2 * raw_from.info['nchan']

    ch_names = []
    for ch_name in raw_from.info['ch_names']:
        ch_names.append(ch_name + ' (old)')
        ch_names.append(ch_name + ' (new)')
    new_info['ch_names'] = ch_names

    chs = []
    for idx, ch in enumerate(raw_from.info['chs']):
        ch_1 = deepcopy(ch)
        ch_1['ch_name'] = new_info['ch_names'][idx * 2]
        chs.append(ch_1)

        ch_2 = deepcopy(ch)
        ch_2['ch_name'] = new_info['ch_names'][idx * 2 + 1]
        chs.append(ch_2)
    new_info['chs'] = chs

    new_info['bads'] = [name for idx, name in enumerate(new_info['ch_names'])
                        if idx % 2 == 0]

    raw_to.info = new_info

    raw_from_data = raw_from._data
    raw_to_data = raw_to._data

    data = np.zeros((raw_from_data.shape[0] * 2, raw_from_data.shape[1]))
    data[0::2, :] = raw_from_data
    data[1::2, :] = raw_to_data

    raw_to._data = data

    return raw_to

def compare_raws(raw_from, raw_to):
    """ Creates and plots a new raw object with channels from two raws
    interleaved
    """
    changes_raw = _prepare_raw_for_changes(raw_from, raw_to)
    changes_raw.plot(color='red', bad_color='blue')
