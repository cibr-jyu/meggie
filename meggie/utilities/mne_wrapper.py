import os
import logging
import inspect
import importlib
import pkgutil

from types import ModuleType
from types import FunctionType

import mne


blacklist = ['tests',
             'conftest',
             'externals',
             'splitext',
             'isfunction',
             'basename',
             'wraps',
             'join',
             'contextmanager',
             'namedtuple',
             'getmembers',
             'verbose',
             'get_channel_types',
             'dir_tree_find',
             'read_big',
             'read_tag',
             'make_dir_tree',
             'read_bad_channels',
             'deepcopy',
             'channel_type',
             'get_current_comp',
             'find_tag',
             'read_ctf_comp',
             'read_meas_info',
             'read_tag_info',
             'check_fname',
             'set_log_level',
             'check_fiff_length',
             'fiff_open',
             'write_nop',
             'end_file',
             'write_int',
             'end_block',
             'write_string',
             'check_fiff_length',
             'write_float_matrix',
             'write_float',
             'write_int',
             'start_block',
             'write_name_list',
             'write_ch_info',
             'b',
             'iteritems',
             'pick_info',
             'channel_indices_by_type',
             'setup_proj',
             'make_projector_info',
             'activate_proj',
             'warn',
             'start_file',
             'write_id',
             'get_machid',
             'object_size',
             'write_meas_info',
             'write_dig_points',
             'write_coord_trans',
             'write_ctf_comp',
             'plt_show',
             'read_layout',
             'figure_nobar',
             'einsum',
             'sizeof_fmt',
             'equalize_channels',
             'combine_evoked',
             'apply_trans',
             'parallel_func',
             'find_layout',
             'add_background_image',
             'psd_array_welch',
             'get_spectrogram',
             'check_version',
             'get_config_path',
             'get_config',
             'set_config',
             'check_n_jobs',
             'jcal2jd',
             'jd2jcal',
             'tridi_inverse_iteration',
             'dpss_windows',
             'tridisolve',
             'next_fast_len',
             'make_eeg_layout',
             'tight_layout',
             'shorten',
             'get_fitting_dig',
             'compute_native_head_t',
             'get_ras_to_neuromag_trans',
             'translation',
             'write_double',
             'make_dig_montage',
             'write_hdf5',
             'write_tfrs']

blacklist.extend(['pick_types',
                  'pick_channels',
                  'rescale',
                  'make_projector',
                  'plot_topomap'])


def wrap(log_level, original_func):
    def wrapped(*args, **kwargs):
        logger = logging.getLogger("mne_wrapper_logger")
        numeric_level = getattr(logging, log_level.upper())

        # print("Wrapped function called: " + str(original_func))

        callargs = inspect.getcallargs(original_func, *args, **kwargs)

        message = ("Calling " + str(original_func.__name__) +
                   " with args " + str(callargs))

        logger.log(numeric_level, message)

        return original_func(*args, **kwargs)
    return wrapped


def wrap_package(root, path, suffix):
    contents = pkgutil.walk_packages(path)

    paths = []
    modules = []
    for item in contents:
        if item.name in blacklist:
            continue

        # ensure walk_packages has not walked away from mne directory
        # see https://bugs.python.org/issue36053
        if not item.module_finder.path.startswith(suffix):
            continue

        if item.ispkg:
            paths.append((item.name, os.path.join(item.module_finder.path,
                                                  item.name)))
        else:
            module = importlib.import_module('.'.join([root, item.name]))
            modules.append((item.name, module))

    init = importlib.import_module('.'.join([root, '__init__']))
    modules.append(('__init__', init))

    for module in modules:
        members = inspect.getmembers(module[1])
        for member in members:
            if isinstance(member[1], FunctionType):
                if member[0].startswith('_'):
                    continue
                if member[0] in blacklist:
                    continue

                wrapped = wrap('debug', member[1])
                setattr(module[1], member[0],
                        wrapped)
            # if isinstance(member[1], MethodType)
            # ...

    for path in paths:
        wrap_package('.'.join([root, path[0]]), [path[1]], suffix)


def wrap_mne():
    wrap_package('mne', mne.__path__, mne.__path__[0])
