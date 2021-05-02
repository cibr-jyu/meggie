# coding: utf-8

"""
"""

import logging
import os

from collections import OrderedDict

import mne
import scipy
import numpy as np
import matplotlib.pyplot as plt

import meggie.utilities.filemanager as filemanager

from meggie.datatypes.evoked.evoked import Evoked

from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import get_channel_average_fig_size
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.channels import pairless_grads
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.stats import prepare_data_for_permutation
from meggie.utilities.stats import permutation_analysis
from meggie.utilities.stats import report_permutation_results
from meggie.utilities.stats import plot_permutation_results

from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_unit


def plot_channel_averages(experiment, evoked):
    """
    """

    colors = color_cycle(len(list(evoked.content.keys())))
    times = list(evoked.content.values())[0].times

    averages = {}
    for key, mne_evoked in sorted(evoked.content.items()):
        data_labels, averaged_data = create_averages(experiment, mne_evoked)

        for label_idx, label in enumerate(data_labels):
            if not label in averages:
                averages[label] = []
            averages[label].append((key, averaged_data[label_idx]))

    ch_types = sorted(set([label[0] for label in averages.keys()]))
    for ch_type in ch_types:

        ch_groups = sorted([label[1] for label in averages.keys() 
                            if label[0] == ch_type])

        ncols = min(4, len(ch_groups))
        nrows = int((len(ch_groups) - 1) / ncols + 1)

        fig, axes = plt.subplots(nrows=nrows, ncols=ncols, squeeze=False)
        fig.set_size_inches(*get_channel_average_fig_size(nrows, ncols))
        for ax_idx in range(ncols*nrows):
            ax = axes[ax_idx // ncols, ax_idx % ncols]
            if ax_idx >= len(ch_groups):
                ax.axis('off')
                continue

            ch_group = ch_groups[ax_idx]
            ax.set_title(ch_group)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power ({})'.format(
                get_unit(ch_type)))

            handles = []
            for color_idx, (key, curve) in enumerate(averages[(ch_type, ch_group)]):
                handles.append(ax.plot(times, curve, color=colors[color_idx], label=key)[0])

            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        fig.legend(handles=handles)
        title_elems = [evoked.name, ch_type]
        fig.canvas.set_window_title('_'.join(title_elems))
        fig.suptitle(' '.join(title_elems))
        fig.tight_layout()

    plt.show()

def run_permutation_test(experiment, window, selected_name, groups, time_limits,
                         frequency_limits, location_limits, threshold,
                         significance, n_permutations, design):
    """
    """
    if location_limits[0] == "ch_name" and time_limits is not None:
        raise Exception('Cannot run permutation tests with both location and time limits')

    evoked_item = experiment.active_subject.evoked[selected_name]
    conditions = list(evoked_item.content.keys())
    groups = OrderedDict(sorted(groups.items()))
    times = evoked_item.times

    info, data, adjacency = prepare_data_for_permutation(
        experiment, design, groups, 'evoked', selected_name,
        location_limits, time_limits, frequency_limits, 
        data_format=('locations', 'times'),
        do_meanwhile=window.update_ui)

    results = permutation_analysis(data, design, conditions, groups, threshold, adjacency, n_permutations,
                                   do_meanwhile=window.update_ui)

    report_permutation_results(results, selected_name, significance,
                               location_limits=location_limits,
                               time_limits=time_limits)

    def time_fun(cluster_idx, cluster, pvalue, res_key):
        """
        """
        fig, ax = plt.subplots()
        if design == 'within-subjects':
            colors = color_cycle(len(conditions))
            for cond_idx, condition in enumerate(conditions):
                evoked = np.mean(data[res_key][cond_idx][:, :, np.unique(cluster[-1])],
                                 axis=(0, -1))
                ax.plot(times, evoked, label=condition, color=colors[cond_idx])
        else:
            colors = color_cycle(len(groups))
            for group_idx, (group_key, group) in enumerate(groups.items()):
                evoked = np.mean(data[res_key][group_key][:, :, np.unique(cluster[-1])],
                                 axis=(0, -1))
                ax.plot(times, evoked, label=group_key, color=colors[group_idx])
        ax.legend()
        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Amplitude')
        tmin = np.min(times[cluster[0]])
        tmax = np.max(times[cluster[0]])
        ax.axvspan(tmin, tmax, alpha=0.5, color='blue')
        fig.suptitle('Cluster ' + str(cluster_idx+1) + ' for ' +
                     str(res_key) + ' (' + str(pvalue) + ')')

    def location_fun(cluster_idx, cluster, pvalue, res_key):
        map_ = [1 if idx in cluster[-1] else 0 for idx in
                range(len(info['ch_names']))]

        fig, ax = plt.subplots()
        ch_type = location_limits[1]
        mne.viz.plot_topomap(np.array(map_), info, vmin=0, vmax=1,
                             cmap='Reds', sensors='r+', axes=ax, ch_type=ch_type)

        fig.suptitle(ch_type + ' cluster of ' + str(cluster_idx+1) + ' for ' +
                     str(res_key) + ' (' + str(pvalue) + ')')

    plot_permutation_results(results, significance,
                             location_limits=location_limits,
                             time_limits=time_limits,
                             location_fun=location_fun,
                             time_fun=time_fun)



def create_averages(experiment, mne_evoked):
    """
    """
    channel_groups = experiment.channel_groups

    mne_evoked = mne_evoked.copy().drop_channels(mne_evoked.info['bads'])

    data_labels, averaged_data = average_to_channel_groups(
        mne_evoked.data, mne_evoked.info, 
        mne_evoked.info['ch_names'], channel_groups)

    return data_labels, averaged_data


@threaded
def group_average_evoked(experiment, evoked_name, groups, new_name):
    """
    """
    keys = []
    time_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                evoked = subject.evoked.get(evoked_name)

                mne_evokeds = evoked.content
                for mne_evoked in mne_evokeds.values():
                    time_arrays.append(mne_evoked.times)
            except Exception as exc:
                continue

    assert_arrays_same(time_arrays)

    grand_evokeds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            evoked = subject.evoked.get(evoked_name)
            if not evoked:
                logging.getLogger('ui_logger').warning(
                    evoked_name + ' not present for ' + subject.name)
                continue

            for evoked_item_key, evoked_item in evoked.content.items():
                grand_key = (group_key, evoked_item_key)

                if grand_key not in grand_evokeds:
                    grand_evokeds[grand_key] = []
                grand_evokeds[grand_key].append(evoked_item)

    grand_averages = {}
    new_keys = []
    for key, grand_evoked in grand_evokeds.items():
        new_key = str(key[1]) + '_' + str(key[0])
        if len(grand_evoked) == 1:
            grand_averages[new_key] = grand_evoked[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(grand_evoked)
        new_keys.append(new_key)

    subject = experiment.active_subject

    evoked_directory = subject.evoked_directory

    params = {'conditions': new_keys,
              'groups': groups}

    grand_average_evoked = Evoked(new_name, evoked_directory, params,
                                  content=grand_averages)

    grand_average_evoked.save_content()
    subject.add(grand_average_evoked, 'evoked')

@threaded
def save_all_channels(experiment, selected_name):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for key, mne_evoked in evoked.content.items():
            column_names = format_floats(mne_evoked.times)

            for ch_idx, ch_name in enumerate(mne_evoked.info['ch_names']):
                if ch_name in mne_evoked.info['bads']:
                    continue
                csv_data.append(mne_evoked.data[ch_idx].tolist())

                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_all_channels_evoked.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

@threaded
def save_channel_averages(experiment, selected_name):
    """
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for key, mne_evoked in evoked.content.items():

            data_labels, averaged_data = create_averages(
                experiment, mne_evoked)

            csv_data.extend(averaged_data.tolist())
            column_names = format_floats(mne_evoked.times)

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_channel_averages_evoked.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

