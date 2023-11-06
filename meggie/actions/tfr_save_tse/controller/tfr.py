""" Contains controlling logic for saving tse
"""

import os
import logging

import numpy as np
import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.threading import threaded


def _compute_tse(meggie_tfr, fmin, fmax):
    tfrs = meggie_tfr.content

    fmin_idx = np.where(meggie_tfr.freqs >= fmin)[0][0]
    fmax_idx = np.where(meggie_tfr.freqs <= fmax)[0][-1]

    if fmax_idx <= fmin_idx:
        raise Exception('Something wrong with the frequencies')

    tses = {}
    for key, tfr in tfrs.items():
        tse = np.mean(tfr.data[:, fmin_idx:fmax_idx+1, :], axis=1)
        tses[key] = tse

    return tses


def _crop_and_correct_to_baseline(tse, blmode, blstart, blend, tmin, tmax, times):
    tmin_idx = np.where(times >= tmin)[0][0]
    tmax_idx = np.where(times <= tmax)[0][-1]

    if blmode:
        if blstart < tmin:
            raise Exception(
                'Baseline start should not be earlier than crop start.')

        if blend > tmax:
            raise Exception(
                'Baseline end should not be later than crop end.')

        # correct to baseline
        tse = mne.baseline.rescale(tse, times, baseline=(blstart, blend),
                                   mode=blmode)

        # crop
        tse = tse[:, tmin_idx:tmax_idx+1]

    return times[tmin_idx:tmax_idx+1], tse


@threaded
def save_tse_all_channels(experiment, tfr_name, blmode, blstart, 
                          blend, tmin, tmax, fmin, fmax):
    """ Saves all channels of a tse to a csv file.
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        tses = _compute_tse(tfr, fmin, fmax)

        for key, tse in tses.items():
            times, tse = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, tfr.times)

            csv_data.extend(tse.tolist())

            for ch_name in tfr.ch_names:
                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

        column_names = format_floats(times)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_all_channels_tse.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


@threaded
def save_tse_channel_averages(experiment, tfr_name, blmode, blstart, 
                              blend, tmin, tmax, fmin, fmax,
                              channel_groups):
    """ Saves channel averages of tse to a csv file.
    """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        tses = _compute_tse(tfr, fmin, fmax)

        for key, tse in tses.items():

            # note: baseline is corrected before channel average
            times, ch_data = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, tfr.times)

            data_labels, averaged_data = average_to_channel_groups(
                ch_data, tfr.info, tfr.ch_names, channel_groups)

            csv_data.extend(averaged_data.tolist())

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

        column_names = format_floats(times)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_channel_averages_tse.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

