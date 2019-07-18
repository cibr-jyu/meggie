# coding: utf-8

"""
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

import meggie.utilities.mne_wrapper as mne


def read_layout(layout):
    """
    """
    if not layout or layout == "Infer from data":
        return

    if os.path.isabs(layout):
        fname = os.path.basename(layout)
        folder = os.path.dirname(layout)
        return mne.read_layout(fname, folder)

    import pkg_resources
    path_mne = pkg_resources.resource_filename(
        'mne', os.path.join('channels', 'data', 'layouts'))
    path_meggie = pkg_resources.resource_filename(
        'meggie', os.path.join('data', 'layouts'))

    if os.path.exists(os.path.join(path_mne, layout)):
        return mne.read_layout(layout, path_mne)

    if os.path.exists(os.path.join(path_meggie, layout)):
        return mne.read_layout(layout, path_meggie)


def get_layouts():
    """
    """
    from pkg_resources import resource_filename

    files = []

    try:
        path_meggie = resource_filename(
            'meggie', os.path.join('data', 'layouts'))

        files.extend([f for f in os.listdir(path_meggie)])
    except BaseException:
        pass

    try:
        path = resource_filename(
            'mne', os.path.join('channels', 'data', 'layouts'))

        files.extend([f for f in os.listdir(path)
                      if os.path.isfile(os.path.join(path, f))
                      and f.endswith('.lout')])
    except BaseException:
        pass

    return files


def copy_recon_files(activeSubject, sourceDirectory):
    """
    Copies mri and surf files from the given directory to under the active
    subject's reconFiles directory (after creating the said directory,
    if need be).
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


def open_raw(fname, preload=True):
    """
    """
    try:
        logging.getLogger('ui_logger').info('Reading ' + fname)
        raw = mne.read_raw_fif(fname, preload=preload, allow_maxshield=True)

        return raw
    except IOError as e:
        raise IOError(str(e))
    except OSError as e:
        raise OSError('You do not have permission to read the file. ' + str(e))
    except ValueError as e:
        raise ValueError('A problem occurred while opening: ' + str(e))


def save_raw(experiment, raw, fname, overwrite=True):
    """ Makes saving raw more atomic
    """

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

    experiment.active_subject.working_file_name = os.path.basename(fname)
    raw._filenames[0] = fname


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
                        experiment.experiment_name, 'output')
    timestamped_folder = os.path.join(path, current_time_str)

    import errno
    try:
        os.makedirs(timestamped_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    return timestamped_folder


def copy_subject_raw(subject, path):
    """ Makes copy of the raw file at subject creation
    """

    filename = os.path.basename(path)
    os.chdir(os.path.dirname(path))
    files = glob.glob(filename[:-4] + '*.fif')

    p = re.compile(re.escape(filename[:-4]) + r'(.fif|-\d{1,}.fif)')

    for f in files:
        if p.match(f):
            shutil.copyfile(f, os.path.join(subject.path,
                                            os.path.basename(f)))


def save_csv(path, data, column_names, row_names):

    # gather all the data to list of rows
    all_data = []

    # freqs data, assume same lengths
    all_data.append([''] + column_names)

    for idx in range(len(data)):
        row_name = row_names[idx]
        row = [row_name] + data[idx]
        all_data.append(row)

    # save to file
    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt='%s', delimiter=', ')


def load_csv(path):

    all_data = np.loadtxt(path, dtype=np.str, delimiter=', ')
    data = []
    column_names = []
    row_names = []

    column_names = all_data[0, 1:].tolist()
    row_names = all_data[1:, 0].tolist()
    data = all_data[1:, 1:].astype(np.float)

    return column_names, row_names, data


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
