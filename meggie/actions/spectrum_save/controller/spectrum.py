""" Contains controlling logic for the spectrum saving.
"""

import os
import logging

import mne
import numpy as np

import meggie.utilities.filemanager as filemanager

from meggie.utilities.formats import format_floats
from meggie.utilities.channels import average_to_channel_groups

from meggie.utilities.threading import threaded


@threaded
def save_all_channels(experiment, selected_name):
    """ Saves all channesl of a spectrum item to a csv file. """
    column_names = []
    row_descs = []
    csv_data = []

    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue
        for key, psd in spectrum.content.items():
            csv_data.extend(psd.tolist())
            column_names = format_floats(spectrum.freqs)

            for ch_name in spectrum.ch_names:
                row_desc = (subject.name, key, ch_name)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_all_channels_spectrum.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

@threaded
def save_channel_averages(experiment, selected_name, channel_groups, log_transformed=False):
    """ Saves channel averages of a spectrum item to a csv file. """
    column_names = []
    row_descs = []
    csv_data = []

    # accumulate csv contents
    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue

        ch_names = spectrum.ch_names
        freqs = spectrum.freqs
        info = spectrum.info

        for key, psd in spectrum.content.items():

            data_labels, averaged_data = average_to_channel_groups(
                psd, info, ch_names, channel_groups)

            if log_transformed:
                csv_data.extend(10 * np.log10(averaged_data.tolist()))
            else:
                csv_data.extend(averaged_data.tolist())

            column_names = format_floats(freqs)

            for ch_type, area in data_labels:
                row_desc = (subject.name, key, ch_type, area)
                row_descs.append(row_desc)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_channel_averages_spectrum.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_descs)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)

