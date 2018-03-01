# coding: utf-8
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen, Erkka Heinilä
This module contains caller class that contains the main state of the software
"""

import subprocess
import logging
import functools
import os

import numpy as np
import matplotlib.pyplot as plt

import meggie.code_meggie.general.fileManager as fileManager


def create_forward_solution(subject, solution_name, decim, triang_ico, conductivity):
    pass


def convert_mri_to_mne(active_subject):
    """
    Uses mne_setup_mri to active subject recon directory to create Neuromag
    slices and sets (to be input later to do_forward_solution).
    
    Return True if creation successful, False if there was an error. 
    """
    sourceAnalDir = active_subject.source_analysis_directory
    
    # Hack the SUBJECT_DIR and SUBJECT variables to right location 
    # (mne_setup_mri searches for reconstructed files from mri directory
    # under the SUBJECT)
    os.environ['SUBJECTS_DIR'] = sourceAnalDir
    os.environ['SUBJECT'] = 'reconFiles'
    
    subprocess.check_output("$MNE_ROOT/bin/mne_setup_mri", shell=True)


def compute_inverse(self, fwd_name):
    """Computes an inverse operator for the forward solution and saves it
    to the source_analysis directory.
    Keyword arguments:
        fwd: The forward operator name.

    Returns:
        The inverse operator
    """
    subject = self.experiment.active_subject
    info = subject.get_working_file().info
    sa_dir = subject._source_analysis_directory
    fwd_file = os.path.join(subject._forwardModels_directory, fwd_name,
                            'reconFiles', 'reconFiles-fwd.fif')
    if os.path.isfile(fwd_file):
        logging.getLogger('ui_logger').info('Reading forward solution...')
    else:
        raise IOError('Could not find forward solution with name %s.' %
                      fwd_file)
    fwd = mne.read_forward_solution(fwd_file)
    cov = subject.get_cov()
    inv = mne.minimum_norm.make_inverse_operator(info, fwd, cov)
    inv_fname = os.path.join(sa_dir, subject.subject_name + '-inv.fif')
    try:
        mne.minimum_norm.write_inverse_operator(inv_fname, inv)
    except Exception as e:
        msg = ('Exception while computing inverse operator:\n\n' + str(e))
        raise Exception(msg)
    return inv

def create_covariance_from_raw(self, cvdict):
    """
    Computes a covariance matrix based on raw file and saves it to the
    approriate location under the subject.

    Keyword arguments:

    cvdict        -- dictionary containing parameters for covariance
                     computation
    """
    subject_name = cvdict['rawsubjectname']
    if subject_name is not None:
        subject = self.experiment.subjects[subject_name]
        raw = subject.get_working_file()
        name = os.path.basename(subject.working_file_name)
        filename_to_write = name[:-4] + '-cov.fif'
    else:
        raw = fileManager.open_raw(cvdict['rawfilepath'], True)
        basename = os.path.basename(cvdict['rawfilepath'])[0]
        filename_to_write = os.path.splitext(basename)[:-4] + '-cov.fif'

    tmin = cvdict['starttime']
    tmax = cvdict['endtime']
    tstep = cvdict['tstep']

    reject = cvdict['reject']
    flat = cvdict['flat']
    picks = cvdict['picks']

    try:
        cov = mne.cov.compute_raw_covariance(raw, tmin, tmax, tstep,
                                             reject, flat, picks)
    except ValueError as e:
        raise ValueError('Error while computing covariance. ' + str(e))

    self._save_covariance(cov, cvdict, filename_to_write)

def create_covariance_from_epochs(self, params):
    subject = self.experiment.active_subject
    collection_names = params['collection_names']
    epochs = []
    filename_to_write = ''

    for collection_name in collection_names:
        epoch = subject.epochs.get(collection_name)
        epochs.append(epoch.raw)
        filename_to_write += os.path.splitext(collection_name)[0] + '-'
    
    filename_to_write = filename_to_write[:len(filename_to_write)-1] + '-cov.fif'
    tmin = params['tmin']
    tmax = params['tmax']
    keep_sample_mean = params['keep_sample_mean']
    method = params['method']
    n_jobs = self.parent.preferencesHandler.n_jobs
    
    try:
        cov = mne.compute_covariance(epochs,
            keep_sample_mean=keep_sample_mean, tmin=tmin, tmax=tmax,
            method=method, n_jobs=n_jobs)            
    except ValueError as e:
        raise ValueError('Error while computing covariance. ' + str(e))
    
    self._save_covariance(cov, params, filename_to_write)
    
def _save_covariance(self, cov, params, filename_to_write):
    
    path = self.experiment.active_subject._source_analysis_directory

    # Remove previous covariance file before creating a new one.
    fileManager.remove_files_with_regex(path, '.*-cov.fif')

    filepath_to_write = os.path.join(path, filename_to_write)
    try:
        mne.write_cov(filepath_to_write, cov)
    except IOError as err:
        err.message = ('Could not write covariance file. The error '
                       'message was: \n\n' + err.message)
        raise

    # Delete previous and write a new parameter file.
    try:
        fileManager.remove_files_with_regex(path, 'covariance.param')
        cvparamFile = os.path.join(path, 'covariance.param')
        fileManager.pickleObjectToFile(params, cvparamFile)

    except Exception:
        fileManager.remove_files_with_regex(path, '*-cov.fif')
        raise

    # Update ui.
    self.parent.update_covariance_info_box()

def plot_covariance(self):
    """Plots the covariance matrix."""
    subject = self.experiment.active_subject
    cov = subject.get_cov()
    cov.plot(subject._working_file.info)

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
                 subjects_dir=subject._reconFiles_directory)
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
    subjects_dir = self.experiment.active_subject.reconFiles_directory
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

