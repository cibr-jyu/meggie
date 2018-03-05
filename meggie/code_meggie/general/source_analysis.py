# coding: utf-8
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen, Erkka Heinilä
"""

import subprocess
import logging
import functools
import os

import numpy as np
import matplotlib.pyplot as plt

import meggie.code_meggie.general.mne_wrapper as mne

import meggie.code_meggie.general.fileManager as fileManager


def create_linear_source_estimate(subject, operator_name, based_on, loose, depth):
    """
    """
    fwd_path = os.path.join(subject.forward_solutions_directory, based_on)
    fwd = mne.read_forward_solution(fwd_path)

    cov_path = subject.covfile_path
    cov = mne.read_cov(cov_path)

    info = subject.get_working_file(preload=False).info

    logging.getLogger('ui_logger').info('Creating inverse operator...')
    inv = mne.make_inverse_operator(info, fwd, cov, loose=loose, depth=depth)
    
    # save the file
    # fname = operator_name + '-inv.fif'
    # path = os.path.join(subject.inverse_operators_directory, fname)
    # mne.write_inverse_operator(path, inv)


def create_forward_solution(subject, solution_name, decim, triang_ico, conductivity):
    """
    """

    subject_name = 'reconFiles'
    subjects_dir = subject.source_analysis_directory

    # set up source space
    src = mne.setup_source_space(subject=subject_name, spacing=decim,
        subjects_dir=subjects_dir)

    # set up bem solution
    model = mne.make_bem_model(subject=subject_name, ico=triang_ico,
			       conductivity=conductivity,
			       subjects_dir=subjects_dir)
    bem = mne.make_bem_solution(model)

    # gather parameters
    trans = subject.transfile_path
    info = subject.get_working_file().info
    meg = True
    eeg = True if len(conductivity) == 3 else False
    
    # make forward solution
    fwd = mne.make_forward_solution(info, trans=trans, src=src, bem=bem,
        meg=meg, eeg=eeg, mindist=5.0)

    # save the file
    fname = solution_name + '-' + decim + '-src-fwd.fif'
    path = os.path.join(subject.forward_solutions_directory, fname)
    mne.write_forward_solution(path, fwd)


def make_source_estimate(self, inst_name, type, inv_name, method, lmbd):
    """
    Method for computing source estimate.
    Args:
        inst_name: Name of the data instance.
        type: str to indicate type of data.
            One of ['raw', 'epochs', 'evoked'].
        inv_name: Name of the inverse operator.
        method: Method to use ('MNE', 'dSPM', 'sLORETA').
        lmbd: Regularization parameter.
    """
    # TODO: refactor
    subject = self.experiment.active_subject
    source_dir = subject._source_analysis_directory
    inv_file = os.path.join(source_dir, inv_name)

    try:
        inv = mne.minimum_norm.read_inverse_operator(inv_file)
    except Exception as err:
        raise Exception('Error while reading inverse '
                        'operator:\n' + str(err))
    if type == 'raw':
        inst = subject.get_working_file()
        try:
            stc = mne.minimum_norm.apply_inverse_raw(inst, inv,
                                                     lambda2=lmbd,
                                                     method=method)
        except Exception as err:
            raise Exception('Exception while computing inverse '
                            'solution:\n' + str(err))
    elif type == 'epochs':
        inst = subject.epochs[inst_name].raw
        try:
            stc = mne.minimum_norm.apply_inverse_epochs(inst, inv,
                                                        lambda2=lmbd,
                                                        method=method)
        except Exception as err:
            raise Exception('Exception while computing inverse '
                            'solution:\n' + str(err))
    elif type == 'evoked':
        evoked = subject.evokeds[inst_name]
        stc = list()

        for mne_evoked in evoked.mne_evokeds.values():
            try:
                stc.append(mne.minimum_norm.apply_inverse(mne_evoked, inv,
                    lambda2=lmbd, method=method))
            except Exception as err:
                raise Exception('Exception while computing inverse '
                                'solution:\n' + str(err))

    stc_fname = os.path.split(inv_file)[-1]
    if isinstance(stc, list):  # epochs and evoked saved individually
        if type == 'epochs':
            stc_path = os.path.join(subject._stc_directory,
                                    stc_fname[:-8] + '-' + type + '-' +
                                    method)
            os.mkdir(stc_path)
        for i, estimate in enumerate(stc):
            if type == 'epochs':
                stc_fname = os.path.join(stc_path, 'epoch-' + str(i))
            else:
                stc_fname = os.path.join(subject._stc_directory,
                                         stc_fname[:-8] + '-' + type +
                                         '-' + method + str(i))
            try:
                estimate.save(stc_fname)
            except Exception as err:
                raise Exception('Exception while saving inverse '
                                'solution:\n' + str(err))
        message = 'Inverse solution computed successfully.'
        logging.getLogger('ui_logger').info(message)
        return stc

    stc_fname = os.path.join(subject._stc_directory,
                             stc_fname[:-8] + '-' + type + '-' + method)
    try:
        stc.save(stc_fname)
    except Exception as err:
        raise Exception('Exception while saving inverse '
                        'solution:\n' + str(err))
    message = 'Inverse solution computed successfully.'
    logging.getLogger('ui_logger').info(message)
    return stc

def plotStc(self, stc_name, hemi, surface, smoothing_steps, alpha):
    """Method for plotting source estimate.
    Args:
        stc: Stc name.
        hemi: Hemisphere 'lh', 'rh' or 'both'.
        surface: Type of surface.
        smoothing_steps: The amount of smoothing.
        alpha: Alpha value to use.
    """
    subject = self.experiment.active_subject
    stc_dir = subject._stc_directory
    fname = os.path.join(stc_dir, stc_name)
    stc = mne.read_source_estimate(fname)
    try:
        stc.plot(subject='', surface=surface, hemi=hemi, alpha=alpha,
                 smoothing_steps=smoothing_steps, time_viewer=True,
                 subjects_dir=subject.reconfiles_directory)
    except Exception as e:
        raise Exception('Error while plotting source estimate:\n' + str(e))

def tfr_clicked(self, event, data, stc, freqs):
    """
    Callback function for plotting frequencies in source space.
    Args:
        event: Mpl event.
        data: Power in shape (sources, times).
        stc: Instance of SourceEstimate. Used for wrapping the freq data.
        freqs: List of float. Frequencies of interest.
    """
    x_data = event.xdata
    y_data = event.ydata
    ax = event.inaxes
    ax.text(0.5, 0.5, 'Loading...')
    ax.get_figure().canvas.draw()
    #time_idx = np.argmin([abs(x_data / 1000. - t) for t in stc.times])
    freq_idx = np.argmin([abs(y_data - f) for f in freqs])
    stc._data = data[:, freq_idx, :]
    subjects_dir = self.experiment.active_subject.reconfiles_directory
    label = str(freqs[freq_idx]) + ' Hz, time=%0.2f ms'
    stc.plot(subject='', subjects_dir=subjects_dir, time_label=label,
             time_viewer=True)

def plot_stc_freq(self, stc, data, freqs, tmin, tmax, ncycles):
    """
    Computes morlet tfr over set of stcs over epochs. Operates on stc
    instance in place.
    Args:
        stc: Instance of stc containing the info. Used as a wrapper when
            plotting the frequencies in source space. Modified in place.
        data: Data in shape (epochs, sources, times).
        freqs: List of float. Frequencies of interest.
        tmin: Float. Minimum time of interest.
        tmax: Float. Maximum time of interest.
        ncycles: Float or list of float. Number of cycles for the wavelet.

    Returns: Instance of figure.
    Matplotlib figure containing average TFR over the epoch stcs.

    """

    n_jobs = self.parent.preferencesHandler.n_jobs
    tmin_i = np.argmin([abs(tmin - t) for t in stc.times])
    tmax_i = np.argmin([abs(tmax - t) for t in stc.times])
    data = np.array(data)[:, :, tmin_i:tmax_i]
    power, _ = mne.time_frequency.tfr._induced_power_cwt(data,
        sfreq=stc.sfreq, frequencies=freqs, n_cycles=ncycles, n_jobs=n_jobs)

    fig, ax = plt.subplots(1, 1)
    ax.imshow(np.mean(power, axis=0),
              extent=(stc.times[tmin_i], stc.times[tmax_i], freqs[0],
                      freqs[-1]), aspect="auto", origin="lower")
    

    stc.times = stc.times[tmin_i:tmax_i]
    click_callback = functools.partial(self.tfr_clicked, data=power, stc=stc,
                                       freqs=freqs)
    fig.canvas.mpl_connect('button_press_event', click_callback)
    fig.suptitle('Average power over all sources.')
    plt.show(block=True)
    return fig

