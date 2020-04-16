# coding: utf-8
"""
"""

import os
import logging

from copy import deepcopy
from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt

import mne

import meggie.utilities.filemanager as filemanager

from meggie.datatypes.spectrum.spectrum import Spectrum

from meggie.utilities.events import find_stim_channel
from meggie.utilities.events import Events

from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.formats import format_floats
from meggie.utilities.colors import color_cycle
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.units import get_scaling
from meggie.utilities.units import get_unit
from meggie.utilities.units import get_power_unit
from meggie.utilities.decorators import threaded


def find_event_times(raw, event_id, mask):
    stim_ch = find_stim_channel(raw)
    sfreq = raw.info['sfreq']

    events = Events(raw, stim_ch, mask, event_id).events
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
        if np.all(np.isclose(row, 0)):
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

    logging.getLogger('ui_logger').info(
        'Plotting spectrum channel averages..')

    averages = {}
    for idx, (key, psd) in enumerate(data.items()):

        data_labels, averaged_data = average_to_channel_groups(
            psd, info, ch_names, channel_groups)

        if not data_labels:
            raise Exception('No channel groups matching the data found.')

        averages[key] = data_labels, averaged_data
        shape = averaged_data.shape

    for ii in range(shape[0]):
        fig, ax = plt.subplots()
        for color_idx, key in enumerate(averages.keys()):
            ax.set_xlabel('Frequency (Hz)')

            ax.set_ylabel('Power ({})'.format(get_power_unit(
                averages[key][0][ii][0],
                log_transformed
            )))

            if log_transformed:
                curve = 10 * np.log10(averages[key][1][ii])
            else:
                curve = averages[key][1][ii]

            ax.plot(freqs, curve, color=colors[color_idx], label=key)

        ax.legend()
        ch_type, ch_group = averages[key][0][ii]
        title = 'spectrum_{0}_{1}_{2}'.format(name, ch_type, ch_group)
        fig.canvas.set_window_title(title)
        fig.suptitle(title)

    plt.show()


def plot_spectrum_topo(experiment, name, log_transformed=True):
    """
    """

    subject = experiment.active_subject
    subject_name = subject.name

    spectrum = subject.spectrum.get(name)

    data = spectrum.content
    freqs = spectrum.freqs
    ch_names_cleaned = [ch_name.replace(' ', '') for ch_name in spectrum.ch_names]

    channel_groups = experiment.channel_groups

    info = subject.get_raw().info
    info_ch_names_cleaned = [ch_name.replace(' ', '') for ch_name in 
                             info['ch_names']]

    colors = color_cycle(len(data))

    logging.getLogger('ui_logger').info(
        'Plotting spectrum from all channels..')

    def individual_plot(ax, ch_idx):
        """
        Callback for the interactive plot.
        Opens a channel specific plot.
        """

        # notice that ch_idx is index in the original ch_names,
        # and ch_names from spectrum object are only the data channels
        ch_name = info_ch_names_cleaned[ch_idx]
        psd_idx = ch_names_cleaned.index(ch_name)

        for color_idx, (key, psd) in enumerate(data.items()):

            if log_transformed:
                curve = 10 * np.log10(psd[psd_idx])
            else:
                curve = psd[psd_idx]

            ax.plot(freqs, psd[psd_idx], color=colors[color_idx],
                    label=key)

        title = 'spectrum_{0}_{1}'.format(name, ch_name)
        ax.figure.canvas.set_window_title(title)
        ax.figure.suptitle(title)
        ax.set_title('')

        ax.legend()

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(info, ch_idx),
            log_transformed
        )))

        plt.show()

    fig = plt.figure()
    for ax, idx in mne.viz.iter_topography(info, fig=fig,
                                           fig_facecolor='white',
                                           axis_spinecolor='white',
                                           axis_facecolor='white',
                                           on_pick=individual_plot):

        ch_name = info_ch_names_cleaned[idx]
        if ch_name not in ch_names_cleaned:
            continue
        psd_idx = ch_names_cleaned.index(ch_name)

        handles = []
        for color_idx, (key, psd) in enumerate(data.items()):

            if log_transformed:
                curve = 10 * np.log10(psd[psd_idx])
            else:
                curve = psd[psd_idx]

            handles.append(ax.plot(curve, linewidth=0.2, color=colors[color_idx],
                                   label=key)[0])

    fig.legend(handles=handles)
    title = 'spectrum_{0}'.format(name)
    fig.canvas.set_window_title(title)
    fig.suptitle(title)
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
    ch_names_cleaned = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                spectrum = subject.spectrum.get(spectrum_name)
                ch_names_cleaned.append(tuple(
                    [ch_name.replace(' ', '') for ch_name in spectrum.ch_names]))
            except Exception as exc:
                continue
    if len(set(ch_names_cleaned)) != 1:
        logging.getLogger('ui_logger').info(
            "PSD's contain different sets of channels. Identifying common ones..")

        common_ch_names_cleaned = list(set.intersection(*map(set, ch_names_cleaned)))

        logging.getLogger('ui_logger').info(
            str(len(common_ch_names_cleaned)) + ' common channels found.')
        logging.getLogger('ui_logger').debug(
            'Common channels are ' + str(common_ch_names_cleaned))
    else:
        common_ch_names_cleaned = ch_names_cleaned[0]

    grand_psds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            spectrum = subject.spectrum.get(spectrum_name)
            if not spectrum:
                continue

            subject_ch_names_cleaned = [ch_name.replace(' ', '') for ch_name 
                                        in spectrum.ch_names]

            for spectrum_item_key, spectrum_item in spectrum.content.items():
                grand_key = (group_key, spectrum_item_key)

                # get common channels in "subject specific space"
                idxs = [subject_ch_names_cleaned.index(ch_name) for ch_name 
                        in common_ch_names_cleaned]
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
    ch_names = common_ch_names_cleaned[0]
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


def save_all_channels(experiment, selected_name):
    column_names = []
    row_names = []
    csv_data = []

    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue
        for key, psd in spectrum.content.items():
            csv_data.extend(psd.tolist())
            column_names = format_floats(spectrum.freqs)

            for ch_name in spectrum.ch_names:
                name = subject.name + '{' + key + '}[' + ch_name + ']'
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_all_channels_spectrum.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_channel_averages(experiment, selected_name, log_transformed=False):
    column_names = []
    row_names = []
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

            if not data_labels:
                raise Exception('No channel groups matching the data found.')

            csv_data.extend(averaged_data.tolist())

            column_names = format_floats(freqs)

            for ch_type, area in data_labels:
                name = (subject.name + '{' + key + '}[' +
                        ch_type + '|' + area + ']')
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_channel_averages_spectrum.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

