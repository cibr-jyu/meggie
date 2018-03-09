# coding: utf-8
"""
Created on Apr 11, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Janne Pesonen
"""

import subprocess
import logging
import functools
import os

import numpy as np
import matplotlib.pyplot as plt

import meggie.code_meggie.general.mne_wrapper as mne

import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.general.stc import SourceEstimateEvoked
from meggie.code_meggie.general.stc import SourceEstimateEpochs
from meggie.code_meggie.general.stc import SourceEstimateRaw


def plot_source_estimate(experiment, stc, initial_time):
    """
    """
    subject = experiment.active_subject.mri_subject_name
    subjects_dir = experiment.active_subject.source_analysis_directory

    stc.plot(subjects_dir=subjects_dir, subject=subject, initial_time=initial_time, hemi='split', time_viewer=True, views=['lat', 'med'])


def create_lcmv_estimate(experiment, stc_name, inst_name, inst_type, 
                         data_covfile, noise_covfile, fwd_name, label,
                         reg, start, stop):
    """
    """

    subject = experiment.active_subject

    fwd_path = os.path.join(subject.forward_solutions_directory, fwd_name)
    fwd = mne.read_forward_solution(fwd_path)

    data_cov_path = os.path.join(subject.cov_directory, data_covfile)
    data_cov = mne.read_cov(data_cov_path)

    noise_cov_path = os.path.join(subject.cov_directory, noise_covfile)
    noise_cov = mne.read_cov(noise_cov_path)

    info = subject.get_working_file(preload=False).info

    logging.getLogger('ui_logger').info('Beamforming...')

    if inst_type == 'evoked':
        evokeds = subject.evokeds[inst_name].mne_evokeds
        stc_insts = {}
        for key, inst in evokeds.items():
            stc_insts[key] = mne.lcmv(inst, fwd, noise_cov=noise_cov, 
                data_cov=data_cov, reg=reg, label=label)

        stc = SourceEstimateEvoked(stc_name, stcs=stc_insts)
            
    elif inst_type == 'epochs':
        inst = subject.epochs[inst_name].raw
        stc_insts = mne.lcmv_epochs(inst, fwd, noise_cov=noise_cov, 
            data_cov=data_cov, reg=reg, label=label)
        
        stc = SourceEstimateEpochs(stc_name, stcs=stc_insts)

    elif inst_type == 'raw':
        inst = subject.get_working_file().copy().copy()
        inst.apply_proj()
      
        stc_inst = mne.lcmv_raw(inst, fwd, noise_cov=noise_cov, 
            data_cov=data_cov, reg=reg, label=label)
        
        stc = SourceEstimateRaw(stc_name, stc=stc_inst)


    logging.getLogger('ui_logger').info('Saving stc...')
    subject.add_stc(stc)
    stc.save(experiment)

    experiment.save_experiment_settings()


def create_linear_source_estimate(experiment, stc_name, inst_name, inst_type, 
                                  covfile, fwd_name, loose, depth, label, 
                                  lambda2, method, start, stop):
    """
    """
    subject = experiment.active_subject

    fwd_path = os.path.join(subject.forward_solutions_directory, fwd_name)
    fwd = mne.read_forward_solution(fwd_path)

    cov_path = os.path.join(subject.cov_directory, covfile)
    cov = mne.read_cov(cov_path)

    info = subject.get_working_file(preload=False).info

    logging.getLogger('ui_logger').info('Creating inverse operator...')
    inv = mne.make_inverse_operator(info, fwd, cov, loose=loose, depth=depth)

    logging.getLogger('ui_logger').info('Applying inverse operator...')

    if inst_type == 'evoked':
        evokeds = subject.evokeds[inst_name].mne_evokeds
        stc_insts = {}
        for key, inst in evokeds.items():
            stc_insts[key] = mne.apply_inverse(inst, inv, lambda2, 
                                                method, label)

        stc = SourceEstimateEvoked(stc_name, stcs=stc_insts)
            
    elif inst_type == 'epochs':
        inst = subject.epochs[inst_name].raw
        stc_insts = mne.apply_inverse_epochs(inst, inv, lambda2, method, label)
        stc = SourceEstimateEpochs(stc_name, stcs=stc_insts)

    elif inst_type == 'raw':
        inst = subject.get_working_file().copy().copy()
        inst.apply_proj()

        stc_inst = mne.apply_inverse_raw(inst, inv, lambda2, method, label, 
                                         start, stop)
        stc = SourceEstimateRaw(stc_name, stc=stc_inst)


    logging.getLogger('ui_logger').info('Saving stc...')
    subject.add_stc(stc)
    stc.save(experiment)

    experiment.save_experiment_settings()
    

def create_forward_solution(subject, solution_name, decim, triang_ico, conductivity, include_eeg, include_meg):
    """
    """

    subject_name = subject.mri_subject_name
    subjects_dir = subject.source_analysis_directory

    logging.getLogger('ui_logger').info('Setting up the source space...')
    src = mne.setup_source_space(subject=subject_name, spacing=decim,
        subjects_dir=subjects_dir)


    logging.getLogger('ui_logger').info('Creating bem model...')
    model = mne.make_bem_model(subject=subject_name, ico=triang_ico,
			       conductivity=conductivity,
			       subjects_dir=subjects_dir)

    logging.getLogger('ui_logger').info('Creating bem solution...')
    bem = mne.make_bem_solution(model)

    # gather parameters
    trans = subject.transfile_path
    info = subject.get_working_file().info
    meg = include_meg
    eeg = include_eeg
    
    logging.getLogger('ui_logger').info('Creating forward solution...')
    fwd = mne.make_forward_solution(info, trans=trans, src=src, bem=bem,
        meg=meg, eeg=eeg, mindist=5.0)

    # save the file
    fname = solution_name + '-' + decim + '-src-fwd.fif'
    path = os.path.join(subject.forward_solutions_directory, fname)

    mne.write_forward_solution(path, fwd)

    logging.getLogger('ui_logger').info('Forward solution creation done.')

