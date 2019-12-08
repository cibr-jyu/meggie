import logging
import os

from pprint import pformat

from meggie.utilities.names import next_available_name
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox

from meggie.tabs.tfr.controller.tfr import save_tfr_channel_averages
from meggie.tabs.tfr.controller.tfr import save_tfr_all_channels
from meggie.tabs.tfr.controller.tfr import save_tse_channel_averages
from meggie.tabs.tfr.controller.tfr import save_tse_all_channels
from meggie.tabs.tfr.controller.tfr import group_average_tfr

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions
from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog

from meggie.tabs.tfr.dialogs.TFRDialogMain import TFRDialog
from meggie.tabs.tfr.dialogs.TFRPlotDialogMain import TFRPlotDialog
from meggie.tabs.tfr.dialogs.TSEPlotDialogMain import TSEPlotDialog


def create(experiment, data, window):
    """ Opens tfr creation dialog
    """
    selected_names = data['inputs']['epochs']

    if not selected_names:
        return

    if len(selected_names) == 1:
        stem = selected_names[0]
    else:
        stem = 'TFR'
    default_name = next_available_name(
        experiment.active_subject.spectrum.keys(), stem)

    dialog = TFRDialog(experiment, window, selected_names, default_name)
    dialog.show()


def delete(experiment, data, window):
    """ Deletes selected tfr item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    subject.remove(selected_name, 'tfr')
    experiment.save_experiment_settings()
    window.initialize_ui()


def delete_from_all(experiment, data, window):
    """ Deletes selected spetrum item from all subjects
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    for subject in experiment.subjects.values():
        if selected_name in subject.tfr:
            try:
                subject.remove(selected_name, 'tfr')
            except Exception as exc:
                logging.getLogger('ui_logger').warning(
                    'Could not remove tfr for ' +
                    subject.name)
    
    experiment.save_experiment_settings()
    window.initialize_ui()


def plot_tfr(experiment, data, window):
    """ Plot TFR topography or averages from selected item
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    dialog = TFRPlotDialog(window, experiment, selected_name)
    dialog.show()

def plot_tse(experiment, data, window):
    """ Plot TSE topography or averages from selected item
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    dialog = TSEPlotDialog(window, experiment, selected_name)
    dialog.show()


def save_tfr(experiment, data, window):
    """ Saves averages or channels to csv from selected item from all subjects
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    time_arrays = []
    freq_arrays = []
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(selected_name)
        if not tfr:
            continue
        time_arrays.append(tfr.times)
        freq_arrays.append(tfr.freqs)
    assert_arrays_same(time_arrays)
    assert_arrays_same(freq_arrays)

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                save_tfr_channel_averages(
                    experiment, selected_name)
            else:
                save_tfr_all_channels(
                    experiment, selected_name)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def save_tse(experiment, data, window):
    """ Computes TSE and saves averages or channels 
    to csv from selected item from all subjects
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    time_arrays = []
    freq_arrays = []
    for subject in experiment.subjects.values():
        tfr = subject.tfr.get(selected_name)
        if not tfr:
            continue
        time_arrays.append(tfr.times)
        freq_arrays.append(tfr.freqs)
    assert_arrays_same(time_arrays)
    assert_arrays_same(freq_arrays)

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                save_tse_channel_averages(
                    experiment, selected_name)
            else:
                save_tse_all_channels(
                    experiment, selected_name)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    pass


def tfr_info(experiment, data, window):
    """ Fills info element
    """
    try:
        selected_name = data['outputs']['tfr'][0]
        evoked = experiment.active_subject.tfr[selected_name]
        message = pformat(evoked.params)
    except Exception as exc:
        message = ""

    return message
