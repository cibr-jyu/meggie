# coding: utf-8
"""
"""

import os
import logging

import numpy as np
import matplotlib.pyplot as plt
import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.colors import color_cycle
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import clean_names
from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_scaling
from meggie.utilities.units import get_unit
from meggie.utilities.units import get_power_unit
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.decorators import threaded

from meggie.datatypes.tfr.tfr import TFR


def _compute_tse(meggie_tfr, fmin, fmax, tmin, tmax, blmode, blstart, blend):
    """
    """
    tfrs = meggie_tfr.content

    times = meggie_tfr.times

    fmin_idx = np.where(meggie_tfr.freqs >= fmin)[0][0]
    fmax_idx = np.where(meggie_tfr.freqs <= fmax)[0][-1]

    if fmax_idx <= fmin_idx:
        raise Exception('Something wrong with the frequencies')

    tmin_idx = np.where(times >= tmin)[0][0]
    tmax_idx = np.where(times <= tmax)[0][-1]

    tses = {}
    for key, tfr in tfrs.items():
        tse = np.mean(tfr.data[:, 
                               fmin_idx:fmax_idx+1, 
                               tmin_idx:tmax_idx+1], axis=1)

        if blmode:
            if blstart < tmin:
                raise Exception(
                    'Baseline start should not be earlier than crop start.')

            if blend > tmax:
                raise Exception(
                    'Baseline end should not be later than crop end.')

            # correct to baseline
            tse = mne.baseline.rescale(tse, times, baseline=(blstart, blend), 
                                       mode=blmode)

        tses[key] = tse

    return times[tmin_idx:tmax_idx+1], tses


def plot_tse_topo(experiment, subject, tfr_name, blmode, blstart, blend, 
                  tmin, tmax, fmin, fmax):
    """
    """
    meggie_tfr = subject.tfr.get(tfr_name)

    times, tses = _compute_tse(meggie_tfr, fmin, fmax, 
                               tmin, tmax, blmode, blstart, blend)

    ch_names = meggie_tfr.ch_names
    info = meggie_tfr.info
    colors = color_cycle(len(tses))

    logging.getLogger('ui_logger').info('Plotting TSE from all channels..')


    def individual_plot(ax, info_idx, names_idx):
        """
        """
        ch_name = ch_names[names_idx]

        title = 'TSE_{0}_{1}'.format(tfr_name, ch_name)
        ax.figure.canvas.set_window_title(title)
        ax.figure.suptitle(title)
        ax.set_title('')

        for color_idx, (key, tse) in enumerate(tses.items()):
            ax.plot(times, tse[names_idx], color=colors[color_idx], label=key)
            ax.axhline(0)
            ax.axvline(0)

        ax.legend()

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(info, info_idx),
            False
        )))

        plt.show()

    fig = plt.figure()
    for idx, info_idx, names_idx in iterate_topography(
            fig, info, ch_names, individual_plot):

        handles = []
        for color_idx, (key, tse) in enumerate(tses.items()):
            handles.append(ax.plot(tse[names_idx], linewidth=0.2, 
                           color=colors[color_idx],
                           label=key)[0])

    fig.legend(handles=handles)
    title = 'TSE_{0}'.format(tfr_name)
    fig.canvas.set_window_title(title)
    fig.suptitle(title)

    plt.show()


def plot_tse_averages(experiment, subject, tfr_name, blmode, blstart, blend,
                      tmin, tmax, fmin, fmax):
    """
    """
    meggie_tfr = subject.tfr.get(tfr_name)

    times, tses = _compute_tse(meggie_tfr, fmin, fmax, 
                               tmin, tmax, blmode, blstart, blend)

    ch_names = meggie_tfr.ch_names
    info = meggie_tfr.info
    colors = color_cycle(len(tses))

    channel_groups = experiment.channel_groups

    logging.getLogger('ui_logger').info('Plotting TSE channel averages..')

    averages = {}
    for idx, (key, tse) in enumerate(tses.items()):

        data_labels, averaged_data = average_to_channel_groups(
            tse, info, ch_names, channel_groups)

        if not data_labels:
            raise Exception('No channel groups matching the data found.')

        averages[key] = data_labels, averaged_data
        shape = averaged_data.shape

    for ii in range(shape[0]):
        fig, ax = plt.subplots()
        for color_idx, key in enumerate(averages.keys()):
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power ({})'.format(get_power_unit(
                averages[key][0][ii][0],
                False
            )))

            ax.plot(times, averages[key][1][ii], color=colors[color_idx],
                    label=key)
        ax.axhline(0)
        ax.legend()
        ch_type, ch_group = averages[key][0][ii]
        title = 'TSE_{0}_{1}_{2}'.format(tfr_name, ch_type, ch_group)
        fig.canvas.set_window_title(title)
        fig.suptitle(title)

    plt.show()


def plot_tfr_averages(experiment, subject, tfr_name, tfr_condition, 
                      blmode, blstart, blend,
                      tmin, tmax, fmin, fmax):

    meggie_tfr = subject.tfr[tfr_name]

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = meggie_tfr.content.get(tfr_condition)

    logging.getLogger('ui_logger').info("Plotting TFR channel averages...")

    data = tfr.data
    ch_names = meggie_tfr.ch_names
    channel_groups = experiment.channel_groups

    data_labels, averaged_data = average_to_channel_groups(
        data, meggie_tfr.info, ch_names, channel_groups)

    if not data_labels:
        raise Exception('No channel groups matching the data found')

    sfreq = meggie_tfr.info['sfreq']
    times = meggie_tfr.times
    freqs = meggie_tfr.freqs

    for idx in range(len(data_labels)):
        data = averaged_data[idx]
        labels = data_labels[idx]
        info = mne.create_info(ch_names=['grand_average'],
                               sfreq=sfreq,
                               ch_types='mag')
        tfr = mne.time_frequency.tfr.AverageTFR(info, 
            data[np.newaxis, :], 
            times, freqs, 1)

        title = 'TFR_{0}_{1}'.format(labels[1], labels[0])

        # prevent interaction as no topography is involved now
        def onselect(*args, **kwargs):
            pass

        tfr._onselect = onselect

        fig = tfr.plot(baseline=bline, mode=mode, title=title, 
                       fmin=fmin, fmax=fmax, 
                       tmin=tmin, tmax=tmax)
        fig.canvas.set_window_title(title)


def plot_tfr_topo(experiment, subject, tfr_name, tfr_condition, 
                  blmode, blstart, blend,
                  tmin, tmax, fmin, fmax):

    meggie_tfr = subject.tfr[tfr_name]

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = meggie_tfr.content.get(tfr_condition)

    logging.getLogger('ui_logger').info("Plotting TFR from all channels...")

    title = 'TFR_{0}_{1}'.format(tfr_name, tfr_condition)
    fig = tfr.plot_topo(show=False,
                        baseline=bline, mode=mode,
                        tmin=tmin, tmax=tmax,
                        fmin=fmin, fmax=fmax,
                        title=title)

    fig.canvas.set_window_title(title)

    def onclick(event):
        channel = plt.getp(plt.gca(), 'title')
        plt.gca().set_title('')

        title = 'TFR_{0}_{1}'.format(tfr_name, channel)
        plt.gcf().canvas.set_window_title(title)
        plt.gcf().suptitle(title)

        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)

    fig.show()


@threaded
def create_tfr(subject, tfr_name, epochs_names,
               freqs, decim, n_cycles, subtract_evoked):

    time_arrays = []
    for name in epochs_names:
        collection = subject.epochs.get(name)
        if collection:
            time_arrays.append(collection.content.times)
    assert_arrays_same(time_arrays)

    tfrs = {}
    for epoch_name in epochs_names:
        epochs = subject.epochs[epoch_name].content
        if subtract_evoked:
            epochs = epochs.copy().subtract_evoked()

        tfr = mne.time_frequency.tfr.tfr_morlet(epochs, 
                                                freqs=freqs, 
                                                n_cycles=n_cycles,
                                                decim=decim, 
                                                average=True,
                                                return_itc=False)
        tfr.comment = epoch_name
        tfrs[epoch_name] = tfr

    # convert list-like to list
    if hasattr(n_cycles, '__len__'):
        n_cycles = list(n_cycles)

    params = {
        'decim': decim,
        'n_cycles': n_cycles,
        'evoked_subtracted': subtract_evoked,
        'conditions': epochs_names
    }

    meggie_tfr = TFR(tfr_name, subject.tfr_directory, params, tfrs)

    meggie_tfr.save_content()
    subject.add(meggie_tfr, "tfr")


@threaded
def group_average_tfr(experiment, tfr_name, groups, new_name):

    # check data cohesion
    keys = []
    freq_arrays = []
    time_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                tfr = subject.tfr.get(tfr_name)
                keys.append(tuple(sorted(tfr.content.keys())))
                freq_arrays.append(tuple(tfr.freqs))
                time_arrays.append(tuple(tfr.times))
            except Exception as exc:
                continue

    assert_arrays_same(keys, 'Conditions do no match')
    assert_arrays_same(freq_arrays, 'Freqs do not match')
    assert_arrays_same(time_arrays)

    # handle channel differences
    ch_names = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                tfr = subject.tfr.get(tfr_name)
                ch_names.append(tuple(clean_names(tfr.ch_names)))
            except Exception as exc:
                continue

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "TFR's contain different sets of channels. Identifying common ones..")

        common_ch_names = list(set.intersection(*map(set, ch_names)))

        logging.getLogger('ui_logger').info(str(len(common_ch_names)) +
                                            ' common channels found.')
        logging.getLogger('ui_logger').debug(
            'Common channels are ' + str(common_ch_names))
    else:
        common_ch_names = ch_names[0]

    grand_tfrs = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            meggie_tfr = subject.tfr.get(tfr_name)
            if not meggie_tfr:
                continue

            for tfr_item_key, tfr_item in meggie_tfr.content.items():
                grand_key = (group_key, tfr_item_key)

                # get common channels in "subject specific space"
                subject_ch_names = tfr_item.info['ch_names']
                for ch_idx, ch_name in enumerate(clean_names(subject_ch_names)):
                    drop_names = []
                    if ch_name not in common_ch_names:
                        drop_names.append(subject_ch_names[ch_idx])
                tfr_item = tfr_item.copy().drop_channels(drop_names)

                # sanity check
                if len(tfr_item.info['ch_names']) != len(common_ch_names):
                    raise Exception('Something wrong with the channels')

                if grand_key in grand_tfrs:
                    grand_tfrs[grand_key].append(tfr_item)
                else:
                    grand_tfrs[grand_key] = [tfr_item]

    grand_averages = {}
    for key, grand_tfr in grand_tfrs.items():
        new_key = str(key[1]) + '_group_' + str(key[0])
        if len(grand_tfr) == 1:
            grand_averages[new_key] = grand_tfr[0].copy()
        else:
            grand_averages[new_key] = mne.grand_average(
                grand_tfr)

    active_subject = experiment.active_subject
    meggie_tfr = active_subject.tfr.get(tfr_name)

    params = {
        'decim': meggie_tfr.decim,
        'n_cycles': meggie_tfr.n_cycles,
        'evoked_subtracted': meggie_tfr.evoked_subtracted,
        'conditions': list(grand_averages.keys()),
        'groups': groups
    }

    meggie_tfr = TFR(new_name, active_subject.tfr_directory, params, grand_averages)

    meggie_tfr.save_content()
    active_subject.add(meggie_tfr, "tfr")


def save_tfr_all_channels(experiment, tfr_name,
                          blmode, blstart, blend,
                          tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_names = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        ch_names = tfr.ch_names

        for key, mne_tfr in tfr.content.items():

            # crop and correct to baseline
            mne_tfr = mne_tfr.copy().crop(tmin=tmin,
                                          tmax=tmax,
                                          fmin=fmin,
                                          fmax=fmax)
            times = mne_tfr.times
            column_names = format_floats(times)
            freqs = format_floats(mne_tfr.freqs)

            data = mne.baseline.rescale(mne_tfr.data, times, baseline=(blstart, blend), 
                                       mode=blmode)

            for ix in range(data.shape[0]):
                for iy in range(data.shape[1]):
                    csv_data.append(data[ix, iy].tolist())

                    row_name = (subject.name +
                                '{' + key + '}' + 
                                '[' + ch_names[ix] + ']' + 
                                '(' + freqs[iy] + ')')
                    row_names.append(row_name)

        folder = filemanager.create_timestamped_folder(experiment)
        fname = tfr_name + '_all_subjects_all_channels_tfr.csv'
        path = os.path.join(folder, fname)

        filemanager.save_csv(path, csv_data, column_names, row_names)
        logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_tfr_channel_averages(experiment, tfr_name,
                              blmode, blstart, blend,
                              tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_names = []
    csv_data = []

    channel_groups = experiment.channel_groups

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        ch_names = tfr.ch_names
        info = tfr.info

        for key, mne_tfr in tfr.content.items():

            # crop and correct to baseline
            mne_tfr = mne_tfr.copy().crop(tmin=tmin,
                                          tmax=tmax,
                                          fmin=fmin,
                                          fmax=fmax)
            times = mne_tfr.times
            column_names = format_floats(times)
            freqs = format_floats(mne_tfr.freqs)

            data = mne.baseline.rescale(mne_tfr.data, times, baseline=(blstart, blend), 
                                       mode=blmode)

            data_labels, averaged_data = average_to_channel_groups(
                data, info, ch_names, channel_groups)

            if not data_labels:
                raise Exception('No channel groups matching the data found')

            for ix in range(averaged_data.shape[0]):
                for iy in range(averaged_data.shape[1]):
                    ch_type, area = data_labels[ix]

                    csv_data.append(averaged_data[ix, iy].tolist())

                    row_name = (subject.name +
                                '{' + key + '}' +
                                '[' + ch_type + '|' + area + ']' +
                                '(' + freqs[iy] + ')')
                    row_names.append(row_name)

        folder = filemanager.create_timestamped_folder(experiment)
        fname = tfr_name + '_all_subjects_channel_averages_tfr.csv'
        path = os.path.join(folder, fname)

        filemanager.save_csv(path, csv_data, column_names, row_names)
        logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_tse_all_channels(experiment, tfr_name, blmode, blstart, 
                          blend, tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_names = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        times, tses = _compute_tse(tfr, fmin, fmax, 
                                   tmin, tmax, blmode, blstart, blend)
        column_names = format_floats(times)

        for key, tse in tses.items():
            csv_data.extend(tse.tolist())

            for ch_name in tfr.ch_names:
                name = (subject.name +
                        '{' + key + '}' +
                        '[' + ch_name + ']')
                row_names.append(name)
    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_all_channels_tfr.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_tse_channel_averages(experiment, tfr_name, blmode, blstart, 
                              blend, tmin, tmax, fmin, fmax):
    """
    """
    column_names = []
    row_names = []
    csv_data = []

    channel_groups = experiment.channel_groups

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        times, tses = _compute_tse(tfr, fmin, fmax, 
                                   tmin, tmax, blmode, blstart, blend)
        column_names = format_floats(times)

        for key, tse in tses.items():

            data_labels, averaged_data = average_to_channel_groups(
                tse, tfr.info, tfr.ch_names, channel_groups)

            if not data_labels:
                raise Exception('No channel groups matching the data found.')

            csv_data.extend(averaged_data.tolist())

            for ch_type, area in data_labels:
                name = (subject.name +
                        '{' + key + '}' +
                        '[' + ch_type + '|' + area + ']')
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_channel_averages_tfr.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


