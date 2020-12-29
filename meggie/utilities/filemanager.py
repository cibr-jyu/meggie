# coding: utf-8

"""
"""

import os
import pickle
import shutil
import re
import sys
import datetime
import logging
import errno

from distutils import dir_util

import numpy as np
import mne


def open_raw(fname, preload=True):
    """
    """
    try:
        logging.getLogger('ui_logger').info('Reading ' + fname)
        raw = mne.io.read_raw(fname, preload=preload)
        return raw
    except Exception as exc:
        logging.getLogger('ui_logger').exception(str(exc))
        raise Exception('Could not read the raw file: ' + str(fname))

def save_raw(raw, path, overwrite=True):
    """ Makes saving raw more atomic
    """

    folder = os.path.dirname(path)
    bname = os.path.basename(path)

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
    """
    """
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path)


def create_timestamped_folder(experiment):
    """
    """
    current_time_str = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.join(experiment.workspace,
                        experiment.name, 'output')
    timestamped_folder = os.path.join(path, current_time_str)

    try:
        os.makedirs(timestamped_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return timestamped_folder


def copy_subject_raw(subject, path):
    """ Makes copy of the raw file at subject creation
    """

    bname = os.path.basename(path)
    folder = os.path.dirname(path)
    stem, ext = os.path.splitext(bname)

    ext_len = len(ext)

    p = re.compile(bname[:-ext_len] + r'(-[0-9]+)?' + bname[-ext_len:])

    contents = os.listdir(folder)
    files = [fname_ for fname_ in contents if p.match(fname_)]

    for fname in files:
        shutil.copyfile(os.path.join(folder, fname), 
                        os.path.join(subject.path, fname))

def save_csv(path, data, column_names, row_descs):
    """
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
    """
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


# see https://stackoverflow.com/a/13790289
def tail(f, lines=1, _buffer=4098):
    """Tail a file and get X lines from the end"""
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
    """ Tries to find correct path for file from user's home folder """
    from os.path import expanduser
    home = expanduser("~")

    if not home:
        return '.'

    return home
