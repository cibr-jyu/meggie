import logging
import os

import numpy as np

from pprint import pformat

from meggie.utilities.channels import read_layout
from meggie.utilities.channels import get_channels
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.groups import average_data_to_channel_groups
from meggie.utilities.names import next_available_name

import meggie.utilities.filemanager as filemanager

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions
from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog
from meggie.tabs.spectrum.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog

from meggie.tabs.spectrum.controller.spectrum import plot_spectrum_topo
from meggie.tabs.spectrum.controller.spectrum import plot_spectrum_averages
from meggie.tabs.spectrum.controller.spectrum import group_average_spectrum
from meggie.tabs.spectrum.controller.spectrum import save_channel_averages
from meggie.tabs.spectrum.controller.spectrum import save_all_channels


def create(experiment, data, window):
    """ Opens spectrum creation dialog
    """
    default_name = next_available_name(
        experiment.active_subject.spectrum.keys(), 'Spectrum')

    dialog = PowerSpectrumDialog(experiment, window, default_name)
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

    def handler(name, groups):
        try:
            group_average_spectrum(experiment, selected_name, groups, name,
                                   do_meanwhile=window.update_ui)
            experiment.save_experiment_settings()
            window.initialize_ui()

        except Exception as exc:
            exc_messagebox(window, exc)
            return
    
    default_name = next_available_name(
       experiment.active_subject.spectrum.keys(), 
       'group_' + selected_name)
    dialog = GroupAverageDialog(experiment, window, handler,
                                default_name)
    dialog.show()


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
    assert_arrays_same(freq_arrays, 'Freqs do not match')

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                save_channel_averages(experiment, selected_name)
            else:
                save_all_channels(experiment, selected_name)
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
