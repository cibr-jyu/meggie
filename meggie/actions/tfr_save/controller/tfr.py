""" Contains controlling logic for the tfr implementation
"""

import os
import logging

import mne

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.threading import threaded


@threaded
def save_tfr_all_channels(experiment, tfr_name,
                          blmode, blstart, blend,
                          tmin, tmax, fmin, fmax):
    """ Saves all channels of tfr item to a csv file.
    """
    column_names = []
    row_descs = []
    csv_data = []

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        ch_names = tfr.ch_names

        for key, mne_tfr in tfr.content.items():

            # crop and correct to baseline
            mne_tfr = mne_tfr.copy().crop(tmin=tmin,
                                          tmax=tmax,
                                          fmin=fmin,
                                          fmax=fmax)
            times = mne_tfr.times
            column_names = format_floats(times)
            freqs = format_floats(mne_tfr.freqs)

            data = mne.baseline.rescale(mne_tfr.data, times, baseline=bline,
                                        mode=mode)

            for ix in range(data.shape[0]):
                for iy in range(data.shape[1]):
                    csv_data.append(data[ix, iy].tolist())

                    row_desc = (subject.name, key, ch_names[ix], freqs[iy])
                    row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_all_channels_tfr.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


@threaded
def save_tfr_channel_averages(experiment, tfr_name,
                              blmode, blstart, blend,
                              tmin, tmax, fmin, fmax,
                              channel_groups):
    """ Saves channel averages of tfr item to a csv file.
    """
    column_names = []
    row_descs = []
    csv_data = []

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    # accumulate csv contents
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(tfr_name)
        if not tfr:
            continue

        ch_names = tfr.ch_names
        info = tfr.info

        for key, mne_tfr in tfr.content.items():

            # crop and correct to baseline
            mne_tfr = mne_tfr.copy().crop(tmin=tmin,
                                          tmax=tmax,
                                          fmin=fmin,
                                          fmax=fmax)
            times = mne_tfr.times
            column_names = format_floats(times)
            freqs = format_floats(mne_tfr.freqs)

            # note: baseline is corrected before channel average
            data = mne.baseline.rescale(mne_tfr.data, times, baseline=bline,
                                        mode=mode)

            data_labels, averaged_data = average_to_channel_groups(
                data, info, ch_names, channel_groups)

            for ix in range(averaged_data.shape[0]):
                for iy in range(averaged_data.shape[1]):
                    ch_type, area = data_labels[ix]

                    csv_data.append(averaged_data[ix, iy].tolist())

                    row_desc = (subject.name, key, ch_type, area, freqs[iy])
                    row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = tfr_name + '_all_subjects_channel_averages_tfr.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


