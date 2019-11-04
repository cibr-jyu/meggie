import logging

from pprint import pformat

from meggie.utilities.channels import read_layout
from meggie.utilities.channels import get_channels
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox

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
    """ Plots spectrum topography of selected item
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return
    plot_spectrum_topo(experiment, selected_name)


def plot_averages(experiment, data, window):
    """ Plots spectrum averages of selected item
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return
    plot_spectrum_averages(experiment, selected_name)


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


def save(experiment, data, window):
    pass


def save_averages(experiment, data, window):
    pass


def spectrum_info(experiment, data, window):
    try:
        selected_name = data['outputs']['spectrum'][0]
        spectrum = experiment.active_subject.spectrum[selected_name]
        message = pformat(spectrum.params)
    except Exception as exc:
        message = ""

    return message

