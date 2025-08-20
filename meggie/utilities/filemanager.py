"""Contains functions for tasks related to file system."""

import appdirs
import os
import shutil
import re
import logging

import importlib.resources as _resources
import importlib.metadata as _metadata

import numpy as np
import mne

from mne.io._read_raw import _get_supported as mne_get_supported


def open_raw(fname, preload=True, verbose="info"):
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
        if verbose == "info" or verbose == "debug":
            logging.getLogger("ui_logger").info("Reading " + fname)
            raw = mne.io.read_raw(fname, preload=preload)
        else:
            raw = mne.io.read_raw(fname, preload=preload, verbose=verbose)
        return raw
    except Exception:
        logging.getLogger("ui_logger").exception("")
        raise Exception("Could not read the raw file: " + str(fname))


def save_raw(raw, path, overwrite=True):
    """Saves a raw to file(s).

    For some safety, move the old files first to temp files,
    then save the new version, and then (if has not failed),
    remove the temp files.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw file to be saved.
    path : str
        The path where to save.
    overwrite : bool
        Whether to overwrite.
    """

    logger = logging.getLogger("ui_logger")

    folder = os.path.dirname(path)
    bname = os.path.basename(path)

    if os.path.exists(path) and not overwrite:
        raise IOError("File already exists.")

    # Move existing files to temporary names
    ext = os.path.splitext(bname)[1]

    # Match filenames that
    # 1) do not start with an underscore,
    # 2) do not contain any extra dots, and
    # 3) end with the ext
    pat_old = re.compile(r"^(?!_)[^.]*" + re.escape(ext) + r"$")
    contents = os.listdir(folder)
    old_files = [fname_ for fname_ in contents if pat_old.match(fname_)]

    temp_paths = []
    for file_ in old_files:
        old_path = os.path.join(folder, os.path.basename(file_))
        temp_path = os.path.join(folder, "_" + os.path.basename(file_))
        logger.debug("Moving previously existing file to: " + str(temp_path))
        shutil.move(old_path, temp_path)
        temp_paths.append(temp_path)

    # Save raw data
    logger.debug("Saving new data to: " + str(path))
    raw.save(path, overwrite=True)

    # Remove old files
    for temp_path in temp_paths:
        logger.debug("Removing previously existing file: " + str(temp_path))
        os.remove(temp_path)

    # Just to make sure, set _filenames[0] to match the new path.
    raw._filenames = [path]


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


def save_csv(path, data, column_names, row_descs):
    """Saves tabular data to csv.

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

    if isinstance(data, np.ndarray):
        data = data.tolist()

    # freqs data, assume same lengths
    all_data.append([""] * len(row_descs[0]) + column_names)

    for idx in range(len(data)):
        row = list(row_descs[idx]) + data[idx]
        all_data.append(row)

    # save to file
    all_data = np.array(all_data)
    np.savetxt(path, all_data, fmt="%s", delimiter=", ")


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

    all_data = np.loadtxt(
        path, dtype=str, delimiter=",", converters=lambda s: s.strip()
    )

    data = []
    column_names = []
    row_descs = []

    first_data_idx = np.min(np.where(all_data[0] != "")[0])

    column_names = all_data[0, first_data_idx:].tolist()
    row_descs = [tuple(elems) for elems in all_data[1:, :first_data_idx]]
    data = all_data[1:, first_data_idx:].astype(float)

    return column_names, row_descs, data


def get_resource_filename(package, resource_name):
    """
    Locate a file or folder inside a distribution package, supporting nested paths.

    Parameters
    ----------
    package : str
        Name of the distribution package to search.
    resource_name : str
        Relative path to the resource within the package.

    Returns
    -------
    str
        Absolute filesystem path to the resource.

    Raises
    ------
    FileNotFoundError
        If the resource cannot be found in the given package.
    """
    parts = os.path.normpath(resource_name).split(os.sep)
    try:
        resource_path = _resources.files(package).joinpath(*parts)
        with _resources.as_file(resource_path) as p:
            return str(p)
    except Exception as e:
        raise FileNotFoundError(
            f"Resource {resource_name!r} not found in package {package!r}: {e}"
        )


def get_distribution_version(dist_name):
    """
    Return the installed version of a distribution, or empty string if missing.

    Parameters
    ----------
    dist_name : str
        Name of the distribution package to query.

    Returns
    -------
    str
        Version string, or '' if the package is not installed.
    """
    try:
        return _metadata.version(dist_name)
    except _metadata.PackageNotFoundError:
        return ""


def get_package_keys():
    """
    Return all installed distribution package names as lowercase with dashes replaced by underscores.

    Returns
    -------
    list of str
        Installed package names, lowercased and with '-' converted to '_'.
    """
    keys = []
    for dist in _metadata.distributions():
        name = dist.metadata.get("Name", "")
        if name:
            keys.append(name.lower().replace("-", "_"))
    return keys


def homepath():
    """Tries to find correct path for home folder.

    Returns
    -------
    str
        Path to home directory.

    """

    home = os.path.expanduser("~")

    if not home:
        return "."

    return home


def configpath():
    """Find a path for configuration files.

    Returns
    -------
    str
        Path to config directory

    """
    return appdirs.user_config_dir("meggie")


def datapath():
    """Find a path for data files.

    Returns
    -------
    str
        Path to data directory

    """
    return os.path.join(appdirs.user_data_dir("meggie"), "experiments")


def get_supported_formats():
    """
    Get all raw‐file formats supported by MNE.

    Returns
    -------
    list of tuple
        Each tuple is (file extension, [reader names]) supported by MNE.
    """
    mne_supported = mne_get_supported()

    items = []
    for ext_item in mne_supported.items():
        ext = ext_item[0]
        names = [val[0] for val in ext_item[1].items()]
        items.append((ext, names))

    return items
