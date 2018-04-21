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


def TFR_raw(experiment, wsize, tstep, channel, fmin, fmax, blstart, blend, mode,
            save_data):
    lout = fileManager.read_layout(experiment.layout)
    
    raw = experiment.active_subject.get_working_file()
    
    raw = raw.copy()
    raw.apply_proj()
    
    tfr = np.abs(mne.stft(raw._data, wsize, tstep=tstep))
    freqs = mne.stftfreq(wsize, sfreq=raw.info['sfreq'])
    times = np.arange(tfr.shape[2]) * tstep / raw.info['sfreq']
    baseline = (blstart, blend)
    
    tfr_ = mne.AverageTFR(raw.info, tfr, times, freqs, 1)
    
    if mode:
        tfr_.data = mne.rescale(tfr_.data, times, baseline=baseline, 
                                         mode=mode)
    
    fig = tfr_.plot(picks=[channel], fmin=fmin, fmax=fmax, layout=lout)
    subject_name = experiment.active_subject.subject_name
    fig.canvas.set_window_title(''.join(['TFR_raw_', subject_name, '_',
                                raw.ch_names[channel]]))
    
    if save_data:
        path = fileManager.create_timestamped_folder(experiment)
        filename = os.path.join(path, ''.join([
            experiment.active_subject.subject_name, '_',
            raw.ch_names[channel], '_TFR.csv']))
        fileManager.save_tfr(filename, tfr[channel], times, freqs)

def plot_power_spectrum_old(experiment, params, save_data, epoch_groups, 
                            basename='raw', update_ui=(lambda: None), n_jobs=1,
                            output_rows='all_channels', output_columns='all_data'):
    """
    Method for plotting power spectrum.
    Parameters:
    params         - Dictionary containing the parameters.
    save_data      - Boolean indicating whether to save psd data to files.
                     Only data from channels of interest is saved.
    """
    lout = fileManager.read_layout(experiment.layout)
        
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
        
    colors = color_cycle(len(psds))

    subject_name = experiment.active_subject.subject_name

    # find all channel names this way because earlier
    # the dimension of channels was reduced with picks
    picked_ch_names = [ch_name for ch_idx, ch_name in 
                    enumerate(info['ch_names']) if 
                    ch_idx in picks]
    ch_names = info['ch_names']

    if save_data:
        logging.getLogger('ui_logger').info("Saving data...")
        path = fileManager.create_timestamped_folder(experiment)

        for idx, psd in enumerate(psds):

            if output_rows == 'channel_averages':

                data = []

                selections = mne.SELECTIONS
                for selection in selections:
                    # find channels names for selection provided by mne
                    selected_ch_names = mne._clean_names(
                        mne.read_selection(selection),
                        remove_whitespace=True)

                    cleaned_picked_ch_names = mne._clean_names(picked_ch_names,
                        remove_whitespace=True)

                    # calculate average
                    ch_average = np.mean(
                        [psd[ch_idx] for ch_idx, ch_name 
                         in enumerate(cleaned_picked_ch_names)
                         if ch_name in selected_ch_names], axis=0)

                    data.append(ch_average)

                data = np.array(data)
                row_names = selections

            else:

                data = psd
                row_names = picked_ch_names

                for row_idx in range(len(row_names)):
                    if picked_ch_names[row_idx] in info['bads']:
                        row_names[row_idx] += ' (bad)'

            if output_columns == 'statistics':
                statistics = SpectrumStatistics(freqs, data, params['log'])

                alpha_peak = statistics.alpha_peak
                alpha_frequency = statistics.alpha_frequency
                alpha_power = statistics.alpha_power

                filename = ''.join([subject_name, '_', basename, '_',
                                    'spectrum_statistics', '_', 
                                    str(psd_groups.keys()[idx]), '.csv'])

                column_names = ['Alpha amplitude', 'Alpha frequency', 'Alpha power']
                data = np.array([alpha_peak, alpha_frequency, alpha_power])
                data = np.transpose(data)

            else:
                filename = ''.join([subject_name, '_', basename, '_',
                    'spectrum', '_', str(psd_groups.keys()[idx]), '.csv'])
                column_names = freqs.tolist()

            fileManager.save_csv(os.path.join(path, filename), data.tolist(), 
                                 column_names, row_names)

    logging.getLogger('ui_logger').info("Plotting power spectrum...")

    def individual_plot(ax, ch_idx):
        """
        Callback for the interactive plot.
        Opens a channel specific plot.
        """

        ch_name = ch_names[ch_idx]
        psd_idx = picked_ch_names.index(ch_name)
        
        fig = plt.gcf()
        fig.canvas.set_window_title(''.join(['Spectrum_', subject_name,
                                    '_', ch_name]))
        
        conditions = [str(key) for key in psd_groups]
        positions = np.arange(0.025, 0.025 + 0.04 * len(conditions), 0.04)
        
        for cond, col, pos in zip(conditions, colors, positions):
            plt.figtext(0.775, pos, cond, color=col, fontsize=12)

        color_idx = 0
        for psd in psds:
            plt.plot(freqs, psd[psd_idx], color=colors[color_idx])
            color_idx += 1
        
        plt.xlabel('Frequency (Hz)')

        plt.ylabel('Power ({})'.format(get_power_unit(
            mne.channel_type(info, ch_idx),
            params['log'] 
        )))

        plt.show()

    for ax, idx in mne.iter_topography(info, fig_facecolor='white',
                                       axis_spinecolor='white',
                                       axis_facecolor='white', layout=lout,
                                       on_pick=individual_plot):

        ch_name = ch_names[idx]
        psd_idx = picked_ch_names.index(ch_name)
        
        color_idx = 0
        for psd in psds:
            ax.plot(psd[psd_idx], linewidth=0.2, color=colors[color_idx])
            color_idx += 1

    plt.gcf().canvas.set_window_title('Spectrum_' + subject_name)
    plt.show()

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
    lout = fileManager.read_layout(experiment.layout)
        
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
            psd_data, freqs, picked_ch_names)

    experiment.active_subject.add_spectrum(spectrum) 

    spectrum.save_data()


def plot_power_spectrum():
    pass

def save_data_psd():
    pass

def group_average_psd():
    pass

