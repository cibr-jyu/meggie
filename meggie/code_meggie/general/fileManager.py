# coding: utf-8
"""
Created on Mar 13, 2013

@author: Jaakko Leppakangas, Atte Rautio, Kari Aliranta

A module for various file operations needed by Meggie.
"""
 
import os
import pickle
import shutil
import glob
import re
import sys
import datetime
import logging

import numpy as np

from distutils import dir_util

import meggie.code_meggie.general.mne_wrapper as mne

def read_layout(layout):
    if not layout or layout == "Infer from data":
	return None

    if os.path.isabs(layout):
        fname = os.path.basename(layout)
        folder = os.path.dirname(layout)
	return mne.read_layout(fname, folder)

    import pkg_resources
    path_mne = pkg_resources.resource_filename('mne', 'channels/data/layouts')
    path_meggie = pkg_resources.resource_filename('meggie', 'data/layouts')

    if os.path.exists(os.path.join(path_mne, layout)):
	return mne.read_layout(layout, path_mne)

    if os.path.exists(os.path.join(path_meggie, layout)):
	return mne.read_layout(layout, path_meggie)



def copy_recon_files(activeSubject, sourceDirectory):
    """
    Copies mri and surf files from the given directory to under the active
    subject's reconFiles directory (after creating the said directory, 
    if need be).
    
    Keyword arguments:
    
    activeSubject            -- currently active subject
    sourceDirectory     -- directory including the mri and surf file 
    
    Returns True if copying was successful, else returns False.
    
    """         
    reconDir = activeSubject.reconfiles_directory
    
    # Empty the destination directory first by removing it, then make it
    # again.
    if os.path.isdir(reconDir):
        dir_util.remove_tree(reconDir)
    
    logger = logging.getLogger('ui_logger')
    
    logger.info('Copying recon files...')
    dir_util.copy_tree(sourceDirectory, reconDir)
    logger.info('Recon files copying complete!')
    

def remove_files_with_regex(directory, pattern):
    """
    Removes, from the given directory, files with a given regex pattern in
    their names.
    
    Keyword arguments:
    directory    -- directory to search the files for.
    pattern      -- regex pattern to match.
    """
    for f in os.listdir(directory):
        if re.search(pattern, f):
            os.remove(os.path.join(directory, f))


def delete_file_at(folder, files):
    """Delete files from a folder.
    
    Keyword arguments:
    
    folder -- The location of the deleted files
    files  -- The files to be deleted. Can be a single file or a list of
              files in the same folder.
    """
    if isinstance(files, list):
        for f in files:
            os.remove(os.path.join(folder, f))
        return
    os.remove(os.path.join(folder, files))
    
    
def load_epochs(fname):
    """Load epochs from a folder.
    
    Keyword arguments:
    fname         -- the name of the fif-file containing epochs.
    
    """
    try:
        epochs = mne.read_epochs(fname)
    except IOError:
        raise Exception('Reading epochs failed.')
    return epochs


def load_evoked(fname):
    """Load evokeds to the list when mainWindow is initialized

    Keyword arguments:
    fName -- the name of the fif-file containing evokeds.
    """
    try:
        evokeds = mne.read_evokeds(fname)
    except IOError:
        raise IOError('Reading evokeds failed.')
    return evokeds


def open_raw(fname, preload=True):
    """
    Opens a raw file.
    Keyword arguments:
    fname         -- A file to open
    preload      -- A boolean telling, whether to read the entire data
                     in the file.
    Raises an exception if the file cannot be opened.
    """
    try:
        logging.getLogger('ui_logger').info('Reading ' + fname)
        raw = mne.read_raw_fif(fname, preload=preload, allow_maxshield=True)

        # this was default till mne-python 0.13, so have it for consistency
        if not mne._has_eeg_average_ref_proj(raw.info['projs']):
            if mne.pick_types(raw.info, meg=False, eeg=True).size > 0:
                raw.set_eeg_reference()

        return raw
    except IOError as e:
        raise IOError(str(e))
    except OSError as e:
        raise OSError('You do not have permission to read the file. ' + str(e))
    except ValueError as e:
        raise ValueError('A problem occurred while opening: ' + str(e))


def save_raw(experiment, raw, fname, overwrite=True):
    
    folder = os.path.dirname(fname)
    bname = os.path.basename(fname)
    
    # be protective and save with other name first and move afterwards
    temp_fname = os.path.join(folder, '_' + bname) 
    raw.save(temp_fname, overwrite=True)

    # assumes filename ends with .fif 
    pat_old = re.compile(bname[:-4] + r'(-[0-9]+)?' + bname[-4:])
    pat_new = re.compile('_' + bname[:-4] + r'(-[0-9]+)?' + bname[-4:])
    
    contents = os.listdir(folder)
    old_files = [fname_ for fname_ in contents if pat_old.match(fname_)]
    new_files = [fname_ for fname_ in contents if pat_new.match(fname_)]

    
    if len(old_files) != len(new_files):
        logger = logging.getLogger('ui_logger')
        logger.warning("Be warned, amount of parts has changed!")
        logger.debug("Old parts: ")
        for part in old_files:
            logger.debug(part)
        logger.debug("New parts: ")
        for part in new_files:
            logger.debug(part)
        
    for file_ in new_files:
        shutil.move(os.path.join(folder, os.path.basename(file_)), 
                    os.path.join(folder, os.path.basename(file_)[1:]))
    experiment.active_subject.working_file_name = os.path.basename(fname)
    raw._filenames[0] = fname
    
def group_save_evokeds(path, evokeds, names):
    """ Combine data from multiple evokeds to one big csv """

    if len(evokeds) == 0:
        raise ValueError("At least one evoked object is needed.")

    message = "Writing " + str(len(evokeds)) + " evokeds to " + path
    logging.getLogger('ui_logger').info(message)

    # gather all the data to list of rows
    all_data = []

    # time point data, assume same lengths for all evokeds
    all_data.append(['times'] + evokeds[0].times.tolist())

    # time series data
    for idx, evoked in enumerate(evokeds):
        for ch_idx in range(len(evoked.data)):
            ch_name = evoked.info['ch_names'][ch_idx].replace(' ', '')
            row_name = names[idx] + ' ' + ch_name

            # mark bad channels
            if evoked.info['ch_names'][ch_idx] in evoked.info['bads']:
                row_name += ' (bad)'

            row = [row_name] + evoked.data[ch_idx, :].tolist()
            all_data.append(row)

    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt='%s', delimiter=', ')    


def save_tfr(path, tfr, times, freqs):

    all_data = []
    all_data.append([''] + times.tolist())
    
    for i in range(tfr.shape[0]):
        row = []
        row.append(freqs[i])
        for value in tfr[i]:
            row.append(value)
        all_data.append(row) 

    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt='%s', delimiter=', ')    


def save_tfr_topology(path, tfrs, times, freqs, labels):
    all_data = []
    all_data.append([''] + times.tolist())
    for idx, tfr in enumerate(tfrs):
        for i in range(tfr.shape[0]):
            row = []
            row.append('[' + labels[idx] + '] ' +  str(freqs[i]))
            for value in tfr[i]:
                row.append(value)
            all_data.append(row)

    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt='%s', delimiter=', ')    


def save_epoch(epoch, overwrite=False):
    """
    """
    if os.path.exists(epoch.path) and overwrite is False:
        return
    # First save the epochs
    epoch.raw.save(epoch.path)


def get_layouts():
    """
    """
    from pkg_resources import resource_filename
    
    files = []
    
    try:
        path_meggie = resource_filename('meggie', 'data/layouts')

        files.extend([f for f in os.listdir(path_meggie)])
    except:
        pass        
    
    try:    
        path = resource_filename('mne', 'channels/data/layouts')
        
        files.extend([f for f in os.listdir(path) 
                      if os.path.isfile(os.path.join(path,f)) 
                      and f.endswith('.lout')])
    except:
        pass
    
    return files

def ensure_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def ensure_folders(paths):
    for path in paths:
        ensure_folder(path)
        
def create_timestamped_folder(experiment):
    current_time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.join(experiment.workspace,
                        experiment.experiment_name, 'output')
    timestamped_folder = os.path.join(path, current_time_str)

    import errno;
    try:
        os.makedirs(timestamped_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return timestamped_folder

def save_subject_raw(subject, path):
    
    filename = os.path.basename(path)
    os.chdir(os.path.dirname(path))
    files = glob.glob(filename[:-4] + '*.fif')
   
    p = re.compile(re.escape(filename[:-4]) + '(.fif|-\d{1,}.fif)')
    
    for f in files:
        if p.match(f):
            shutil.copyfile(f, os.path.join(subject.subject_path, 
                                            os.path.basename(f)))

def _read_epoch_stcs(subject):
    """
    Helper for getting stc epoch dirs for a subject.
    Args:
        subject: instance of Subject
            Subject in use.

    Returns: list
        List of epoch dirs as str.
    """
    stc_dir = subject.stc_directory
    stcs = list()
    for epochs_dir in os.listdir(stc_dir):
        if os.path.isdir(os.path.join(stc_dir, epochs_dir)):
            stcs.append(epochs_dir)
    return stcs

def save_np_array(path, freqs, data, epochs_info):
    
    # gather all the data to list of rows
    all_data = []

    # freqs data, assume same lengths for all evokeds
    all_data.append(['freqs'] + freqs.tolist())

    for idx in range(data.shape[0]):
        row_name = epochs_info['ch_names'][idx]
        
        # mark bad channels
        if epochs_info['ch_names'][idx] in epochs_info['bads']:
            row_name += ' (bad)'        
        
        row = [row_name] + data[idx].tolist()
        all_data.append(row)
 
    # save to file
    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt='%s', delimiter=', ')    
    
