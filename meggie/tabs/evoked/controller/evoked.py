# coding: utf-8

"""
"""

import copy
import logging
import os

import mne
import numpy as np
import matplotlib.pyplot as plt

import meggie.utilities.filemanager as filemanager

from meggie.utilities.colors import color_cycle
from meggie.utilities.groups import average_data_to_channel_groups

from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_unit


def plot_channel_averages(experiment, selected_evokeds):
    """
    Draws a topography representation of the evoked potentials.

    """
    layout = filemanager.read_layout(experiment.layout)
    colors = color_cycle(len(evokeds))

    # get evokeds
    evokeds = None

    channel_groups = experiment.channel_groups

    new_evokeds = []
    for evoked_idx, evoked in enumerate(evokeds):
        new_evokeds.append(evoked.copy().drop_channels(evoked.info['bads']))

    averages = []
    for evoked_idx, evoked in enumerate(new_evokeds):
        data_labels, averaged_data = average_data_to_channel_groups(
            evoked.data, evoked.info['ch_names'], channel_groups)
        averages.append((data_labels, averaged_data))
        shape = averaged_data.shape

    # create averages
    # then plot, maybe using plot_timeseries of mne, or using this.

    for ii in range(shape[0]):
        fig, ax = plt.subplots()
        for evoked_idx in range(len(new_evokeds)):
            evoked_name = new_evokeds[evoked_idx].comment
            times = new_evokeds[evoked_idx].times
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('{}'.format(get_unit(
                averages[evoked_idx][0][ii][0]
            )))
            ax.plot(times, averages[evoked_idx][1][ii],
                    color=colors[evoked_idx])
        ch_type, ch_group = averages[evoked_idx][0][ii]
        title = 'Evoked ({0}, {1})'.format(ch_type, ch_group)
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
