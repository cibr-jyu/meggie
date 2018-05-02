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

from meggie.ui.utils.decorators import threaded
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.utils.units import get_scaling
from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.utils.units import get_power_unit
from meggie.code_meggie.general.statistic import SpectrumStatistics
from meggie.code_meggie.structures.spectrum import Spectrum


def TFR(experiment, epochs, collection_name, ch_index, freqs, ncycles, decim,
        mode, blstart, blend, save_data, color_map='auto', n_jobs=1):
    """
    Plots a time-frequency representation of the data for a selected
    channel. Modified from example by Alexandre Gramfort.
    """

    baseline = (blstart, blend)
    
    @threaded
    def calculate_tfrs():
        power, itc = mne.tfr_morlet(epochs, freqs=freqs, n_cycles=ncycles, 
                                    decim=decim, n_jobs=n_jobs)
        evoked = epochs.average()
        return power, itc, evoked
        
    power, itc, evoked = calculate_tfrs()
    
    if mode:
        power.data = mne.rescale(power.data, power.times, 
            baseline=baseline, mode=mode)
        itc.data = mne.rescale(itc.data, itc.times, 
            baseline=baseline, mode=mode)          
    
    ch_name = power.ch_names[ch_index]
    
    if save_data:

        subject = experiment.active_subject.subject_name
        path = fileManager.create_timestamped_folder(experiment)
        ch_name = power.ch_names[ch_index]

        power_fname = os.path.join(
            path,
            subject + '_' + ch_name + '_TFR_epochs_induced.csv'
        )

        fileManager.save_tfr(power_fname, power.data[ch_index], power.times, freqs)

        itc_fname = os.path.join(
            path,
            subject + '_' + ch_name + '_TFR_epochs_itc.csv'
        )

        fileManager.save_tfr(itc_fname, itc.data[ch_index], itc.times, freqs)

    evoked_data = evoked.data[ch_index]
    evoked_times = 1e3 * evoked.times

    logging.getLogger('ui_logger').info('Plotting TFR.')
    fig = plt.figure()

    plt.subplot2grid((3, 15), (0, 0), colspan=14)

    ch_type = mne.channel_type(evoked.info, ch_index)

    try:
        plt.ylabel(get_unit(ch_type))
        evoked_data *= get_scaling(ch_type)
    except:
        raise TypeError('TFR plotting for %s channels not supported.' % 
                        ch_type)

    plt.plot(evoked_times, evoked_data)
    plt.title('Evoked response (%s)' % evoked.ch_names[ch_index])
    plt.xlabel('Time (ms)')
    plt.xlim(evoked_times[0], evoked_times[-1])

    if color_map == 'auto':
        cmap = 'RdBu_r'
    else:
        cmap = color_map    

    data = power.data[ch_index]

    plt.subplot2grid((3, 15), (1, 0), colspan=14)
    img = plt.imshow(data, extent=[evoked_times[0], evoked_times[-1],
        freqs[0], freqs[-1]], aspect='auto', origin='lower', cmap=cmap)
    plt.xlabel('Time (ms)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Induced power (%s)' % evoked.ch_names[ch_index])
    plt.colorbar(cax=plt.subplot2grid((3, 15), (1, 14)), mappable=img)

    data = itc.data[ch_index]
        
    plt.subplot2grid((3, 15), (2, 0), colspan=14)
    img = plt.imshow(data, extent=[evoked_times[0], evoked_times[-1],
        freqs[0], freqs[-1]], aspect='auto', origin='lower', cmap=cmap)
    plt.xlabel('Time (ms)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Phase-lock (%s)' % evoked.ch_names[ch_index])
    plt.colorbar(cax=plt.subplot2grid((3, 15), (2, 14)), mappable=img)

    plt.tight_layout()
    fig.canvas.set_window_title('_'.join(['TFR', collection_name,
                                          ch_name]))
    fig.show()


def TFR_topology(experiment, inst, collection_name, reptype, freqs, decim, mode, 
                 blstart, blend, ncycles, ch_type, scalp, color_map='auto',
                 save_data=False, n_jobs=1):
    """
    Plots time-frequency representations on topographies for MEG sensors.
    Modified from example by Alexandre Gramfort and Denis Engemann.
    Keyword arguments:
    inst            -- Epochs extracted from the data or previously computed
                       AverageTFR object to plot.
    collection_name -- Name of the epoch collection.
    reptype         -- Type of representation (average or itc).
    freqs           -- Frequencies for the representation as a numpy array.
    decim           -- Temporal decimation factor.
    mode            -- Rescaling mode (logratio | ratio | zscore |
                       mean | percent).
    blstart         -- Starting point for baseline correction.
    blend           -- Ending point for baseline correction.
    ncycles         -- Value used to count the number of cycles.
    ch_type         -- Channel type (mag | grad | eeg).
    scalp           -- Parameter dictionary for scalp plot. If None, no scalp
                       plot is drawn.
    color_map       -- Matplotlib color map to use. Defaults to ``auto``, in
                       which case ``RdBu_r`` is used or ``Reds`` if only
                       positive values exist in the data.
    save_data       -- save data to file or not
    """

    @threaded
    def calculate_tfrs():
        power, itc = mne.tfr_morlet(inst, freqs=freqs, n_cycles=ncycles, 
                                    decim=decim, n_jobs=n_jobs)
        return power, itc
    
    power, itc = calculate_tfrs()
    baseline = (blstart, blend)
    layout = fileManager.read_layout(experiment.layout)
            
    if reptype == 'average':
        inst = power
        title = 'Average power'
    elif reptype == 'itc':
        inst = itc
        title = 'Inter-trial coherence'
        
    if color_map == 'auto':
        cmap = 'RdBu_r'
    else:
        cmap = color_map

    if mode:
        inst.data = mne.rescale(inst.data, inst.times, 
            baseline=baseline, mode=mode)    

    if save_data:
        subject = experiment.active_subject.subject_name
        path = fileManager.create_timestamped_folder(experiment)

        fname = os.path.join(
            path,
            subject + '_TFR_epochs_allchannels.csv'
        )

        labels = []
        for ch_name in inst.info['ch_names']:
            if ch_name in inst.info['bads']:
                ch_name += ' (bad)'
            labels.append(ch_name)

        logging.getLogger('ui_logger').info("Saving data..")
        fileManager.save_tfr_topology(fname, inst.data, 
                            inst.times, freqs, labels)
        

    if scalp is not None:
        inst.plot_topomap(tmin=scalp['tmin'], tmax=scalp['tmax'],
                          fmin=scalp['fmin'], fmax=scalp['fmax'],
                          ch_type=ch_type, layout=layout,
                          show=False, cmap=cmap)

    logging.getLogger('ui_logger').info("Plotting.")
    fig = inst.plot_topo(fmin=freqs[0], fmax=freqs[-1], layout=layout, 
        cmap=cmap, title=title)

    fig.canvas.set_window_title('TFR' + '_' + collection_name)
    fig.show()

    def onclick(event):
        channel = plt.getp(plt.gca(), 'title')
        plt.gcf().canvas.set_window_title('_'.join(['TFR', collection_name,
                                                    channel]))
        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)



@threaded
def _compute_spectrum(epoch_groups, params, n_jobs):
    """Performed in a worker thread."""
    fmin = params['fmin']
    fmax = params['fmax']
    nfft = params['nfft']
    overlap = params['overlap']
    picks = params['picks']

    psd_groups = OrderedDict()
    
    for key, epochs in epoch_groups.items():
        for epoch in epochs:

            epoch.load_data()
            length = epoch._data.shape[-1]
            
            psds, freqs = mne.psd_welch(epoch, fmin=fmin, fmax=fmax, 
                n_fft=nfft, n_overlap=overlap, picks=picks, 
                proj=True, n_jobs=n_jobs)

            psds = np.average(psds, axis=0)

            if params['log']:
                psds = 10 * np.log10(psds)
            
            if key not in psd_groups:
                psd_groups[key] = []

            psd_groups[key].append((psds, freqs, length))

    return psd_groups


def create_power_spectrum(experiment, spectrum_name, params, epoch_groups, 
                          update_ui=(lambda: None), n_jobs=1):
    """
    """
        
    for epochs in epoch_groups.values():
        info = epochs[0].info
        break
        
    picks = mne.pick_types(info, meg=True, eeg=True,
                           exclude=[])

    params['picks'] = picks
    psd_groups = _compute_spectrum(epoch_groups, params, n_jobs=n_jobs,
                                   do_meanwhile=update_ui)

    for psd_list in psd_groups.values():
        freqs = psd_list[0][1]
        break
    
    psds = []
    for psd_list in psd_groups.values():
        # do a weighted (epoch lengths as weights) average of psds inside a group

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


def plot_power_spectrum(experiment, name):
    """
    """

    lout = fileManager.read_layout(experiment.layout)

    subject = experiment.active_subject
    subject_name = subject.subject_name

    spectrum = subject.spectrums.get(name)

    data = spectrum.data
    freqs = spectrum.freqs
    ch_names = spectrum.ch_names
    log_transformed = spectrum.log_transformed

    raw_info = subject.get_working_file().info

    colors = color_cycle(len(data))

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

        psd_idx = ch_names.index(raw_info['ch_names'][idx])
        
        for color_idx, psd in enumerate(data.values()):
            ax.plot(psd[psd_idx], linewidth=0.2, color=colors[color_idx])

    plt.gcf().canvas.set_window_title('spectrum_' + subject_name)
    plt.show()


def save_data_psd(experiment, subjects, output_rows, 
                  output_columns, spectrum_name):

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

                selections = mne.SELECTIONS
                for selection in selections:
                    # find channels names for selection provided by mne
                    selected_ch_names = mne._clean_names(
                        mne.read_selection(selection),
                        remove_whitespace=True)

                    cleaned_ch_names = mne._clean_names(ch_names,
                        remove_whitespace=True)

                    # calculate average
                    ch_average = np.mean(
                        [psd[ch_idx] for ch_idx, ch_name 
                         in enumerate(cleaned_ch_names)
                         if ch_name in selected_ch_names
                         and ch_name not in info['bads']], axis=0)

                    subject_data.append(ch_average)

                subject_data = np.array(subject_data)

                subject_row_names = []
                for sel in selections:
                    row_name = ('[' + subject_name + '] ' + 
                                '{' + str(key) + '} ' + sel)
                    subject_row_names.append(row_name)

            else:
                subject_data = psd

                subject_row_names = []
                for ch_name in ch_names:
                    row_name = ('[' + subject_name + '] ' + 
                                '{' + str(key) + '} ' + ch_name)
                    subject_row_names.append(row_name)

            if output_columns == 'statistics':
                statistics = SpectrumStatistics(
                    freqs, subject_data, log_transformed)

                alpha_peak = statistics.alpha_peak
                alpha_frequency = statistics.alpha_frequency
                alpha_power = statistics.alpha_power

                filename = ''.join([subject_name, '_', 
                                    'spectrum_statistics.csv'])

                column_names = ['Alpha amplitude', 'Alpha frequency', 'Alpha power']
                subject_data = np.transpose(
                    np.array([alpha_peak, alpha_frequency, alpha_power]))

            else:
                filename = ''.join([subject_name, '_', 'spectrum.csv'])
                column_names = freqs.tolist()

            row_names.extend(subject_row_names)
            data.extend(subject_data.tolist())

    fileManager.save_csv(os.path.join(path, filename), data, 
                         column_names, row_names)


def group_average_psd(experiment, spectrum_name):
    logging.getLogger('ui_logger').info('Calculating group average for psds') 


def create_tfr(experiment, subject, tfr_name, epochs_name, 
               freqs, decim, ncycles, n_jobs):

    epochs = subject.epochs[epochs_name].raw

    tfr = mne.tfr_morlet(epochs, freqs=freqs, n_cycles=ncycles, decim=decim,
                         average=False, return_itc=False, n_jobs=n_jobs)

    meggie_tfr = TFR(tfr, tfr_name, subject, decim=decim, n_cycles)

    experiment.active_subject.add_tfr(meggie_tfr) 

    meggie_tfr.save_data()

