# coding: utf-8
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen, Erkka Heinilä
This module contains caller class that contains the main state of the software
"""

import subprocess
import itertools
import os
import glob
import fnmatch
import re
import shutil
import copy
import math
from os.path import isfile
from os.path import join
from subprocess import CalledProcessError
from copy import deepcopy

from functools import partial
from collections import OrderedDict

from PyQt4 import QtCore, QtGui

import mne
import numpy as np
import pylab as pl
import matplotlib.pyplot as plt


from meggie.ui.sourceModeling.holdCoregistrationDialogMain import holdCoregistrationDialog
from meggie.ui.sourceModeling.forwardModelSkipDialogMain import ForwardModelSkipDialog
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.general.wrapper import wrap_mne_call
from meggie.code_meggie.general import fileManager
from meggie.code_meggie.epoching.epochs import Epochs
from meggie.code_meggie.epoching.events import Events
from meggie.code_meggie.general.measurementInfo import MeasurementInfo
from meggie.code_meggie.general.singleton import Singleton

from meggie.code_meggie.utils.units import get_scaling
from meggie.code_meggie.utils.units import get_unit
from meggie.code_meggie.utils.units import get_power_unit


### Methods needed for source modeling ###    

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

def create_forward_model(self, fmdict):
    """
    Creates a single forward model and saves it to an appropriate
    directory.
    The steps taken are the following:

    - Run mne_setup_source_space to handle various steps of source space
    creation
    - Use mne_watershed_bem to create bem model meshes
    - Create BEM model with mne_setup_forward_model
    - Copy the bem files to the directory named according to fmname

    Keyword arguments:
    
    fmdict        -- dictionary, including in three dictionaries, the
                     parameters for three separate mne scripts run
                     in the forward model creation.
    """
    activeSubject = self.experiment._active_subject

    # Set env variables to point to appropriate directories. 
    os.environ['SUBJECTS_DIR'] = activeSubject._source_analysis_directory
    os.environ['SUBJECT'] = 'reconFiles'
    
    # The scripts call scripts themselves and need environ for path etc.
    env = os.environ
    
    # Some test files for whether setup_source_space has and watershed
    # have already been run. MNE scripts delete these if something fails,
    # so it should be save to base tests on these.
    bemDir = os.path.join(activeSubject._reconFiles_directory, 'bem/')
    fmDir = activeSubject._forwardModels_directory
            
    # Should have the source space description file.
    sourceSpaceSetupTestList = glob.glob(bemDir + '*src.fif') 
    
    waterShedDir = os.path.join(bemDir, 'watershed/')
    waterShedSurfaceTestFile = os.path.join(waterShedDir,
                                            'reconFiles_brain_surface')
    wsCorTestFile = os.path.join(waterShedDir, 'ws/', 'COR-.info')
    
    fmname = fmdict['fmname']
    (setupSourceSpaceArgs, waterShedArgs, setupFModelArgs) = \
    fileManager.convertFModelParamDictToCmdlineParamTuple(fmdict)
    
    # Check if source space is already setup and watershed calculated, and
    # offer to skip them and only perform setup_forward_model.
    reply = 'computeAll'
    if len(sourceSpaceSetupTestList) > 0 and \
        os.path.exists(waterShedSurfaceTestFile) and \
        os.path.exists(wsCorTestFile):
    
        try: 
            sSpaceDict = fileManager.unpickle(os.path.join(fmDir,
                                              'setupSourceSpace.param'))
            wshedDict = fileManager.unpickle(os.path.join(fmDir,
                                                          'wshed.param'))

            fModelSkipDialog = ForwardModelSkipDialog(self, sSpaceDict,
                                                      wshedDict)
        
            fModelSkipDialog.exec_()
            reply = fModelSkipDialog.get_return_value()
        except:
            # On error compute all.
            reply = 'computeAll'
    
    if reply == 'cancel':
        # To keep forward model dialog open
        return False
    
    elif reply == 'bemOnly':
        # Need to do this to get triangulation files to right place and
        # naming for mne_setup_forward_model.
        fileManager.link_triang_files(activeSubject)
        self._call_mne_setup_forward_model(setupFModelArgs, env)
    
        fileManager.create_fModel_directory(fmname, activeSubject)          
        fileManager.write_forward_model_parameters(fmname,
            activeSubject, None, None, fmdict['sfmodelArgs'])
        
        # These should always exist, should be safe to unpickle.
        sspaceParamFile = os.path.join(fmDir, 'setupSourceSpace.param')
        wshedParamFile = os.path.join(fmDir, 'wshed.param')
        sspaceArgsDict = fileManager.unpickle(sspaceParamFile)
        wshedArgsDict = fileManager.unpickle(wshedParamFile)
             
        mergedDict = dict([('fmname', fmname)] + \
                          sspaceArgsDict.items() + \
                          wshedArgsDict.items() + \
                          fmdict['sfmodelArgs'].items() + \
                          [('coregistered', 'no')] + \
                          [('fsolution', 'no')])
        
        fmlist = self.parent.forwardModelModel.\
                 fmodel_dict_to_list(mergedDict)
        self.parent.forwardModelModel.add_fmodel(fmlist)
    
    elif reply == 'computeAll':
        # To make overwriting unnecessary
        if os.path.isdir(bemDir):
            shutil.rmtree(bemDir)
        self._call_mne_setup_source_space(setupSourceSpaceArgs, env)
        self._call_mne_watershed_bem(waterShedArgs, env)
        
        # Right name and place for triang files, see above.
        fileManager.link_triang_files(activeSubject)
        self._call_mne_setup_forward_model(setupFModelArgs, env)    
    
        fileManager.create_fModel_directory(fmname, activeSubject)          
        fileManager.write_forward_model_parameters(fmname, activeSubject,
            fmdict['sspaceArgs'], fmdict['wsshedArgs'],
            fmdict['sfmodelArgs'])
        mergedDict = dict([('fmname', fmname)] + \
                          fmdict['sspaceArgs'].items() + \
                          fmdict['wsshedArgs'].items() + \
                          fmdict['sfmodelArgs'].items() + \
                          [('coregistered', 'no')] + \
                          [('fsolution', 'no')])
            
        fmlist = self.parent.forwardModelModel.\
                 fmodel_dict_to_list(mergedDict)
        self.parent.forwardModelModel.add_fmodel(fmlist)             

    return True

def _call_mne_setup_source_space(self, setupSourceSpaceArgs, env):
    try:
        # TODO: this actually has an MNE-Python counterpart, which doesn't
        # help much, as the others don't (11.10.2014).
        mne_setup_source_space_commandList = \
            ['$MNE_ROOT/bin/mne_setup_source_space'] + \
            setupSourceSpaceArgs
        mne_setup_source_spaceCommand = ' '.join(
                                        mne_setup_source_space_commandList)
        setupSSproc = subprocess.check_output(mne_setup_source_spaceCommand,
                                shell=True, env=env)
        self.parent.processes.append(setupSSproc)
    except CalledProcessError as e:
        raise Exception('There was a problem with mne_setup_source_space. Script '
                        'output: \n' + e.output)
    except Exception as e:
        message = 'There was a problem with mne_setup_source_space: ' + \
                  str(e) + \
                  ' (Are you sure you have your MNE_ROOT set right ' + \
                  'in Meggie preferences?)'
        raise Exception(message)

def _call_mne_watershed_bem(self, waterShedArgs, env):
    try:
        mne_watershed_bem_commandList = ['$MNE_ROOT/bin/mne_watershed_bem'] + \
                                waterShedArgs
        mne_watershed_bemCommand = ' '.join(mne_watershed_bem_commandList)
        wsProc = subprocess.check_output(mne_watershed_bemCommand,
                                shell=True, env=env)
        self.parent.processes.append(wsProc)

    except CalledProcessError as e:
        title = 'Problem with forward model creation'
        message = 'There was a problem with mne_watershed_bem. ' + \
                  'Script output: \n' + e.output
        raise Exception(message)

    except Exception as e:
        message = 'There was a problem with mne_watershed_bem: ' + \
                  str(e) + \
                  ' (Are you sure you have your MNE_ROOT set right ' + \
                  'in Meggie preferences?)'
        raise Exception(message)

def _call_mne_setup_forward_model(self, setupFModelArgs, env):
    try:
        mne_setup_forward_modelCommandList = \
            ['$MNE_ROOT/bin/mne_setup_forward_model'] + setupFModelArgs
        mne_setup_forward_modelCommand = ' '.join(
                                    mne_setup_forward_modelCommandList)
        setupFModelProc = subprocess.check_output(mne_setup_forward_modelCommand, shell=True,
                                env=env)
        self.parent.processes.append(setupFModelProc)
    except CalledProcessError as e:    
        title = 'Problem with forward model creation'
        message = 'There was a problem with mne_setup_forward_model. ' + \
                 'Script output: \n' + e.output
        raise Exception(message)
    except Exception as e:
        message = 'There was a problem with mne_setup_forward_model: ' + \
                  str(e) + \
                  ' (Are you sure you have your MNE_ROOT set right ' + \
                  'in Meggie preferences?)'
        raise Exception(message)

def coregister_with_mne_gui_coregistration(self):
    """
    Uses mne.gui.coregistration for head coordinate coregistration.
    """
    activeSubject = self.experiment.active_subject
    tableView = self.parent.ui.tableViewFModelsForCoregistration
    
    # Selection for the view is SingleSelection / SelectRows, so this
    # should return indexes for single row.
    selectedRowIndexes = tableView.selectedIndexes()
    selectedFmodelName = selectedRowIndexes[0].data() 
                         
    subjects_dir = os.path.join(activeSubject._forwardModels_directory,
                                selectedFmodelName)
    subject = 'reconFiles'
    rawPath = os.path.join(activeSubject.subject_path,
                           self.experiment.active_subject.working_file_name)

    gui = mne.gui.coregistration(tabbed=True, split=True, scene_width=300,
                                 inst=rawPath, subject=subject,
                                 subjects_dir=subjects_dir)
    QtCore.QCoreApplication.processEvents()

    # Needed for copying the resulting trans file to the right location.
    self.coregHowtoDialog = holdCoregistrationDialog(self, activeSubject,
                                                     selectedFmodelName) 
    self.coregHowtoDialog.ui.labelTransFileWarning.hide()
    self.coregHowtoDialog.show()

def create_forward_solution(self, fsdict):
    """
    Creates a forward solution based on parameters given in fsdict.

    Keyword arguments:

    fsdict    -- dictionary of parameters for forward solution creation.
    """
    activeSubject = self.experiment._active_subject
    rawInfo = activeSubject.get_working_file().info

    tableView = self.parent.ui.tableViewFModelsForSolution
    selectedRowIndexes = tableView.selectedIndexes()
    selectedFmodelName = selectedRowIndexes[0].data()

    fmdir = os.path.join(activeSubject._forwardModels_directory,
                         selectedFmodelName)
    transFilePath = os.path.join(fmdir, 'reconFiles',
                                 'reconFiles-trans.fif')

    srcFileDir = os.path.join(fmdir, 'reconFiles', 'bem')
    srcFilePath = None
    for f in os.listdir(srcFileDir):
        if fnmatch.fnmatch(f, 'reconFiles*src.fif'):
            srcFilePath = os.path.join(srcFileDir, f)

    bemSolFilePath = None
    for f in os.listdir(srcFileDir):
        if fnmatch.fnmatch(f, 'reconFiles*bem-sol.fif'):
            bemSolFilePath = os.path.join(srcFileDir, f)

    targetFileName = os.path.join(fmdir, 'reconFiles',
                                  'reconFiles-fwd.fif')
    n_jobs = self.parent.preferencesHandler.n_jobs

    try:
        mne.make_forward_solution(rawInfo, transFilePath, srcFilePath,
                                  bemSolFilePath, targetFileName,
                                  fsdict['includeMEG'],
                                  fsdict['includeEEG'], fsdict['mindist'],
                                  fsdict['ignoreref'], True,
                                  n_jobs)
        fileManager.write_forward_solution_parameters(fmdir, fsdict)
        self.parent.forwardModelModel.initialize_model()
    except Exception as e:
        msg = ('There was a problem with forward solution. The MNE-Python '
               'message was: \n\n' + str(e))
        raise Exception(msg)

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
        print 'Reading forward solution...'
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
        print 'Inverse solution computed succesfully.'
        return stc

    stc_fname = os.path.join(subject._stc_directory,
                             stc_fname[:-8] + '-' + type + '-' + method)
    try:
        stc.save(stc_fname)
    except Exception as err:
        raise Exception('Exception while saving inverse '
                        'solution:\n' + str(err))
    print 'Inverse solution computed succesfully.'
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
    import matplotlib.pyplot as plt

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
    click_callback = partial(self.tfr_clicked, data=power, stc=stc,
                             freqs=freqs)
    fig.canvas.mpl_connect('button_press_event', click_callback)
    fig.suptitle('Average power over all sources.')
    plt.show(block=True)
    return fig

