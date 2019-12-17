"""
"""
import logging
import os

from pprint import pformat

import mne
import matplotlib.pyplot as plt

from meggie.tabs.evoked.controller.evoked import create_averages
from meggie.tabs.evoked.controller.evoked import plot_channel_averages
from meggie.tabs.evoked.controller.evoked import group_average_evoked
from meggie.tabs.evoked.controller.evoked import save_all_channels
from meggie.tabs.evoked.controller.evoked import save_channel_averages

import meggie.utilities.filemanager as filemanager

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions

from meggie.utilities.channels import read_layout
from meggie.utilities.channels import get_channels
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.names import next_available_name

from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog
from meggie.tabs.evoked.dialogs.createEvokedDialogMain import CreateEvokedDialog


def create(experiment, data, window):
    """ Opens evoked creation dialog
    """
    selected_names = data['inputs']['epochs']

    if not selected_names:
        return

    if len(selected_names) == 1:
        stem = selected_names[0]
    else:
        stem = 'Evoked'
    default_name = next_available_name(
        experiment.active_subject.evoked.keys(), stem)

    dialog = CreateEvokedDialog(experiment, window, selected_names, 
                                default_name)
    dialog.show()


def delete(experiment, data, window):
    """ Deletes selected evoked item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    subject.remove(selected_name, 'evoked')
    experiment.save_experiment_settings()
    window.initialize_ui()


def delete_from_all(experiment, data, window):
    """ Deletes selected evoked item from all subjects
    """
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    for subject in experiment.subjects.values():
        if selected_name in subject.evoked:
            try:
                subject.remove(selected_name, 'evoked')
            except Exception as exc:
                logging.getLogger('ui_logger').warning(
                    'Could not remove evoked for ' +
                    subject.name)

    experiment.save_experiment_settings()
    window.initialize_ui()


def _plot_evoked_averages(experiment, evoked):
    plot_channel_averages(experiment, evoked)


def _plot_evoked_topo(experiment, evoked):
    evokeds = []
    for key, evok in evoked.content.items():
        evokeds.append(evok)

    def onclick(event):
        try:
            channel = plt.getp(plt.gca(), 'title')
            plt.gca().set_title('')

            title = "evoked_{0}_{1}".format(evoked.name, channel)

            plt.gcf().canvas.set_window_title(title)
            plt.gcf().suptitle(title)
            plt.show()
        except Exception as exc:
            pass

    fig = mne.viz.plot_evoked_topo(evokeds)
    fig.canvas.mpl_connect('button_press_event', onclick)
    title = "evoked_{0}".format(evoked.name)
    fig.canvas.set_window_title(title)
    fig.suptitle(title)


def plot_evoked(experiment, data, window):
    """ Plots topo or averages of selected item
    """
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return
    subject = experiment.active_subject
    evoked = subject.evoked.get(selected_name)

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                _plot_evoked_averages(
                    experiment, evoked)
            else:
                _plot_evoked_topo(
                    experiment, evoked)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def plot_topomap(experiment, data, window):
    """ Plots topomaps of selected item
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    layout = experiment.layout
    layout = read_layout(layout)

    evoked = subject.evoked.get(selected_name)

    for key, evoked in evoked.content.items():
        channels = get_channels(evoked.info)
        for ch_type in channels.keys():
            title = '{0}_{1}_{2}'.format(selected_name, key, ch_type)
            fig = mne.viz.plot_evoked_topomap(
                evoked, ch_type=ch_type, layout=layout,
                title=title)
            fig.canvas.set_window_title(title)


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    def handler(name, groups):
        try:
            group_average_evoked(experiment, selected_name, groups, name,
                                 do_meanwhile=window.update_ui)
            experiment.save_experiment_settings()
            window.initialize_ui()

        except Exception as exc:
            exc_messagebox(window, exc)
            return

    default_name = next_available_name(
        experiment.active_subject.evoked.keys(), 
        'group_' + selected_name)
    dialog = GroupAverageDialog(experiment, window, handler,
                                default_name)
    dialog.show()


def save(experiment, data, window):
    """ Saves averages or channels to csv from selected item from all subjects
    """
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    # validate times
    time_arrays = []
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        if not evoked:
            continue

        for mne_evoked in evoked.content.values():
            time_arrays.append(mne_evoked.times)
    assert_arrays_same(time_arrays)

    def handler(selected_option):
        try:
            if selected_option == 'channel_averages':
                save_channel_averages(
                    experiment, selected_name)
            else:
                save_all_channels(
                    experiment, selected_name)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def evoked_info(experiment, data, window):
    """ Fills info element
    """
    try:
        selected_name = data['outputs']['evoked'][0]
        evoked = experiment.active_subject.evoked[selected_name]
        params = evoked.params

        message = ""
        if 'conditions' in params:
            message += 'Conditions: ' + ', '.join(params['conditions']) + '\n'

        if 'groups' in params:
            for key, names in params['groups'].items():
                message += '\nGroup '+ str(key) + ': \n'
                for name in names:
                    message += name + '\n'
        
    except Exception as exc:
        message = ""

    return message

