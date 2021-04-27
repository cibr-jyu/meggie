
# coding: utf-8
"""
"""

import os
import logging

import mne

import numpy as np
import scipy


def prepare_data_for_permutation(experiment, design, groups, conditions,
                                 item_type, item_name, 
                                 location_limits, time_limits, frequency_limits,
                                 data_format=('locations', 'freqs', 'times')):
    """
    """
    final_data = {}
    if design == 'between-subjects':
        for condition in conditions:
            cond_data = []
            for group in groups.values():
                group_data = []
                for subject_name in group:
                    subject = experiment.subjects[subject_name]
                    subject_item = getattr(subject, item_type).get(item_name)
                    if not subject_item:
                        message = "Skipping " + subject_name + " (no " + str(item_type) + ")"
                        logging.getLogger('ui_logger').warning(message) 

                    data = subject_item.content[condition]
                    if frequency_limits is not None:
                        # average over the selected frequency range
                        freqs = subject_item.freqs
                        fmin_idx = np.where(freqs >= frequency_limits[0])[0][0]
                        fmax_idx = np.where(freqs <= frequency_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('freqs'), 0)
                        averaged = np.mean(swapped[fmin_idx:fmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('freqs'), 0)
                    if location_limits is not None:
                        # take the seleted location
                        ch_names = subject_item.ch_names
                        ch_idx = ch_names.index(location_limits)
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idx][np.newaxis, :]
                        data = np.swapaxes(selected, data_format.index('locations'), 0)
                    if time_limits is not None:
                        # average over the selected temporal range
                        times = subject_item.times
                        tmin_idx = np.where(times >= time_limits[0])[0][0]
                        tmax_idx = np.where(times <= time_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('times'), 0)
                        averaged = np.mean(swapped[tmin_idx:tmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('times'), 0)

                    # move locations dim to last place
                    data = np.rollaxis(data, data_format.index('locations'), data.ndim)

                    group_data.append(data)
                cond_data.append(np.array(group_data))
            final_data[condition] = cond_data
        return final_data
    elif design == 'within-subjects':
        final_data = {}
        for group_key, group in groups.items():

            group_data = []
            for subject_idx, subject_name in enumerate(group):
                subject = experiment.subjects[subject_name]
                subject_item = getattr(subject, item_type).get(item_name)
                if not subject_item:
                    message = "Skipping " + subject_name + " (no " + str(item_type) + ")"
                    logging.getLogger('ui_logger').warning(message) 

                cond_data = []
                for condition_idx, condition in enumerate(conditions):
                    data = subject_item.content[condition]
                    if frequency_limits is not None:
                        # average over the selected frequency range
                        freqs = subject_item.freqs
                        fmin_idx = np.where(freqs >= frequency_limits[0])[0][0]
                        fmax_idx = np.where(freqs <= frequency_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('freqs'), 0)
                        averaged = np.mean(swapped[fmin_idx:fmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('freqs'), 0)
                    if location_limits is not None:
                        # take the seleted location
                        ch_names = subject_item.ch_names
                        ch_idx = ch_names.index(location_limits)
                        swapped = np.swapaxes(data, data_format.index('locations'), 0)
                        selected = data[ch_idx][np.newaxis, :]
                        data = np.swapaxes(selected, data_format.index('locations'), 0)
                    if time_limits is not None:
                        # average over the selected temporal range
                        times = subject_item.times
                        tmin_idx = np.where(times >= time_limits[0])[0][0]
                        tmax_idx = np.where(times <= time_limits[1])[0][-1]
                        swapped = np.swapaxes(data, data_format.index('times'), 0)
                        averaged = np.mean(swapped[tmin_idx:tmax_idx], axis=0)[np.newaxis, :]
                        data = np.swapaxes(averaged, data_format.index('times'), 0)
                    cond_data.append(data)
                group_data.append(cond_data)

            # The format needed is:
            # (n_conds, n_subjects, ..., n_channels)
            swapped = np.swapaxes(np.array(group_data), 0, 1)
            rolled = np.rollaxis(swapped, 2 + data_format.index('locations'), swapped.ndim)
            final_data[group_key] = rolled
            return final_data
    else:
        raise Exception("Only within and between subjects designs are supported")

