""" Contains group average implementation.
"""

import logging

from copy import deepcopy

import mne

import numpy as np

from meggie.datatypes.spectrum.spectrum import Spectrum

from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.validators import assert_lists_same
from meggie.utilities.channels import clean_names
from meggie.utilities.threading import threaded


@threaded
def group_average_spectrum(experiment, spectrum_name, groups, new_name):
    """ Computes a group average spectrum item.
    """
    # check data cohesion
    keys = []
    freq_arrays = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                spectrum = subject.spectrum.get(spectrum_name)
                keys.append(tuple(sorted(spectrum.content.keys())))
                freq_arrays.append(tuple(spectrum.freqs))
            except Exception as exc:
                continue

    assert_lists_same(keys, 'Conditions do not match')
    assert_arrays_same(freq_arrays, 'Freqs do not match')

    # handle channel differences
    ch_names = []
    for group_key, group_subjects in groups.items():
        for subject_name in group_subjects:
            try:
                subject = experiment.subjects.get(subject_name)
                spectrum = subject.spectrum.get(spectrum_name)
                ch_names.append(tuple(clean_names(spectrum.ch_names)))
            except Exception as exc:
                continue

    if len(set(ch_names)) != 1:
        logging.getLogger('ui_logger').info(
            "PSD's contain different sets of channels. Identifying common ones..")

        common_ch_names = list(set.intersection(*map(set, ch_names)))

        logging.getLogger('ui_logger').info(
            str(len(common_ch_names)) + ' common channels found.')
    else:
        common_ch_names = ch_names[0]

    grand_psds = {}
    for group_key, group_subjects in groups.items():
        for subject in experiment.subjects.values():
            if subject.name not in group_subjects:
                continue

            spectrum = subject.spectrum.get(spectrum_name)
            if not spectrum:
                continue

            subject_ch_names = clean_names(spectrum.ch_names) 

            for spectrum_item_key, spectrum_item in spectrum.content.items():
                grand_key = (group_key, spectrum_item_key)

                # get common channels in "subject specific space"
                idxs = [subject_ch_names.index(ch_name) for ch_name 
                        in common_ch_names]

                spectrum_item = spectrum_item[idxs]

                if grand_key not in grand_psds:
                    grand_psds[grand_key] = []
                grand_psds[grand_key].append(spectrum_item)

    grand_averages = {}
    for key, grand_psd in grand_psds.items():
        new_key = str(key[1]) + '_group_' + str(key[0])
        if len(grand_psd) == 1:
            grand_averages[new_key] = grand_psd[0].copy()
        else:
            grand_averages[new_key] = np.mean(grand_psd, axis=0)

    subject = experiment.active_subject

    try:
        spectrum = subject.spectrum.get(spectrum_name)
    except Exception as exc:
        raise Exception('Active subject should be included in the groups')

    spectrum_directory = subject.spectrum_directory

    info = spectrum.info
    common_idxs = [ch_idx for ch_idx, ch_name in enumerate(clean_names(info['ch_names']))
                   if ch_name in common_ch_names]
    info = mne.pick_info(info, sel=common_idxs)

    freqs = spectrum.freqs
    data = grand_averages

    params = deepcopy(spectrum.params)

    # individual intervals not relevant in the group item
    params.pop('intervals', None)

    params['groups'] = groups
    params['conditions'] = [elem for elem in grand_averages.keys()]

    spectrum = Spectrum(new_name, subject.spectrum_directory,
                        params, data, freqs, info)

    spectrum.save_content()
    subject.add(spectrum, 'spectrum')
