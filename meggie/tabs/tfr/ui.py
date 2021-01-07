import logging
import os

from meggie.utilities.names import next_available_name
from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox

from meggie.tabs.tfr.controller.tfr import plot_tfr_averages
from meggie.tabs.tfr.controller.tfr import plot_tfr_topo
from meggie.tabs.tfr.controller.tfr import plot_tse_averages
from meggie.tabs.tfr.controller.tfr import plot_tse_topo
from meggie.tabs.tfr.controller.tfr import save_tfr_channel_averages
from meggie.tabs.tfr.controller.tfr import save_tfr_all_channels
from meggie.tabs.tfr.controller.tfr import save_tse_channel_averages
from meggie.tabs.tfr.controller.tfr import save_tse_all_channels
from meggie.tabs.tfr.controller.tfr import group_average_tfr

from meggie.utilities.formats import format_float
from meggie.utilities.formats import format_floats
from meggie.utilities.channels import get_channels_by_type

from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog

from meggie.tabs.tfr.dialogs.TFROutputOptionsMain import TFROutputOptions
from meggie.tabs.tfr.dialogs.TFRDialogMain import TFRDialog


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
        experiment.active_subject.tfr.keys(), stem)

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

    try:
        subject.remove(selected_name, 'tfr')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted selected TFR')

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
                logging.getLogger('ui_logger').exception(str(exc))
                logging.getLogger('ui_logger').warning(
                    'Could not remove tfr for ' +
                    subject.name)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted selected TFR from all subjects')

    window.initialize_ui()


def plot_tfr(experiment, data, window):
    """ Plot TFR topography or averages from selected item
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    def handler(output, condition, blmode, blstart, blend,
                tmin, tmax, fmin, fmax):
        try:
            info = experiment.active_subject.tfr[selected_name].info
            if output == 'all_channels':
                chs = list(get_channels_by_type(info).keys())
                if 'eeg' in chs:
                    plot_tfr_topo(experiment, experiment.active_subject,
                                  selected_name, condition, blmode, blstart, 
                                  blend, tmin, tmax, fmin, fmax, ch_type='eeg')
                if 'grad' in chs or 'mag' in chs:
                    plot_tfr_topo(experiment, experiment.active_subject,
                                  selected_name, condition, blmode, blstart, 
                                  blend, tmin, tmax, fmin, fmax, ch_type='meg')

            else:
                plot_tfr_averages(experiment, experiment.active_subject,
                                  selected_name, condition, blmode, blstart,
                                  blend, tmin, tmax, fmin, fmax)
        except Exception as exc:
            exc_messagebox(window, exc)

        logging.getLogger('ui_logger').info('Plotting TFR')

    dialog = TFROutputOptions(window, experiment, selected_name,
                              handler, ask_condition=True)
    dialog.show()

def plot_tse(experiment, data, window):
    """ Plot TSE topography or averages from selected item
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    def handler(output, condition, blmode, blstart, blend,
                tmin, tmax, fmin, fmax):
        try:
            info = experiment.active_subject.tfr[selected_name].info
            if output == 'all_channels':
                chs = list(get_channels_by_type(info).keys())
                if 'eeg' in chs:
                    plot_tse_topo(experiment, experiment.active_subject, 
                                  selected_name, blmode, blstart, 
                                  blend, tmin, tmax, fmin, fmax, ch_type='eeg')
                if 'grad' in chs or 'mag' in chs:
                    plot_tse_topo(experiment, experiment.active_subject, 
                                  selected_name, blmode, blstart, 
                                  blend, tmin, tmax, fmin, fmax, ch_type='meg')
            else:
                plot_tse_averages(experiment, experiment.active_subject,
                                  selected_name, blmode, blstart,
                                  blend, tmin, tmax, fmin, fmax)
        except Exception as exc:
            exc_messagebox(window, exc)

        logging.getLogger('ui_logger').info('Plotting TSE')

    dialog = TFROutputOptions(window, experiment, selected_name, handler)
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
    assert_arrays_same(freq_arrays, 'Freqs do no match')

    def handler(output, condition, blmode, blstart, blend,
                tmin, tmax, fmin, fmax):
        try:
            if output == 'all_channels':
                save_tfr_all_channels(experiment, selected_name,
                                      blmode, blstart, blend,
                                      tmin, tmax, fmin, fmax,
                                      do_meanwhile=window.update_ui)
            else:
                save_tfr_channel_averages(experiment, selected_name,
                                          blmode, blstart, blend,
                                          tmin, tmax, fmin, fmax,
                                          do_meanwhile=window.update_ui)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = TFROutputOptions(window, experiment, selected_name, handler)
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
    assert_arrays_same(freq_arrays, 'Freqs do no match')

    def handler(output, condition, blmode, blstart, blend,
                tmin, tmax, fmin, fmax):
        try:
            if output == 'all_channels':
                save_tse_all_channels(experiment, selected_name,
                                      blmode, blstart, blend,
                                      tmin, tmax, fmin, fmax,
                                      do_meanwhile=window.update_ui)
            else:
                save_tse_channel_averages(experiment, selected_name,
                                          blmode, blstart, blend,
                                          tmin, tmax, fmin, fmax,
                                          do_meanwhile=window.update_ui)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = TFROutputOptions(window, experiment, selected_name, handler)
    dialog.show()


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    try:
        selected_name = data['outputs']['tfr'][0]
    except IndexError as exc:
        return

    def handler(name, groups):
        try:
            group_average_tfr(experiment, selected_name, groups, name,
                              do_meanwhile=window.update_ui)
            experiment.save_experiment_settings()
            window.initialize_ui()

        except Exception as exc:
            exc_messagebox(window, exc)

        logging.getLogger('ui_logger').info('Finished creating group average TFR.')

    default_name = next_available_name(
        experiment.active_subject.tfr.keys(),
        'group_' + selected_name)
    dialog = GroupAverageDialog(experiment, window, handler, default_name)
    dialog.show()


def tfr_info(experiment, data, window):
    """ Fills info element
    """
    try:
        selected_name = data['outputs']['tfr'][0]

        tfr = experiment.active_subject.tfr[selected_name]
        params = tfr.params

        message = ""
        if 'decim' in params:
            message += 'Decimated by factor: {0}\n'.format(params['decim'])
        if 'evoked_subtracted' in params:
            message += 'Evoked subtracted: {0}\n'.format(params['evoked_subtracted'])
        if 'conditions' in params:
            message += 'Conditions: ' + ', '.join(params['conditions']) + '\n'
        if 'n_cycles' in params:
            message += 'Cycles: ' + ', '.join(format_floats(params['n_cycles'])) + '\n'

        if hasattr(tfr, 'times'):
            message += 'Times: {0}s - {1}s\n'.format(
                format_float(tfr.times[0]), format_float(tfr.times[-1]))

        if hasattr(tfr, 'freqs'):
            message += 'Freqs: {0} - {1}\n'.format(
                format_float(tfr.freqs[0]), format_float(tfr.freqs[-1]))

        if 'groups' in params:
            for key, names in params['groups'].items():
                message += '\nGroup ' + str(key) + ': \n'
                for name in names:
                    message += name + '\n'

    except Exception as exc:
        message = ""

    return message
