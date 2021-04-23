"""
"""
import logging

import mne
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from matplotlib.lines import Line2D

from meggie.tabs.evoked.controller.evoked import create_averages
from meggie.tabs.evoked.controller.evoked import plot_channel_averages
from meggie.tabs.evoked.controller.evoked import group_average_evoked
from meggie.tabs.evoked.controller.evoked import save_all_channels
from meggie.tabs.evoked.controller.evoked import save_channel_averages

import meggie.utilities.filemanager as filemanager

from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.plotting import color_cycle
from meggie.utilities.units import get_scaling
from meggie.utilities.units import get_unit
from meggie.utilities.smooth import smooth_signal
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.names import next_available_name

from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions
from meggie.utilities.dialogs.singleChannelDialogMain import SingleChannelDialog
from meggie.tabs.evoked.dialogs.createEvokedDialogMain import CreateEvokedDialog
from meggie.tabs.evoked.dialogs.evokedTopomapDialogMain import EvokedTopomapDialog


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

    try:
        subject.remove(selected_name, 'evoked')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted evoked: ' + selected_name)

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
                logging.getLogger('ui_logger').exception('')
                logging.getLogger('ui_logger').warning(
                    'Could not remove evoked for ' +
                    subject.name)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted evoked from all subjects: ' + selected_name)

    window.initialize_ui()


def _plot_evoked_averages(experiment, evoked):
    plot_channel_averages(experiment, evoked)


def _plot_evoked_topo(experiment, evoked, ch_type):
    """
    """
    evokeds = []
    labels = []
    for key, evok in sorted(evoked.content.items()):

        info = evok.info
        if ch_type == 'eeg':
            dropped_names = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                             if ch_idx not in mne.pick_types(info, eeg=True, meg=False)]
        else:
            dropped_names = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                             if ch_idx not in mne.pick_types(info, eeg=False, meg=True)]

        evok = evok.copy().drop_channels(dropped_names)

        evokeds.append(evok)
        labels.append(key)

    colors = color_cycle(len(evoked.content.keys()))

    # setup legend for subplots
    lines = [Line2D([0], [0], color=colors[idx], label=labels[idx]) 
             for idx in range(len(labels))]
    def onclick(event):
        try:
            # not nice:
            ax = plt.gca()

            channel = plt.getp(ax, 'title')
            ax.set_title('')

            title_elems = [evoked.name, channel]

            ax.legend(handles=lines, loc='upper right')

            ax.figure.canvas.set_window_title('_'.join(title_elems))
            ax.figure.suptitle(title, ' '.join(title_elems))
            plt.show()
        except Exception as exc:
            pass

    fig = mne.viz.plot_evoked_topo(evokeds, color=colors)
    fig.canvas.mpl_connect('button_press_event', onclick)
    title = "{0}_{1}".format(evoked.name, ch_type)
    fig.canvas.set_window_title(title)


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
                info = list(evoked.content.values())[0].info
                chs = list(get_channels_by_type(info).keys())
                if 'eeg' in chs:
                    _plot_evoked_topo(
                        experiment, evoked, ch_type='eeg')
                if 'grad' in chs or 'mag' in chs:
                    _plot_evoked_topo(
                        experiment, evoked, ch_type='meg')
        except Exception as exc:
            exc_messagebox(window, exc)

        logging.getLogger('ui_logger').info('Plotting evoked.')

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

    evoked = subject.evoked.get(selected_name)

    def handler(tmin, tmax, step, radius, evoked):

        for key, evok in sorted(evoked.content.items()):
            channels = get_channels_by_type(evok.info)
            for ch_type in channels.keys():
                title_elems = [selected_name, key, ch_type]
                times = np.arange(tmin, tmax, step)

                # Use custom figure so that mne does not remove the mpl toolbar
                fig = plt.figure()
                axes = []

                # one subplot for each topomap
                for idx in range(len(times)):
                    spec = GridSpec(5, 2*(len(times)+1)).new_subplotspec((1, 2*idx), 
                                                                     rowspan=3, colspan=2)
                    axes.append(fig.add_subplot(spec))

                # and one for colorbar
                spec = GridSpec(5, 2*(len(times)+1)).new_subplotspec((1, 2*len(times)), 
                                                                 rowspan=3, colspan=1)
                axes.append(fig.add_subplot(spec))

                # until there is a good solution to topomap skirts, fix a value
                sphere = None
                if ch_type in ['mag', 'grad']:
                    sphere = radius

                try:
                    fig = mne.viz.plot_evoked_topomap(
                        evok, times=times, ch_type=ch_type,
                        title=' '.join(title_elems), axes=axes, sphere=sphere)
                    fig.canvas.set_window_title('_'.join(title_elems))
                except Exception as exc:
                    exc_messagebox(window, exc)

        logging.getLogger('ui_logger').info('Plotting evoked topomap.')

    dialog = EvokedTopomapDialog(window, evoked, handler)
    dialog.show()

def plot_single_channel(experiment, data, window):
    """ Plots a single channel from selected evoked
    """
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return
    subject = experiment.active_subject
    evokeds = subject.evoked.get(selected_name)
    content = evokeds.content

    info = list(content.values())[0].info

    conditions = [key for key in sorted(content.keys())]

    title = evokeds.name

    ch_names = info['ch_names']
    chs_by_type = get_channels_by_type(info)

    ylims = {}
    scalings = {}
    units = {}
    ch_types = {}
    for ch_name in ch_names:
        ch_type = None

        for key, values in chs_by_type.items():
            if ch_name in values:
                ch_type = key

        if not ch_type:
            continue

        ch_types[ch_name] = ch_type

        ymin, ymax = 0, 0
        idx = info['ch_names'].index(ch_name)
        for mne_evoked in content.values():
            if np.max(mne_evoked.data[idx]) > ymax:
                ymax = np.max(mne_evoked.data[idx])
            if np.min(mne_evoked.data[idx]) < ymin:
                ymin = np.min(mne_evoked.data[idx])

        ylims[ch_name] = (ymin, ymax)
        scalings[ch_name] = get_scaling(ch_type)
        units[ch_name] = get_unit(ch_type)

    colors = color_cycle(len(content.keys()))

    def handler(ch_name, title, legend, ylim, window, window_len):
        try:
            ch_idx = info['ch_names'].index(ch_name)

            # create new evoked based on old
            new_evokeds = []
            for key, evoked in sorted(content.items()):
                new_evoked = evoked.copy()
                
                # smoothen
                if window:
                    new_evoked.data[ch_idx] = smooth_signal(new_evoked.data[ch_idx], 
                        window_len=window_len, window=window)

                new_evoked.comment = legend[key]
                new_evokeds.append(new_evoked)

            ylim = {ch_types[ch_name]: ylim}

            mne.viz.plot_compare_evokeds(new_evokeds, title=title, picks=[ch_idx],
                                         colors=colors, ylim=ylim, show_sensors=False)
        except Exception as exc:
            exc_messagebox(window, exc)

        logging.getLogger('ui_logger').info('Plotting single channel evoked.')

    dialog = SingleChannelDialog(window, handler, title,
                                 ch_names, scalings, units,
                                 ylims, conditions)
    dialog.show()


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    try:
        selected_name = data['outputs']['evoked'][0]
    except IndexError as exc:
        return

    name = next_available_name(
        experiment.active_subject.evoked.keys(), 
        'group_' + selected_name)

    def handler(groups):
        try:
            group_average_evoked(experiment, selected_name, groups, name,
                                 do_meanwhile=window.update_ui)
            experiment.save_experiment_settings()
            window.initialize_ui()

        except Exception as exc:
            exc_messagebox(window, exc)
            return

        logging.getLogger('ui_logger').info('Finished creating group average evoked.')

    dialog = GroupSelectionDialog(experiment, window, handler)
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
                save_channel_averages(experiment, selected_name,
                                      do_meanwhile=window.update_ui)
            else:
                save_all_channels(experiment, selected_name,
                                  do_meanwhile=window.update_ui)
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

