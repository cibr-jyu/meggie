# coding: utf-8
"""
"""

import os
import logging

import numpy as np
import mne


def get_default_channel_groups(info, ch_type):

    from mne.selection import _divide_to_regions

    if ch_type == 'meg':
        picks = mne.pick_types(info, meg=True, eeg=False)
    else:
        picks = mne.pick_types(info, meg=False, eeg=True)

    ch_names = [ch_name for idx, ch_name in enumerate(info['ch_names'])
                if idx in picks]

    if not ch_names:
        return {}

    info_filt = info.copy().pick_channels(ch_names)

    # check if there is no montage set..
    ch_norms = []
    for ch in info_filt['chs']:
        ch_norms.append(np.linalg.norm(ch['loc']))
    if np.all(np.isclose(ch_norms, ch_norms[0])):
        return {}

    regions = _divide_to_regions(info_filt, add_stim=False)

    ch_groups = {}
    for region_key, region in regions.items():
        region_ch_names = [info_filt['ch_names'][ch_idx] for ch_idx 
                           in region]
        ch_groups[region_key] = [info['ch_names'].index(ch_name) 
                                 for ch_name in region_ch_names]

    return ch_groups


def get_channels(info):
    channels = {}
    grads = mne.pick_types(info, meg='grad', eeg=False)
    if grads.size > 0:
        channels['grad'] = grads
    mags = mne.pick_types(info, meg='mag', eeg=False)
    if mags.size > 0:
        channels['mag'] = mags
    eegs = mne.pick_types(info, meg=False, eeg=True)
    if eegs.size > 0:
        channels['eeg'] = eegs
    return channels


def average_data_to_channel_groups(data, ch_names, channel_groups):
    """ averages data by ch groups and ch types
    """
    ch_types = ['grad', 'mag', 'eeg']

    averaged_data = []
    data_labels = []

    if channel_groups == 'MNE':
        for ch_type in ch_types:
            if ch_type in ['mag', 'grad']:
                selections = mne.selection._SELECTIONS
                for selection in selections:
                    selected_ch_names = mne.utils._clean_names(
                        mne.read_selection(selection),
                        remove_whitespace=True)

                    cleaned_ch_names = mne.utils._clean_names(ch_names,
                                                              remove_whitespace=True)

                    if ch_type == 'grad':
                        ch_names_filt = [ch_name for ch_name in selected_ch_names
                                         if not ch_name.endswith('1') and
                                         'MEG' in ch_name]
                        average_type = 'rms'
                    elif ch_type == 'mag':
                        ch_names_filt = [ch_name for ch_name in selected_ch_names
                                         if ch_name.endswith('1') and
                                         'MEG' in ch_name]
                        average_type = 'mean'

                    if not set(cleaned_ch_names).intersection(
                            set(ch_names_filt)):
                        continue

                    # calculate average
                    data_in_chs = [data[ch_idx] for ch_idx, ch_name
                                   in enumerate(cleaned_ch_names)
                                   if ch_name in ch_names_filt]
                    if average_type == 'mean':
                        ch_average = np.mean(data_in_chs, axis=0)
                    else:
                        ch_average = np.sqrt(
                            np.sum(np.array(data_in_chs)**2, axis=0))

                    averaged_data.append(ch_average)
                    data_labels.append((ch_type, selection))
            elif ch_type == 'eeg':
                cleaned_ch_names = mne.utils._clean_names(ch_names,
                                                          remove_whitespace=True)

                # without further knowledge, we average all channels for eeg
                eeg_ch_names = [ch_name for ch_name in cleaned_ch_names
                                if ch_name.startswith('E')]

                if not eeg_ch_names:
                    continue

                # calculate average
                ch_average = np.mean(
                    [data[ch_idx] for ch_idx, ch_name
                     in enumerate(cleaned_ch_names)
                     if ch_name in eeg_ch_names], axis=0)

                averaged_data.append(ch_average)
                data_labels.append((ch_type, 'All channels'))

        averaged_data = np.array(averaged_data)

        return data_labels, averaged_data
