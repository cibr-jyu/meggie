"""
"""
import logging
import os

from pprint import pformat

import mne
import matplotlib.pyplot as plt 

from meggie.tabs.evoked.controller.evoked import create_averages

import meggie.utilities.filemanager as filemanager

from meggie.utilities.channels import read_layout
from meggie.utilities.channels import get_channels
from meggie.utilities.validators import assert_array_lengths

from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog
from meggie.tabs.evoked.dialogs.createEvokedDialogMain import CreateEvokedDialog


def create(experiment, data, window):
    """ Opens evoked creation dialog
    """
    selected_names = data['inputs']['epochs']

    if not selected_names:
        return

    dialog = CreateEvokedDialog(experiment, window, selected_names)
    dialog.show()


def delete(experiment, data, window):
    """ Deletes selected evoked item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    subject.remove(selected_name, 'epochs')
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
        if selected_name in subject.epochs:
            try:
                subject.remove(selected_name, 'evoked')
            except Exception as exc:
                logging.getLogger('ui_logger').warning(
                    'Could not remove evoked for ' +
                    subject.name)
    experiment.save_experiment_settings()
    window.initialize_ui()


def plot_averages(experiment, data, window):
    """ Plots channel averages of selected item 
    """
    pass


def plot_topo(experiment, data, window):
    """ Plots topo of selected item
    """
    subject = experiment.active_subject

    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    evoked = subject.evoked.get(selected_name)

    evokeds = []
    for key, evoked in evoked.content.items():
        evokeds.append(evoked)

    def onclick(event):
        plt.show()

    fig = mne.viz.plot_evoked_topo(evokeds)
    fig.canvas.mpl_connect('button_press_event', onclick)


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
            title = key + ' (' + ch_type + ')'
            mne.viz.plot_evoked_topomap(
                evoked, ch_type=ch_type, layout=layout,
                title=title)


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    subject = experiment.active_subject

    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    # evoked = subject.evoked.get(selected_name)

    def handler(groups):
        pass
        # varmista että threaded kaikkialla mahollisessa käytössä
        # group averarge
        # save
        # initialize ui
        # save experiment settings

    dialog = GroupAverageDialog(experiment, handler)
    dialog.show()


def save(experiment, data, window):
    """ Saves all channels to csv from selected item
    """
    column_names = []
    row_names = []
    csv_data = []

    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    subject = experiment.active_subject
    evoked = subject.evoked.get(selected_name)

    for key, mne_evoked in evoked.content.items():
        csv_data.extend(mne_evoked.data.tolist())
        column_names = mne_evoked.times.tolist()

        for ch_name in mne_evoked.info['ch_names']:
            name = key + '[' + ch_name + ']'
            if ch_name in mne_evoked.info['bads']:
                name = name + ' (bad)'
            row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = subject.name + '_' + evoked.name + '.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_from_all(experiment, data, window):
    """ Saves all channels to csv from selected item from all subjects
    """
    column_names = []
    row_names = []
    csv_data = []

    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    # validate array lengths
    time_arrays = []
    for subject in experiment.subjects.values():
        try:
            evoked = subject.evoked.get(selected_name)
        except Exception as exc:
            continue
        for mne_evoked in evoked.content.values():
            time_arrays.append(mne_evoked.times)
    assert_array_lengths(time_arrays)

    # accumulate csv contents
    for subject in experiment.subjects.values():
        try:
            evoked = subject.evoked.get(selected_name)
        except Exception as exc:
            continue

        for key, mne_evoked in evoked.content.items():
            csv_data.extend(mne_evoked.data.tolist())
            column_names = mne_evoked.times.tolist()

            for ch_name in mne_evoked.info['ch_names']:
                name = subject.name + '{' + key + '}' + '[' + ch_name + ']'
                if ch_name in mne_evoked.info['bads']:
                    name = name + ' (bad)'
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = 'all_subjects_' + evoked.name + '.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_averages(experiment, data, window):
    """ Saves averages to csv from selected item
    """
    column_names = []
    row_names = []
    csv_data = []

    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    subject = experiment.active_subject
    evoked = subject.evoked.get(selected_name)

    # accumulate csv contents
    for key, mne_evoked in evoked.content.items():

        data_labels, averaged_data = create_averages(experiment, mne_evoked)

        csv_data.extend(averaged_data.tolist())
        column_names = mne_evoked.times.tolist()

        for ch_type, area in data_labels:
            name = key + '[' + ch_type + '|' + area + ']'
            row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = subject.name + '_' + evoked.name + '.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def save_averages_from_all(experiment, data, window):
    """ Saves averages to csv from selected item from all subjects
    """
    column_names = []
    row_names = []
    csv_data = []

    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    # validate array lengths
    time_arrays = []
    for subject in experiment.subjects.values():
        try:
            evoked = subject.evoked.get(selected_name)
        except Exception as exc:
            continue
        for mne_evoked in evoked.content.values():
            time_arrays.append(mne_evoked.times)
    assert_array_lengths(time_arrays)

    # accumulate csv contents
    for subject in experiment.subjects.values():
        evoked = subject.evoked.get(selected_name)
        for key, mne_evoked in evoked.content.items():

            data_labels, averaged_data = create_averages(experiment, mne_evoked)

            csv_data.extend(averaged_data.tolist())
            column_names = mne_evoked.times.tolist()

            for ch_type, area in data_labels:
                name = (subject.name + '{' + key + '}' + '[' + 
                        ch_type + '|' + area + ']')
                row_names.append(name)

    folder = filemanager.create_timestamped_folder(experiment)
    fname = 'all_subjects_' + evoked.name + '.csv'
    path = os.path.join(folder, fname)

    filemanager.save_csv(path, csv_data, column_names, row_names)
    logging.getLogger('ui_logger').info('Saved the csv file to ' + path)


def evoked_info(experiment, data, window):
    """ Fills info element
    """
    try:
        selected_name = data['outputs']['evoked'][0]
        evoked = experiment.active_subject.evoked[selected_name]
        filtered = {key: evoked.params[key] for key in ['event_names']}
        message = pformat(filtered)
    except Exception as exc:
        message = ""

    return message

