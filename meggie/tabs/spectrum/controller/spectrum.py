# coding: utf-8
"""
"""

import os
import logging

from copy import deepcopy
from collections import OrderedDict

import mne

import numpy as np
import matplotlib.pyplot as plt

import meggie.utilities.filemanager as filemanager

from meggie.datatypes.spectrum.spectrum import Spectrum

from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import find_events
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.formats import format_floats
from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import get_channel_average_fig_size
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import clean_names
from meggie.utilities.units import get_power_unit
from meggie.utilities.decorators import threaded


def find_event_times(raw, event_id, mask):
    stim_ch = find_stim_channel(raw)
    sfreq = raw.info['sfreq']

    events = find_events(raw, stim_ch, mask, event_id)
    times = [(event[0] - raw.first_samp) / sfreq for event in events]
    return times


def get_raw_blocks_from_intervals(subject, intervals):
    """
    """
    raw = subject.get_raw()

    raw_times = raw.times.copy()

    raw_blocks = OrderedDict()
    times = {}
    for ival_type, (avg_group, start, end) in intervals:
        if avg_group not in raw_blocks:
            raw_blocks[avg_group] = []
            times[avg_group] = []

        if ival_type == 'fixed':
            block = raw.copy().crop(tmin=start, tmax=end)
            raw_blocks[avg_group].append(block)
            times[avg_group].append((start, end))
        else:
            # the following code finds all start points of intervals by events or
            # start of recording. then matching end point is found by
            # (can be same) other events or end of recording.
            if start[0] == 'events':
                start_times = find_event_times(raw, start[1], start[2])
            elif start[0] == 'start':
                start_times = [raw_times[0]]
            elif start[0] == 'end':
                start_times = [raw_times[-1]]

            for start_time in start_times:
                if end[0] == 'events':
                    end_times = find_event_times(raw, end[1], end[2])
                    found = False
                    for end_time in end_times:
                        # use equality so that one can also specify same trigger for
                        # start and end (with different offsets)
                        if end_time >= start_time:
                            found = True
                            break
                    if not found:
                        logging.getLogger('ui_logger').info(
                            'Found start event with no matching end event')
                        continue
                elif end[0] == 'start':
                    end_time = raw_times[0]
                elif end[0] == 'end':
                    end_time = raw_times[-1]

                # crop with offsets
                times[avg_group].append((start_time + start[3],
                                         end_time + end[3]))
                block = raw.copy().crop(tmin=(start_time + start[3]),
                                        tmax=(end_time + end[3]))
                raw_blocks[avg_group].append(block)

    for key in raw_blocks:
        if len(raw_blocks[key]) == 0:
            raise Exception('Was not able to find raw segments for all groups')
     
    return times, raw_blocks


@threaded
def create_power_spectrum(subject, spectrum_name, params, intervals):
    """
    """
    # get raw objects organized with average groups as keys
    ival_times, raw_block_groups = get_raw_blocks_from_intervals(subject,
                                                                 intervals)

    raw = subject.get_raw()
    info = raw.info

    picks = mne.pick_types(info, meg=True, eeg=True,
                           exclude='bads')

    # remove zero channels from picks
    zero_idxs = []
    for idx, row in enumerate(raw._data):
        if np.all(row == 0):
            zero_idxs.append(idx)
    picks = [pick for pick in picks if pick not in zero_idxs]

    fmin = params['fmin']
    fmax = params['fmax']
    nfft = params['nfft']
    overlap = params['overlap']

    # compute psd's
    psd_groups = OrderedDict()
    for key, raw_blocks in raw_block_groups.items():
        for raw_block in raw_blocks:
            length = len(raw_block.times)
            psds, freqs = mne.time_frequency.psd_welch(
                raw_block, fmin=fmin, fmax=fmax,
                n_fft=nfft, n_overlap=overlap, picks=picks,
                proj=True)

            if key not in psd_groups:
                psd_groups[key] = []

            psd_groups[key].append((psds, freqs, length))

    for psd_list in psd_groups.values():
        freqs = psd_list[0][1]
        break

    psds = []
    for psd_list in psd_groups.values():
        # do a weighted (raw block lengths as weights) average of psds inside a
        # group
        weights = np.array([length for psds_, freqs, length in psd_list])
        weights = weights.astype(float) / np.sum(weights)
        psd = np.average([psds_ for psds_, freqs, length in psd_list],
                         weights=weights, axis=0)
        psds.append(psd)

    # find all channel names this way because earlier
    # the dimension of channels was reduced with picks
    picked_ch_names = [ch_name for ch_idx, ch_name in
                       enumerate(info['ch_names']) if
                       ch_idx in picks]

    psd_data = dict(zip(psd_groups.keys(), psds))

    params = deepcopy(params)
    params['conditions'] = [elem for elem in psd_groups.keys()]
    params['intervals'] = ival_times

    spectrum = Spectrum(spectrum_name, subject.spectrum_directory,
                        params, psd_data, freqs, picked_ch_names)

    spectrum.save_content()
    subject.add(spectrum, 'spectrum')


def plot_spectrum_averages(experiment, name, log_transformed=True):
    """
    """

    subject = experiment.active_subject
    subject_name = subject.name

    spectrum = subject.spectrum.get(name)

    data = spectrum.content
    freqs = spectrum.freqs
    ch_names = spectrum.ch_names 
    channel_groups = experiment.channel_groups
    info = subject.get_raw().info

    colors = color_cycle(len(data))

    averages = {}
    for key, psd in sorted(data.items()):

        data_labels, averaged_data = average_to_channel_groups(
            psd, info, ch_names, channel_groups)

        for label_idx, label in enumerate(data_labels):
            if not label in averages:
                averages[label] = []
            averages[label].append((key, averaged_data[label_idx]))

    ch_groups = sorted(set([label[1] for label in averages.keys()]))
    ch_types = sorted(set([label[0] for label in averages.keys()]))

    ncols = 4
    nrows = int((len(ch_groups) - 1) / ncols + 1)

    for ch_type in ch_types:
        fig, axes = plt.subplots(nrows=nrows, ncols=ncols)
        fig.set_size_inches(*get_channel_average_fig_size(nrows, ncols))
        for ch_group_idx, ch_group in enumerate(ch_groups):
            ax = axes[ch_group_idx // ncols, ch_group_idx % ncols]
            ax.set_title(ch_group)
            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Power ({})'.format(
                get_power_unit(ch_type, log_transformed)))

            handles = []
            for color_idx, (key, curve) in enumerate(averages[(ch_type, ch_group)]):
                if log_transformed:
                    curve = 10 * np.log10(curve)
                handles.append(ax.plot(freqs, curve, color=colors[color_idx], label=key)[0])

        fig.legend(handles=handles)
        title_elems = [name, ch_type]
        fig.canvas.set_window_title('_'.join(title_elems))
        fig.suptitle(' '.join(title_elems))
        fig.tight_layout()

    plt.show()


def plot_spectrum_topo(experiment, name, log_transformed=True, ch_type='meg'):
    """
    """

    subject = experiment.active_subject
    subject_name = subject.name
    spectrum = subject.spectrum.get(name)
    data = spectrum.content
    freqs = spectrum.freqs
    ch_names = spectrum.ch_names
    info = subject.get_raw().info
    if ch_type == 'meg':
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                           if ch_idx in mne.pick_types(info, meg=True, eeg=False)]
    else:
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                           if ch_idx in mne.pick_types(info, eeg=True, meg=False)]
    info = info.copy().pick_channels(picked_channels)

    colors = color_cycle(len(data))

    def individual_plot(ax, info_idx, names_idx):
        """
        """
        ch_name = ch_names[names_idx]
        for color_idx, (key, psd) in enumerate(sorted(data.items())):

            if log_transformed:
                curve = 10 * np.log10(psd[names_idx])
            else:
                curve = psd[names_idx]

            ax.plot(freqs, curve, color=colors[color_idx],
                    label=key)

        title_elems = [name, ch_name]
        ax.figure.canvas.set_window_title('_'.join(title_elems))
        ax.figure.suptitle(' '.join(title_elems))
        ax.set_title('')

        ax.legend()
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(info, info_idx),
            log_transformed
        )))

        plt.show()

    fig = plt.figure()

    for ax, info_idx, names_idx in iterate_topography(
            fig, info, ch_names, individual_plot):

        handles = []
        for color_idx, (key, psd) in enumerate(sorted(data.items())):

            if log_transformed:
                curve = 10 * np.log10(psd[names_idx])
            else:
                curve = psd[names_idx]

            handles.append(ax.plot(curve, color=colors[color_idx],
                                   linewidth=0.5, label=key)[0])

    if not handles:
        return

    fig.legend(handles=handles)
    title = 'spectrum_{0}_{1}'.format(name, ch_type)
    fig.canvas.set_window_title(title)
    plt.show()

@threaded
def group_average_spectrum(experiment, spectrum_name, groups, new_name):

    # check data cohesion
    keys = []
    freq_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                spectrum = subject.spectrum.get(spectrum_name)
                keys.append(tuple(sorted(spectrum.content.keys())))
                freq_arrays.append(tuple(spectrum.freqs))
            except Exception as exc:
                continue

    assert_arrays_same(keys, 'Conditions do not match')
    assert_arrays_same(freq_arrays, 'Freqs do not match')

    # handle channel differences
    ch_names = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                spectrum = subject.spectrum.get(spectrum_name)
                ch_names.append(tuple(clean_names(spectrum.ch_names)))
            except Exception as exc:
                continue

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "PSD's contain different sets of channels. Identifying common ones..")

        common_ch_names = list(set.intersection(*map(set, ch_names)))

        logging.getLogger('ui_logger').info(
            str(len(common_ch_names)) + ' common channels found.')
        logging.getLogger('ui_logger').debug(
            'Common channels are ' + str(common_ch_names))
    else:
        common_ch_names = ch_names[0]

    grand_psds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            spectrum = subject.spectrum.get(spectrum_name)
            if not spectrum:
                continue

            subject_ch_names = clean_names(spectrum.ch_names) 

            for spectrum_item_key, spectrum_item in spectrum.content.items():
                grand_key = (group_key, spectrum_item_key)

                # get common channels in "subject specific space"
                idxs = [subject_ch_names.index(ch_name) for ch_name 
                        in common_ch_names]

                spectrum_item = spectrum_item[idxs]

                if grand_key not in grand_psds:
                    grand_psds[grand_key] = []
                grand_psds[grand_key].append(spectrum_item)

    grand_averages = {}
    for key, grand_psd in grand_psds.items():
        new_key = str(key[1]) + '_group_' + str(key[0])
        if len(grand_psd) == 1:
            grand_averages[new_key] = grand_psd[0].copy()
        else:
            grand_averages[new_key] = np.mean(grand_psd, axis=0)

    subject = experiment.active_subject

    try:
        spectrum = subject.spectrum.get(spectrum_name)
    except Exception as exc:
        raise Exception('Active subject should be included in the groups')

    spectrum_directory = subject.spectrum_directory

    freqs = spectrum.freqs
    ch_names = common_ch_names
    data = grand_averages

    params = deepcopy(spectrum.params)

    # individual intervals not relevant in the group item
    params.pop('intervals', None)

    params['groups'] = groups
    params['conditions'] = [elem for elem in grand_averages.keys()]

    spectrum = Spectrum(new_name, subject.spectrum_directory,
                        params, data, freqs, ch_names)

    spectrum.save_content()
    subject.add(spectrum, 'spectrum')

@threaded
def save_all_channels(experiment, selected_name):
    column_names = []
    row_descs = []
    csv_data = []

    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue
        for key, psd in spectrum.content.items():
            csv_data.extend(psd.tolist())
            column_names = format_floats(spectrum.freqs)

            for ch_name in spectrum.ch_names:
                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_all_channels_spectrum.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

@threaded
def save_channel_averages(experiment, selected_name, log_transformed=False):
    column_names = []
    row_descs = []
    csv_data = []

    channel_groups = experiment.channel_groups

    # accumulate csv contents
    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue

        ch_names = spectrum.ch_names
        freqs = spectrum.freqs

        info = subject.get_raw().info

        for key, psd in spectrum.content.items():

            data_labels, averaged_data = average_to_channel_groups(
                psd, info, ch_names, channel_groups)

            if log_transformed:
                csv_data.extend(10 * np.log10(averaged_data.tolist()))
            else:
                csv_data.extend(averaged_data.tolist())

            column_names = format_floats(freqs)

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_channel_averages_spectrum.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

