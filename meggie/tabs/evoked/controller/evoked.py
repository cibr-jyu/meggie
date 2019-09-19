# coding: utf-8

"""
"""

import copy
import logging
import os

import mne
import numpy as np
import matplotlib.pyplot as plt

from meggie.utilities.channels import read_layout
from meggie.utilities.colors import color_cycle
from meggie.utilities.groups import average_data_to_channel_groups

from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_unit


def plot_channel_averages(experiment, evoked):
    """
    Draws a topography representation of the evoked potentials.

    """
    
    # average and restructure for ease of plotting
    averages = {}
    for key, mne_evoked in evoked.content.items():
        data_labels, averaged_data = create_averages(experiment, mne_evoked)
        for idx in range(len(data_labels)):
            if not data_labels[idx] in averages:
                averages[data_labels[idx]] = []
            averages[data_labels[idx]].append(averaged_data[idx])

    layout = read_layout(experiment.layout)
    colors = color_cycle(len(list(averages.values())[0]))

    for type_key, item in averages.items():
        fig, ax = plt.subplots()
        for evoked_idx, evoked_data in enumerate(item):
            mne_evoked = list(evoked.content.values())[evoked_idx]
            evoked_name = mne_evoked.comment
            times = mne_evoked.times
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('{}'.format(get_unit(
                type_key[0]
            )))
            ax.plot(times, evoked_data,
                    color=colors[evoked_idx])
        title = 'Evoked ({0}, {1})'.format(type_key[0], type_key[1])
        fig.canvas.set_window_title(title)
        fig.suptitle(title)

    plt.show()


def create_averages(experiment, mne_evoked):
    channel_groups = experiment.channel_groups

    mne_evoked = mne_evoked.copy().drop_channels(mne_evoked.info['bads'])

    data_labels, averaged_data = average_data_to_channel_groups(
        mne_evoked.data, mne_evoked.info['ch_names'], channel_groups)

    return data_labels, averaged_data


@threaded
def group_average(experiment, evoked_name, groups):
    """
    """

    # sanity checks
    sfreqs = []
    tmins = []
    tmaxs = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            subject = experiment.subjects.get(subject_name)
            if not subject:
                continue
            evoked = subject.evokeds.get(evoked_name)
            if not evoked:
                continue

            mne_evokeds = evoked.mne_evokeds
            for mne_evoked in mne_evokeds.values():
                sfreqs.append(mne_evoked.info['sfreq'])
                tmins.append(mne_evoked.times[0])
                tmaxs.append(mne_evoked.times[-1])

    if len(set(sfreqs)) > 1:
        raise Exception('Sampling rates do not match')
    if len(set(tmins)) > 1 or len(set(tmaxs)) > 1:
        raise Exception('Times do not match')

    count = 0
    found_subjects = []
    group_info = {}
    for subject in experiment.subjects.values():
        subject_in_groups = False
        for group_key, group_subjects in groups.items():
            if subject.subject_name in group_subjects:
                subject_in_groups = True
        if not subject_in_groups:
            continue

        if subject.evokeds.get(evoked_name):
            count += 1
            evoked = subject.evokeds.get(evoked_name)
            info = evoked.info['epoch_collections'][subject.subject_name]
            group_info[subject.subject_name] = {'epoch_collections': info}
            found_subjects.append(subject)

    if count == 0:
        raise ValueError('No evoked responses found from any subject.')

    grand_evokeds = {}
    for group_key, group_subjects in groups.items():
        for subject in found_subjects:
            if subject.subject_name not in group_subjects:
                continue
            evoked = subject.evokeds.get(evoked_name)
            for evoked_item_key, evoked_item in evoked.mne_evokeds.items():
                grand_key = (group_key, evoked_item_key)
                if grand_key in grand_evokeds:
                    grand_evokeds[grand_key].append(evoked_item)
                else:
                    grand_evokeds[grand_key] = [evoked_item]

    grand_averages = {}
    for key, grand_evoked in grand_evokeds.items():
        new_key = str(key[1]) + '_' + str(key[0])
        if len(grand_evoked) == 1:
            grand_averages[new_key] = grand_evoked[0].copy()

        else:
            grand_averages[new_key] = mne.grand_average(grand_evoked)

        grand_averages[new_key].comment = new_key

    return grand_averages, group_info
