# coding: utf-8
"""
"""

import os
import logging

from copy import deepcopy

from collections import OrderedDict

import numpy as np
import matplotlib.pyplot as plt

import meggie.code_meggie.general.mne_wrapper as mne

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
def _compute_spectrum(raw_block_groups, params, n_jobs):
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
                proj=True, n_jobs=n_jobs)

            if params['log']:
                psds = 10 * np.log10(psds)
            
            if key not in psd_groups:
                psd_groups[key] = []

            psd_groups[key].append((psds, freqs, length))

    return psd_groups


def create_power_spectrum(experiment, spectrum_name, params, raw_block_groups, 
                          update_ui=(lambda: None), n_jobs=1):
    """
    """
        
    for raw_blocks in raw_block_groups.values():
        info = raw_blocks[0].info
        break

    picks = mne.pick_types(info, meg=True, eeg=True,
                           exclude='bads')

    params['picks'] = picks
    psd_groups = _compute_spectrum(raw_block_groups, params, n_jobs=n_jobs,
                                   do_meanwhile=update_ui)

    for psd_list in psd_groups.values():
        freqs = psd_list[0][1]
        break
    
    psds = []
    for psd_list in psd_groups.values():
        # do a weighted (raw block lengths as weights) average of psds inside a group

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


def plot_power_spectrum(experiment, name, output):
    """
    """

    subject = experiment.active_subject
    subject_name = subject.subject_name

    spectrum = subject.spectrums.get(name)

    lout = fileManager.read_layout(experiment.layout)

    data = spectrum.data
    freqs = spectrum.freqs
    ch_names = spectrum.ch_names
    log_transformed = spectrum.log_transformed

    channel_groups = experiment.channel_groups

    raw_info = subject.get_working_file().info

    colors = color_cycle(len(data))

    if output == 'all_channels':
        logging.getLogger('ui_logger').info('Plotting spectrum from all channels..')

        def individual_plot(ax, ch_idx):
            """
            Callback for the interactive plot.
            Opens a channel specific plot.
            """

            # notice that ch_idx is index in the original ch_names,
            # and ch_names from spectrum object are only the data channels
            ch_name = raw_info['ch_names'][ch_idx]
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

            if raw_info['ch_names'][idx] not in ch_names:
                continue

            psd_idx = ch_names.index(raw_info['ch_names'][idx])
            
            for color_idx, psd in enumerate(data.values()):
                ax.plot(psd[psd_idx], linewidth=0.2, color=colors[color_idx])

        plt.gcf().canvas.set_window_title('spectrum_' + subject_name)
        plt.show()

    elif output == 'channel_averages':
        logging.getLogger('ui_logger').info('Plotting spectrum channel averages..')


        averages = {}
        for idx, (key, psd) in enumerate(spectrum.data.items()):

            data_labels, averaged_data = average_data_to_channel_groups(
                psd, ch_names, channel_groups, type_='mean')
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


    channel_groups = experiment.channel_groups

    logging.getLogger('ui_logger').info('Saving..')
    path = fileManager.create_timestamped_folder(experiment)
    data = []
    row_names = []


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

                data_labels, averaged_data = average_data_to_channel_groups(
                    psd, ch_names, channel_groups, type_='mean')

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
            
            filename = ''.join([subject_name, '_', 'spectrum.csv'])
            column_names = freqs.tolist()

            row_names.extend(subject_row_names)
            data.extend(subject_data.tolist())

    fileManager.save_csv(os.path.join(path, filename), data, 
                         column_names, row_names)

def group_average_psd(experiment, spectrum_name):
    logging.getLogger('ui_logger').info('Calculating group average for psds') 

    # check data coherence
    keys = []
    ch_names = []
    freqs = []
    logs = []
    for subject in experiment.subjects.values():
        spectrum = subject.spectrums.get(spectrum_name)
        if not spectrum:
            continue
        keys.append(tuple(spectrum.data.keys()))
        ch_names.append(tuple(spectrum.ch_names))
        freqs.append(tuple(spectrum.freqs))
        logs.append(spectrum.log_transformed)

    if len(set(keys)) != 1:
        raise Exception("PSD's contain different conditions")
    if len(set(ch_names)) != 1:
        raise Exception("PSD's contain different sets of channels")
    if len(set(freqs)) != 1:
        raise Exception("PSD's contain different sets of freqs")
    if len(set(logs)) != 1:
        raise Exception("Some of the PSD's are log transformed and some are not")

    data = dict([(key, []) for key in keys[0]])
    for subject in experiment.subjects.values():
        spectrum = subject.spectrums.get(spectrum_name)
        if not spectrum:
            continue

        for key, cond_data in spectrum.data.items():
            data[key].append(cond_data)

    for key in data:
        data[key] = np.mean(data[key], axis=0)

    freqs = spectrum.freqs
    ch_names = spectrum.ch_names
    name = 'group_' + spectrum_name

    spectrum = Spectrum(name, experiment.active_subject,
            logs[0], data, freqs, ch_names)

    experiment.active_subject.add_spectrum(spectrum) 

    spectrum.save_data()


def create_tfr(experiment, subject, tfr_name, epochs_name, 
               freqs, decim, ncycles, subtract_evoked, n_jobs):

    epochs = subject.epochs[epochs_name].raw

    if subtract_evoked:
        logging.getLogger('ui_logger').info('Subtracting evoked...')
        epochs = epochs.copy().subtract_evoked()

    logging.getLogger('ui_logger').info('Computing TFR...')

    tfr = mne.tfr_morlet(epochs, freqs=freqs, n_cycles=ncycles, decim=decim,
                         average=True, return_itc=False, n_jobs=n_jobs)

    logging.getLogger('ui_logger').info('Saving TFR...')

    # convert list-like to list
    if hasattr(ncycles, '__len__'):
        ncycles = list(ncycles)

    meggie_tfr = TFR(tfr, tfr_name, subject, decim, ncycles, subtract_evoked)

    experiment.active_subject.add_tfr(meggie_tfr) 

    meggie_tfr.save_tfr()


def plot_tfr_topology(experiment, tfr, name, blmode, blstart, blend):

    layout = fileManager.read_layout(experiment.layout)

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    logging.getLogger('ui_logger').info("Plotting TFR topology...")
    fig = tfr.plot_topo(layout=layout, show=False, baseline=bline, mode=mode)

    fig.canvas.set_window_title('TFR' + '_' + name)

    def onclick(event):
        channel = plt.getp(plt.gca(), 'title')
        plt.gcf().canvas.set_window_title('_'.join(['TFR', name,
                                                    channel]))
        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.show()


def group_average_tfr(experiment, tfr_name):
    logging.getLogger('ui_logger').info('Calculating group average for tfrs') 

    # check data coherence
    freqs = []
    times = []
    ch_names = []
    decims = []
    subtracts = []

    for subject in experiment.subjects.values():
        tfr = subject.tfrs.get(tfr_name)
        if not tfr:
            continue
        freqs.append(tuple(tfr.tfr.freqs))
        times.append(tuple(tfr.tfr.times))
        ch_names.append(tuple(tfr.tfr.info['ch_names']))
        decims.append(tfr.decim)
        subtracts.append(tfr.evoked_subtracted)

    if len(set(freqs)) != 1:
        raise Exception("TFR's contain different sets of freqs")
    if len(set(ch_names)) != 1:
        raise Exception("TFR's contain different sets of channels")
    if len(set(times)) != 1:
        raise Exception("TFR's contain different sets of times")
    if len(set(decims)) != 1:
        raise Exception("TFR's contain different sets of decims")
    if len(set(subtracts)) != 1:
        raise Exception("TFR's contain different evoked subtraction settings")

    tfrs = []
    for subject in experiment.subjects.values():
        tfr = subject.tfrs.get(tfr_name)
        if not tfr:
            continue
        tfrs.append(tfr.tfr)

    if len(tfrs) < 2:
        raise Exception('No other subject with a corresponding TFR found')

    average_tfr = mne.grand_average(tfrs, drop_bads=False)
    decim = tfr.decim
    n_cycles = tfr.n_cycles
    evoked_subtracted = tfr.evoked_subtracted

    meggie_tfr = TFR(average_tfr, 'group_' + tfr_name, 
                     experiment.active_subject, 
                     decim, n_cycles, evoked_subtracted)

    experiment.active_subject.add_tfr(meggie_tfr)

    meggie_tfr.save_tfr()

