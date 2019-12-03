import logging
import os

import numpy as np

from pprint import pformat

from meggie.utilities.channels import read_layout
from meggie.utilities.channels import get_channels
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.groups import average_data_to_channel_groups

import meggie.utilities.filemanager as filemanager

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions
from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog
from meggie.tabs.spectrum.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog

from meggie.tabs.spectrum.controller.spectrum import plot_spectrum_topo
from meggie.tabs.spectrum.controller.spectrum import plot_spectrum_averages
from meggie.tabs.spectrum.controller.spectrum import group_average_spectrum


def create(experiment, data, window):
    """ Opens spectrum creation dialog
    """
    dialog = PowerSpectrumDialog(experiment, window)
    dialog.show()


def delete(experiment, data, window):
    """ Deletes selected spectrum item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    subject.remove(selected_name, 'spectrum')
    experiment.save_experiment_settings()
    window.initialize_ui()


def delete_from_all(experiment, data, window):
    """ Deletes selected spectrum item from all subjects
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    for subject in experiment.subjects.values():
        if selected_name in subject.spectrum:
            try:
                subject.remove(selected_name, 'spectrum')
            except Exception as exc:
                logging.getLogger('ui_logger').warning(
                    'Could not remove spectrum for ' +
                    subject.name)

    experiment.save_experiment_settings()
    window.initialize_ui()


def plot_spectrum(experiment, data, window):
    """ Plots spectrum topography or averages of selected item
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                plot_spectrum_averages(experiment, selected_name)
            else:
                plot_spectrum_topo(experiment, selected_name)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    def handler(groups):
        try:
            group_average_spectrum(experiment, selected_name, groups,
                                   do_meanwhile=window.update_ui)
        except Exception as exc:
            exc_messagebox(window, exc)
            return

        experiment.save_experiment_settings()
        window.initialize_ui()

    dialog = GroupAverageDialog(experiment, window, handler)
    dialog.show()


def _save_all_channels(experiment, selected_name):
    column_names = []
    row_names = []
    csv_data = []

    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue
        for key, psd in spectrum.content.items():
            csv_data.extend(psd.tolist())
            column_names = spectrum.freqs.tolist()

            for ch_name in spectrum.ch_names:
                name = subject.name + '{' + key + '}[' + ch_name + ']'
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_all_channels.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def _save_averages(experiment, selected_name):
    column_names = []
    row_names = []
    csv_data = []

    channel_groups = experiment.channel_groups

    # accumulate csv contents
    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue

        log_transformed = spectrum.log_transformed
        ch_names = spectrum.ch_names
        freqs = spectrum.freqs

        for key, psd in spectrum.content.items():

            if log_transformed:
                psd = 10 ** (psd / 10.0)

            data_labels, averaged_data = average_data_to_channel_groups(
                psd, ch_names, channel_groups)

            if log_transformed:
                averaged_data = 10 * np.log10(averaged_data)

            csv_data.extend(averaged_data.tolist())
            column_names = freqs.tolist()

            for ch_type, area in data_labels:
                name = (subject.name + '{' + key + '}[' +
                        ch_type + '|' + area + ']')
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = selected_name + '_all_subjects_channel_averages.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save(experiment, data, window):
    """ Saves all channels or averages to csv from selected item from all 
    subjects
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    # validate freqs
    freq_arrays = []
    for subject in experiment.subjects.values():
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            continue
        freq_arrays.append(spectrum.freqs)
    assert_arrays_same(freq_arrays)

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                _save_averages(experiment, selected_name)
            else:
                _save_all_channels(experiment, selected_name)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def spectrum_info(experiment, data, window):
    """
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
        spectrum = experiment.active_subject.spectrum[selected_name]
        message = pformat(spectrum.params)
    except Exception as exc:
        message = ""

    return message
