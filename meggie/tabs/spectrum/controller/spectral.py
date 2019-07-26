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


from meggie.code_meggie.analysis.utils import color_cycle
from meggie.code_meggie.analysis.utils import average_data_to_channel_groups

from meggie.ui.utils.decorators import threaded
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.utils.units import get_scaling
from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.utils.units import get_power_unit
from meggie.code_meggie.structures.spectrum import Spectrum
from meggie.code_meggie.structures.tfr import TFR


@threaded
def _compute_spectrum(raw_block_groups, params):
    """Performed in a worker thread."""
    fmin = params['fmin']
    fmax = params['fmax']
    nfft = params['nfft']
    overlap = params['overlap']
    picks = params['picks']

    psd_groups = OrderedDict()

    for key, raw_blocks in raw_block_groups.items():
        for raw_block in raw_blocks:

            length = len(raw_block.times)

            psds, freqs = mne.psd_welch(raw_block, fmin=fmin, fmax=fmax,
                                        n_fft=nfft, n_overlap=overlap, picks=picks,
                                        proj=True)

            if params['log']:
                psds = 10 * np.log10(psds)

            if key not in psd_groups:
                psd_groups[key] = []

            psd_groups[key].append((psds, freqs, length))

    return psd_groups


def create_power_spectrum(experiment, spectrum_name, params, raw_block_groups,
                          update_ui=(lambda: None)):
    """
    """

    for raw_blocks in raw_block_groups.values():
        info = raw_blocks[0].info
        break

    picks = mne.pick_types(info, meg=True, eeg=True,
                           exclude='bads')

    params['picks'] = picks
    psd_groups = _compute_spectrum(raw_block_groups, params,
                                   do_meanwhile=update_ui)

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

    spectrum = Spectrum(spectrum_name, experiment.active_subject,
                        params['log'], psd_data, freqs, picked_ch_names)

    experiment.active_subject.add_spectrum(spectrum)

    spectrum.save_data()


def plot_tse(experiment, tfr_name, minfreq, maxfreq, baseline, output):

    subject = experiment.active_subject
    subject_name = subject.subject_name

    meggie_tfr = subject.tfrs.get(tfr_name)

    lout = fileManager.read_layout(experiment.layout)

    data = meggie_tfr.tfrs
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

    if output == 'all_channels':
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
                tse = mne.rescale(tse, times, baseline=baseline)

                plt.plot(times, tse[ch_idx], color=colors[color_idx])
                plt.axhline(0)
                color_idx += 1

            plt.xlabel('Time (s)')

            plt.ylabel('Power ({})'.format(get_power_unit(
                mne.channel_type(example_tfr.info, ch_idx),
                False
            )))

            plt.show()

        for ax, ch_idx in mne.iter_topography(example_tfr.info, fig_facecolor='white',
                                              axis_spinecolor='white',
                                              axis_facecolor='white', layout=lout,
                                              on_pick=individual_plot):

            for color_idx, tfr in enumerate(data.values()):
                # average over freqs
                tse = np.mean(tfr.data[:, lfreq_idx:hfreq_idx, :], axis=1)
                # correct to baseline
                tse = mne.rescale(tse, times, baseline=baseline)

                ax.plot(tse[ch_idx], linewidth=0.2, color=colors[color_idx])

        plt.gcf().canvas.set_window_title('tse_' + subject_name)
        plt.show()

    elif output == 'channel_averages':
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
                tse = mne.rescale(tse, times, baseline=baseline)

                ax.plot(times, tse, color=colors[color_idx])
                ax.axhline(0)
            ch_type, ch_group = averages[key][0][ii]
            title = 'TSE ({0}, {1})'.format(ch_type, ch_group)
            fig.canvas.set_window_title(title)
            fig.suptitle(title)

        plt.show()


def plot_power_spectrum(experiment, name, output):
    """
    """

    subject = experiment.active_subject
    subject_name = subject.subject_name

    spectrum = subject.spectrums.get(name)

    lout = fileManager.read_layout(experiment.layout)

    data = spectrum.data
    freqs = spectrum.freqs
    ch_names = [ch_name.replace(' ', '') for ch_name in spectrum.ch_names]
    log_transformed = spectrum.log_transformed

    channel_groups = experiment.channel_groups

    raw_info = subject.get_working_file().info

    colors = color_cycle(len(data))

    if output == 'all_channels':
        logging.getLogger('ui_logger').info(
            'Plotting spectrum from all channels..')

        def individual_plot(ax, ch_idx):
            """
            Callback for the interactive plot.
            Opens a channel specific plot.
            """

            # notice that ch_idx is index in the original ch_names,
            # and ch_names from spectrum object are only the data channels
            ch_name = raw_info['ch_names'][ch_idx].replace(' ', '')
            psd_idx = ch_names.index(ch_name)

            fig = plt.gcf()
            fig.canvas.set_window_title(''.join(['spectrum_', subject_name,
                                                 '_', ch_name]))

            conditions = [str(key) for key in data]
            positions = np.arange(0.025, 0.025 + 0.04 * len(conditions), 0.04)

            for cond, col, pos in zip(conditions, colors, positions):
                plt.figtext(0.775, pos, cond, color=col, fontsize=12)

            color_idx = 0
            for psd in data.values():
                plt.plot(freqs, psd[psd_idx], color=colors[color_idx])
                color_idx += 1

            plt.xlabel('Frequency (Hz)')

            plt.ylabel('Power ({})'.format(get_power_unit(
                mne.channel_type(raw_info, ch_idx),
                log_transformed
            )))

            plt.show()

        for ax, idx in mne.iter_topography(raw_info, fig_facecolor='white',
                                           axis_spinecolor='white',
                                           axis_facecolor='white', layout=lout,
                                           on_pick=individual_plot):

            ch_name = raw_info['ch_names'][idx].replace(' ', '')
            if ch_name not in ch_names:
                continue

            psd_idx = ch_names.index(ch_name)

            for color_idx, psd in enumerate(data.values()):
                ax.plot(psd[psd_idx], linewidth=0.2, color=colors[color_idx])

        plt.gcf().canvas.set_window_title('spectrum_' + subject_name)
        plt.show()

    elif output == 'channel_averages':
        logging.getLogger('ui_logger').info(
            'Plotting spectrum channel averages..')

        averages = {}
        for idx, (key, psd) in enumerate(spectrum.data.items()):

            if log_transformed:
                psd = 10 ** (psd / 10.0)

            data_labels, averaged_data = average_data_to_channel_groups(
                psd, ch_names, channel_groups)

            if log_transformed:
                averaged_data = 10 * np.log10(averaged_data)

            averages[key] = data_labels, averaged_data
            shape = averaged_data.shape

        for ii in range(shape[0]):
            fig, ax = plt.subplots()
            for color_idx, key in enumerate(spectrum.data.keys()):
                ax.set_xlabel('Frequency (Hz)')
                ax.set_ylabel('Power ({})'.format(get_power_unit(
                    averages[key][0][ii][0],
                    log_transformed
                )))
                ax.plot(freqs, averages[key][1][ii], color=colors[color_idx])
            ch_type, ch_group = averages[key][0][ii]
            title = 'Spectrum ({0}, {1})'.format(ch_type, ch_group)
            fig.canvas.set_window_title(title)
            fig.suptitle(title)

        plt.show()


def save_data_psd(experiment, subjects, output_rows, spectrum_name):

    logging.getLogger('ui_logger').info('Checking compatibility..')
    freq_lengths = []
    ch_name_lengths = []
    for subject in subjects:
        spectrum = subject.spectrums.get(spectrum_name, None)
        if spectrum is None:
            continue
        freq_lengths.append(len(spectrum.freqs))
        ch_name_lengths.append(len(spectrum.ch_names))

    if len(set(freq_lengths)) > 1:
        raise Exception("Frequencies are not all equal")

    if len(set(ch_name_lengths)) > 1:
        raise Exception("Channels are not all equal")

    if len(subjects) > 1:
        filename = 'group_spectrum_' + spectrum_name + '.csv'
    else:
        filename = (subjects[0].subject_name + '_spectrum_' +
                    spectrum_name + '.csv')

    channel_groups = experiment.channel_groups

    logging.getLogger('ui_logger').info('Saving..')
    path = fileManager.create_timestamped_folder(experiment)
    data = []
    row_names = []

    if len(subjects) == 1: 
        fname_stem = subjects[0].subject_name
    else:
        fname_stem = 'subjects'

    for subject in subjects:
        spectrum = subject.spectrums.get(spectrum_name, None)
        if spectrum is None:
            continue

        freqs = spectrum.freqs
        ch_names = spectrum.ch_names
        info = subject.get_working_file(preload=False).info
        subject_name = subject.subject_name
        log_transformed = spectrum.log_transformed

        for idx, (key, psd) in enumerate(spectrum.data.items()):

            if output_rows == 'channel_averages':

                subject_data = []

                if log_transformed:
                    psd = 10 ** (psd / 10.0)

                data_labels, averaged_data = average_data_to_channel_groups(
                    psd, ch_names, channel_groups)

                if log_transformed:
                    averaged_data = 10 * np.log10(averaged_data)

                subject_data = np.array(averaged_data)

                subject_row_names = []
                for ch_type, sel in data_labels:
                    row_name = ('[' + subject_name + '] ' +
                                '{' + str(key) + '} ' +
                                '(' + ch_type + ') ' + sel)
                    subject_row_names.append(row_name)
            else:
                subject_data = psd

                subject_row_names = []
                for ch_name in ch_names:
                    row_name = ('[' + subject_name + '] ' +
                                '{' + str(key) + '} ' + ch_name)
                    subject_row_names.append(row_name)

            column_names = freqs.tolist()

            row_names.extend(subject_row_names)
            data.extend(subject_data.tolist())

    fileManager.save_csv(os.path.join(path, filename), data,
                         column_names, row_names)


def group_average_psd(experiment, spectrum_name, groups):
    logging.getLogger('ui_logger').info('Calculating group average for psds')

    # check data coherence
    keys = []
    ch_names = []
    freqs = []
    logs = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            subject = experiment.subjects.get(subject_name)
            if not subject:
                continue
            spectrum = subject.spectrums.get(spectrum_name)
            if not spectrum:
                continue
            keys.append(tuple(spectrum.data.keys()))
            ch_names.append(tuple([ch_name.replace(" ", "")
                                   for ch_name in spectrum.ch_names]))
            freqs.append(tuple(spectrum.freqs))
            logs.append(spectrum.log_transformed)

    if len(set(keys)) != 1:
        raise Exception("PSD's contain different conditions")
    if len(set(freqs)) != 1:
        raise Exception("PSD's contain different sets of freqs")
    if len(set(logs)) != 1:
        raise Exception(
            "Some of the PSD's are log transformed and some are not")

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "PSD's contain different sets of channels. Identifying common ones..")
        common_ch_names = list(set.intersection(*map(set, ch_names)))
        logging.getLogger('ui_logger').info(
            str(len(common_ch_names)) + ' common channels found.')
        logging.getLogger('ui_logger').debug(
            'Common channels are ' + str(ch_names))
    else:
        common_ch_names = ch_names[0]

    grand_psds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.subject_name not in group_subjects:
                continue
            spectrums = subject.spectrums.get(spectrum_name)
            if not spectrums:
                continue
            for spectrum_item_key, spectrum_item in spectrums.data.items():
                grand_key = (group_key, spectrum_item_key)

                idxs = []
                # get common channels in "subject specific space"
                for ch_idx, ch_name in enumerate(
                    [ch.replace(' ', '') for ch in spectrums.ch_names]
                ):
                    if ch_name in common_ch_names:
                        idxs.append(ch_idx)

                spectrum_item = spectrum_item[idxs]

                # sanity check
                if spectrum_item.shape[0] != len(common_ch_names):
                    raise Exception('Something wrong with the channels')

                if grand_key in grand_psds:
                    grand_psds[grand_key].append(spectrum_item)
                else:
                    grand_psds[grand_key] = [spectrum_item]

    grand_averages = {}
    for key, grand_psd in grand_psds.items():
        new_key = str(key[1]) + '_group_' + str(key[0])
        if len(grand_psd) == 1:
            grand_averages[new_key] = grand_psd[0].copy()
        else:
            grand_averages[new_key] = np.mean(grand_psd, axis=0)

    active_subject = experiment.active_subject
    spectrum = active_subject.spectrums.get(spectrum_name)

    freqs = spectrum.freqs
    ch_names = common_ch_names
    log_transformed = spectrum.log_transformed

    name = 'group_' + spectrum_name

    spectrum = Spectrum(name, active_subject,
                        log_transformed, grand_averages, freqs, ch_names)

    experiment.active_subject.add_spectrum(spectrum)

    spectrum.save_data()


def create_tfr(experiment, subject, tfr_name, epochs_names,
               freqs, decim, ncycles, subtract_evoked):

    # check that lengths are same
    time_arrays = []
    for name in epochs_names:
        collection = subject.epochs.get(name)
        if collection:
            time_arrays.append(collection.raw.times)

    for ix, i_times in enumerate(time_arrays):
        for jx, j_times in enumerate(time_arrays):
            if ix != jx:
                try:
                    np.testing.assert_array_almost_equal(i_times, j_times)
                except AssertionError:
                    raise Exception('Epochs collections of different time'
                                    'scales are not allowed')

    tfrs = {}
    for epoch_name in epochs_names:
        epochs = subject.epochs[epoch_name].raw
        if subtract_evoked:
            logging.getLogger('ui_logger').info('Subtracting evoked...')
            epochs = epochs.copy().subtract_evoked()

        logging.getLogger('ui_logger').info('Computing TFR...')

        tfr = mne.tfr_morlet(epochs, freqs=freqs, n_cycles=ncycles,
                             decim=decim, average=True,
                             return_itc=False)
        tfr.comment = epoch_name
        tfrs[epoch_name] = tfr

    logging.getLogger('ui_logger').info('Saving TFR...')

    # convert list-like to list
    if hasattr(ncycles, '__len__'):
        ncycles = list(ncycles)

    meggie_tfr = TFR(tfrs, tfr_name, subject, decim, ncycles, subtract_evoked)

    experiment.active_subject.add_tfr(meggie_tfr)

    meggie_tfr.save_tfr()


def plot_tfr(experiment, tfr, name, blmode, blstart, blend,
             output):

    layout = fileManager.read_layout(experiment.layout)

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    logging.getLogger('ui_logger').info("Plotting TFR...")

    if output == 'all_channels':
        fig = tfr.plot_topo(layout=layout, show=False,
                            baseline=bline, mode=mode)

        fig.canvas.set_window_title('TFR' + '_' + name)

        def onclick(event):
            channel = plt.getp(plt.gca(), 'title')
            plt.gcf().canvas.set_window_title('_'.join(['TFR', name,
                                                        channel]))
            plt.show(block=False)

        fig.canvas.mpl_connect('button_press_event', onclick)
        fig.show()
    else:

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
            tfr = mne.AverageTFR(
                info,
                data[np.newaxis, :],
                times,
                freqs,
                1)

            title = labels[1] + ' (' + labels[0] + ')'

            # prevent interaction as no topology is involved now
            def onselect(*args, **kwargs):
                pass

            tfr._onselect = onselect

            tfr.plot(baseline=bline, mode=mode,
                     title=title)


def group_average_tfr(experiment, tfr_name, groups):
    logging.getLogger('ui_logger').info('Calculating group average for tfrs')

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

    experiment.active_subject.add_tfr(meggie_tfr)

    meggie_tfr.save_tfr()
