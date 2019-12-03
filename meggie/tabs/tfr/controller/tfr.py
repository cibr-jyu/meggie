# coding: utf-8
"""
"""

import os
import logging

import numpy as np
import matplotlib.pyplot as plt
import mne

from meggie.utilities.channels import read_layout
from meggie.utilities.colors import color_cycle
from meggie.utilities.groups import average_data_to_channel_groups
from meggie.utilities.decorators import threaded
from meggie.utilities.units import get_scaling
from meggie.utilities.units import get_unit
from meggie.utilities.units import get_power_unit
from meggie.utilities.validators import assert_arrays_same

from meggie.datatypes.tfr.tfr import TFR


def plot_tse_topo(experiment, subject, tfr_name, minfreq, maxfreq, baseline):
    """
    """
    subject_name = subject.name

    meggie_tfr = subject.tfr.get(tfr_name)

    lout = read_layout(experiment.layout)

    data = meggie_tfr.content
    example_tfr = list(data.values())[0]
    ch_names = example_tfr.info['ch_names']
    times = example_tfr.times

    lfreq_idx = np.where(example_tfr.freqs >= minfreq)[0][0]
    hfreq_idx = np.where(example_tfr.freqs <= maxfreq)[0][-1]

    if hfreq_idx <= lfreq_idx:
        raise Exception('Something wrong with the frequencies')

    channel_groups = experiment.channel_groups

    colors = color_cycle(len(data))

    # in contrast to spectrum plot, here the channels and locations
    # are both contained in the tfr object, which simplifies things

    logging.getLogger('ui_logger').info('Plotting TSE from all channels..')

    def individual_plot(ax, ch_idx):
        """
        Callback for the interactive plot.
        Opens a channel specific plot.
        """

        ch_name = example_tfr.info['ch_names'][ch_idx]

        fig = plt.gcf()
        fig.canvas.set_window_title(''.join(['tse_', subject_name,
                                             '_', ch_name]))

        conditions = [str(key) for key in data]
        positions = np.arange(0.025, 0.025 + 0.04 * len(conditions), 0.04)

        for cond, col, pos in zip(conditions, colors, positions):
            plt.figtext(0.775, pos, cond, color=col, fontsize=12)

        color_idx = 0
        for tfr in data.values():
            times = tfr.times

            # average over freqs
            tse = np.mean(tfr.data[:, lfreq_idx:hfreq_idx, :], axis=1)
            # correct to baseline
            tse = mne.baseline.rescale(tse, times, baseline=baseline)

            plt.plot(times, tse[ch_idx], color=colors[color_idx])
            plt.axhline(0)
            color_idx += 1

        plt.xlabel('Time (s)')

        plt.ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(example_tfr.info, ch_idx),
            False
        )))

        plt.show()

    for ax, ch_idx in mne.viz.iter_topography(example_tfr.info, fig_facecolor='white',
                                          axis_spinecolor='white',
                                          axis_facecolor='white', layout=lout,
                                          on_pick=individual_plot):

        for color_idx, tfr in enumerate(data.values()):
            # average over freqs
            tse = np.mean(tfr.data[:, lfreq_idx:hfreq_idx, :], axis=1)
            # correct to baseline
            tse = mne.baseline.rescale(tse, times, baseline=baseline)

            ax.plot(tse[ch_idx], linewidth=0.2, color=colors[color_idx])

    plt.gcf().canvas.set_window_title('tse_' + subject_name)
    plt.show()


def plot_tse_averages(experiment, subject, tfr_name, minfreq, maxfreq, baseline):
    """
    """
    subject_name = subject.name

    meggie_tfr = subject.tfr.get(tfr_name)

    lout = read_layout(experiment.layout)

    data = meggie_tfr.content
    example_tfr = list(data.values())[0]
    ch_names = example_tfr.info['ch_names']
    times = example_tfr.times

    lfreq_idx = np.where(example_tfr.freqs >= minfreq)[0][0]
    hfreq_idx = np.where(example_tfr.freqs <= maxfreq)[0][-1]

    if hfreq_idx <= lfreq_idx:
        raise Exception('Something wrong with the frequencies')

    channel_groups = experiment.channel_groups

    colors = color_cycle(len(data))

    # in contrast to spectrum plot, here the channels and locations
    # are both contained in the tfr object, which simplifies things

    logging.getLogger('ui_logger').info('Plotting TSE channel averages..')

    averages = {}
    for idx, (key, tfr) in enumerate(data.items()):

        data_labels, averaged_data = average_data_to_channel_groups(
            tfr.data, ch_names, channel_groups)

        averages[key] = data_labels, averaged_data
        shape = averaged_data.shape

    for ii in range(shape[0]):
        fig, ax = plt.subplots()
        for color_idx, key in enumerate(data.keys()):
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power ({})'.format(get_power_unit(
                averages[key][0][ii][0],
                False
            )))

            # average over freqs
            tse = np.mean(averages[key][1][ii]
                          [lfreq_idx:hfreq_idx, :], axis=0)
            # correct to baseline
            tse = mne.baseline.rescale(tse, times, baseline=baseline)

            ax.plot(times, tse, color=colors[color_idx])
            ax.axhline(0)
        ch_type, ch_group = averages[key][0][ii]
        title = 'TSE ({0}, {1})'.format(ch_type, ch_group)
        fig.canvas.set_window_title(title)
        fig.suptitle(title)

    plt.show()


def plot_tfr_averages(experiment, subject, tfr_name, tfr_condition, 
                      blmode, blstart, blend):

    layout = read_layout(experiment.layout)

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = subject.tfr[tfr_name].content.get(tfr_condition)

    logging.getLogger('ui_logger').info("Plotting TFR channel averages...")

    data = tfr.data
    ch_names = tfr.info['ch_names']
    channel_groups = experiment.channel_groups

    data_labels, averaged_data = average_data_to_channel_groups(
        data, ch_names, channel_groups)

    sfreq = tfr.info['sfreq']
    times = tfr.times
    freqs = tfr.freqs

    for idx in range(len(data_labels)):
        data = averaged_data[idx]
        labels = data_labels[idx]
        info = mne.create_info(ch_names=['grandaverage'],
                               sfreq=sfreq,
                               ch_types='mag')
        tfr = mne.time_frequency.tfr.AverageTFR(
            info, data[np.newaxis, :], times, freqs, 1)

        title = labels[1] + ' (' + labels[0] + ')'

        # prevent interaction as no topology is involved now
        def onselect(*args, **kwargs):
            pass

        tfr._onselect = onselect

        tfr.plot(baseline=bline, mode=mode,
                 title=title)


def plot_tfr_topo(experiment, subject, tfr_name, tfr_condition, 
                  blmode, blstart, blend):

    layout = read_layout(experiment.layout)

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = subject.tfr[tfr_name].content.get(tfr_condition)

    logging.getLogger('ui_logger').info("Plotting TFR from all channels...")

    fig = tfr.plot_topo(layout=layout, show=False,
                        baseline=bline, mode=mode)

    fig.canvas.set_window_title('TFR (' + tfr_name + ', ' + 
                                tfr_condition + ')')

    def onclick(event):
        channel = plt.getp(plt.gca(), 'title')
        plt.gcf().canvas.set_window_title('_'.join(['TFR', tfr_name,
                                                    channel]))
        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.show()


@threaded
def create_tfr(subject, tfr_name, epochs_names,
               freqs, decim, ncycles, subtract_evoked):

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
                                                n_cycles=ncycles,
                                                decim=decim, 
                                                average=True,
                                                return_itc=False)
        tfr.comment = epoch_name
        tfrs[epoch_name] = tfr

    # convert list-like to list
    if hasattr(ncycles, '__len__'):
        ncycles = list(ncycles)

    params = {
        'decim': decim,
        'ncycles': ncycles,
        'subtract_evoked': subtract_evoked,
        'conditions': epochs_names
    }

    meggie_tfr = TFR(tfr_name, subject.tfr_directory, params, tfrs)

    meggie_tfr.save_content()
    subject.add(meggie_tfr, "tfr")


def group_average_tfr(experiment, tfr_name, groups):

    # check data coherence
    keys = []
    freqs = []
    times = []
    ch_names = []
    decims = []
    subtracts = []

    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            subject = experiment.subjects.get(subject_name)
            if not subject:
                continue
            meggie_tfr = subject.tfrs.get(tfr_name)
            if not meggie_tfr:
                continue

            tfr = list(meggie_tfr.tfrs.values())[0]

            keys.append(tuple(list(meggie_tfr.tfrs.keys())))

            freqs.append(tuple(tfr.freqs))
            times.append(tuple(tfr.times))
            ch_names.append(tuple([ch_name.replace(" ", "") for ch_name in
                                   tfr.info['ch_names']]))
            decims.append(meggie_tfr.decim)
            subtracts.append(meggie_tfr.evoked_subtracted)

    if len(set(keys)) != 1:
        raise Exception("TFR's contain different sets of conditions")
    if len(set(freqs)) != 1:
        raise Exception("TFR's contain different sets of freqs")
    if len(set(times)) != 1:
        raise Exception("TFR's contain different sets of times")
    if len(set(decims)) != 1:
        raise Exception("TFR's contain different sets of decims")
    if len(set(subtracts)) != 1:
        raise Exception("TFR's contain different evoked subtraction settings")

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "TFR's contain different sets of channels. Identifying common ones..")
        common_ch_names = list(set.intersection(*map(set, ch_names)))
        logging.getLogger('ui_logger').info(str(len(common_ch_names)) +
                                            ' common channels found.')
        logging.getLogger('ui_logger').debug(
            'Common channels are ' + str(ch_names))
    else:
        common_ch_names = ch_names[0]

    grand_tfrs = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.subject_name not in group_subjects:
                continue
            meggie_tfr = subject.tfrs.get(tfr_name)
            if not meggie_tfr:
                continue
            for tfr_item_key, tfr_item in meggie_tfr.tfrs.items():
                grand_key = (group_key, tfr_item_key)

                idxs = []
                # get common channels in "subject specific space"
                for ch_idx, ch_name in enumerate(
                    [ch.replace(' ', '') for ch in tfr_item.info['ch_names']]
                ):
                    if ch_name in common_ch_names:
                        idxs.append(ch_idx)
                tfr_item = tfr_item.copy().drop_channels(
                    [ch_name for ch_idx, ch_name in enumerate(tfr_item.info['ch_names'])
                     if ch_idx not in idxs])

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
                grand_tfr, drop_bads=False)

    active_subject = experiment.active_subject
    meggie_tfr = active_subject.tfrs.get(tfr_name)

    decim = meggie_tfr.decim
    n_cycles = meggie_tfr.n_cycles
    evoked_subtracted = meggie_tfr.evoked_subtracted

    meggie_tfr = TFR(grand_averages, 'group_' + tfr_name,
                     active_subject,
                     decim, n_cycles, evoked_subtracted)

    meggie_tfr.save_content()
    experiment.active_subject.add(meggie_tfr, "tfr")

