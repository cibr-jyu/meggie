# coding: utf-8
"""
"""

import os
import logging

import mne


def get_channels(info):
    channels = {}
    grads = mne.pick_types(info, meg='grad', eeg=False)
    if grads.size > 0:
        channels['grad'] = grads
    mags = mne.pick_types(info, meg='mag', eeg=False)
    if mags.size > 0:
        channels['mag'] = mags
    eegs = mne.pick_types(info, meg=False, eeg=True)
    if eegs.size > 0:
        channels['eeg'] = eegs
    return channels


def read_layout(layout):
    """
    """
    if not layout or layout == "Infer from data":
        return

    if os.path.isabs(layout):
        fname = os.path.basename(layout)
        folder = os.path.dirname(layout)
        return mne.channels.read_layout(fname, folder)

    import pkg_resources
    path_mne = pkg_resources.resource_filename(
        'mne', os.path.join('channels', 'data', 'layouts'))
    path_meggie = pkg_resources.resource_filename(
        'meggie', os.path.join('data', 'layouts'))

    if os.path.exists(os.path.join(path_mne, layout)):
        return mne.channels.read_layout(layout, path_mne)

    if os.path.exists(os.path.join(path_meggie, layout)):
        return mne.channels.read_layout(layout, path_meggie)


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
