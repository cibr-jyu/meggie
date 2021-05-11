"""Contains functions for tasks related to file system.
"""

import os
import shutil
import re
import datetime
import logging
import errno

import numpy as np
import mne


def open_raw(fname, preload=True, verbose='info'):
    """Reads a raw from file.

    Parameters
    ----------
    fname : str
        Path to the raw file.
    preload : bool
        Should the data be loaded as well or just the metadata.
    verbose : str
        Verbose level for the read_raw call.

    Returns
    -------
    mne.io.Raw
        The raw object read from the file.
    """
    try:
        if verbose == 'info' or verbose == 'debug':
            logging.getLogger('ui_logger').info('Reading ' + fname)
            raw = mne.io.read_raw(fname, preload=preload)
        else:
            raw = mne.io.read_raw(fname, preload=preload, verbose=verbose)
        return raw
    except Exception as exc:
        logging.getLogger('ui_logger').exception('')
        raise Exception('Could not read the raw file: ' + str(fname))

def save_raw(raw, path, overwrite=True):
    """Saves a raw to file(s).

    After witnessing several corruptions along the way, 
    this was made more atomic by saving the raw first to a tmp file 
    and then moving with shutil.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw file to be saved.
    path : str
        The path where to save.
    overwrite : bool
        Whether to overwrite.
    """

    folder = os.path.dirname(path)
    bname = os.path.basename(path)

    exists = False
    if os.path.exists(path):
        if not overwrite:
            raise IOError('File already exists.')
        exists = True

    # be protective and save with other name first and move afterwards
    temp_path = os.path.join(folder, '_' + bname)
    raw.save(temp_path, overwrite=True)

    stem, ext = os.path.splitext(bname)
    ext_len = len(ext)

    # assumes filename ends with .fif
    pat_old = re.compile(bname[:-ext_len] + r'(-[0-9]+)?' + bname[-ext_len:])
    pat_new = re.compile('_' + bname[:-ext_len] + r'(-[0-9]+)?' + bname[-ext_len:])

    contents = os.listdir(folder)
    old_files = [fname_ for fname_ in contents if pat_old.match(fname_)]
    new_files = [fname_ for fname_ in contents if pat_new.match(fname_)]

    if len(old_files) != len(new_files):
        logger = logging.getLogger('ui_logger')
        if exists:
            logger.warning("Be warned, amount of parts has changed!")
        logger.debug("Old parts: ")
        for part in old_files:
            logger.debug(part)
        logger.debug("New parts: ")
        for part in new_files:
            logger.debug(part)

    moved_paths = []
    for file_ in new_files:
        tmp_path = os.path.join(folder, os.path.basename(file_))
        new_path = os.path.join(folder, os.path.basename(file_)[1:])
        shutil.move(tmp_path, new_path)
        moved_paths.append(new_path)

    for file_ in old_files:
        old_file_path = os.path.join(folder, os.path.basename(file_))
        if old_file_path not in moved_paths:
            logger.warning('Removing unused part: ' + str(old_file_path))
            os.remove(old_file_path)

    raw._filenames[0] = path


def ensure_folders(paths):
    """Ensures that paths in specified in the paths param exist.

    Parameters
    ----------
    paths : list
        List of folder paths.
    """
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def create_timestamped_folder(experiment):
    """Creates folder with a timestamp inside the output folder in the
    experiment folder.

    Parameters
    ----------
    experiment : meggie.experiment.Experiment
        The experiment where to create the folder.

    Returns
    -------
    str
        The path to the folder.
    """
    current_time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.join(experiment.path, 'output')
    timestamped_folder = os.path.join(path, current_time_str)

    try:
        os.makedirs(timestamped_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return timestamped_folder


def save_csv(path, data, column_names, row_descs):
    """ Saves tabular data to csv.

    Parameters
    ----------
    path : str
        Where to save.
    data : a numpy array of shape (n_rows, n_cols)
        Data to save.
    column_names : list
        List of column names.
    row_descs : list
        List of row descriptions that can be tuples like
        ('EEG', 'Left-frontal'), which are then put to the 
        csv as multiple columns.
    """
    # gather all the data to list of rows
    all_data = []

    if type(data) == np.ndarray:
        data = data.tolist()

    # freqs data, assume same lengths
    all_data.append(['']*len(row_descs[0]) + column_names)

    for idx in range(len(data)):
        row = list(row_descs[idx]) + data[idx]
        all_data.append(row)

    # save to file
    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt='%s', delimiter=', ')


def load_csv(path):
    """Loads tabular data from csv.

    Parameters
    ----------
    path : str
        Path to the csv file.

    Returns
    -------
    list
        Column names.
    list
        Row descriptions.
    np.array
        The data.
    """
    all_data = np.loadtxt(path, dtype=np.str, delimiter=', ')

    data = []
    column_names = []
    row_descs = []

    first_data_idx = np.min(np.where(all_data[0] != '')[0])

    column_names = all_data[0, first_data_idx:].tolist()
    row_descs = [tuple(elems) for elems in all_data[1:, :first_data_idx]]
    data = all_data[1:, first_data_idx:].astype(np.float)

    return column_names, row_descs, data


def tail(f, lines=1, _buffer=4098):
    """Tail a file and get `lines` lines from the end,

    See https://stackoverflow.com/a/13790289

    Parameters
    ----------
    f : file descriptor
        The file descriptor already opened.
    lines : int
        How many lines to read from the end.
    _buffer : int
        What buffer size to use.

    Returns
    -------
    list
        Lines from the end.
    """
    # place holder for the lines found
    lines_found = []

    # block counter will be multiplied by buffer
    # to get the block size from the end
    block_counter = -1

    # loop until we find X lines
    while len(lines_found) < lines:
        try:
            f.seek(block_counter * _buffer, os.SEEK_END)
        except IOError:  # either file is too small, or too many lines requested
            f.seek(0)
            lines_found = f.readlines()
            break

        lines_found = f.readlines()

        block_counter -= 1

    return lines_found[-lines:]


def homepath():
    """Tries to find correct path for home folder.

    Returns
    -------
    str
        Path to home directory.

    """
    from os.path import expanduser
    home = expanduser("~")

    if not home:
        return '.'

    return home
