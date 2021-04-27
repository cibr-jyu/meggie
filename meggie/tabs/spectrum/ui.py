import logging

from meggie.utilities.validators import assert_arrays_same
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.names import next_available_name
from meggie.utilities.formats import format_float

from meggie.utilities.dialogs.outputOptionsMain import OutputOptions
from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog
from meggie.utilities.dialogs.powerSpectrumDialogMain import PowerSpectrumDialog
from meggie.utilities.dialogs.permutationTestDialogMain import PermutationTestDialog

from meggie.tabs.spectrum.controller.spectrum import plot_spectrum_topo
from meggie.tabs.spectrum.controller.spectrum import plot_spectrum_averages
from meggie.tabs.spectrum.controller.spectrum import group_average_spectrum
from meggie.tabs.spectrum.controller.spectrum import save_channel_averages
from meggie.tabs.spectrum.controller.spectrum import save_all_channels
from meggie.tabs.spectrum.controller.spectrum import create_power_spectrum
from meggie.tabs.spectrum.controller.spectrum import run_permutation_test

from meggie.utilities.channels import get_channels_by_type


def create(experiment, data, window):
    """ Opens spectrum creation dialog
    """
    default_name = next_available_name(
        experiment.active_subject.spectrum.keys(), 'Spectrum')

    def handler(subject, spectrum_name, params, intervals):
        """ Handles spectrum creation, initiated by the dialog
        """
        create_power_spectrum(subject, spectrum_name, params, intervals,
                              do_meanwhile=window.update_ui)

    dialog = PowerSpectrumDialog(experiment, window, default_name, handler)
    dialog.show()


def delete(experiment, data, window):
    """ Deletes selected spectrum item for active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    try:
        subject.remove(selected_name, 'spectrum')
    except Exception as exc:
        exc_messagebox(window, exc)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted spectrum: ' + selected_name)

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
                logging.getLogger('ui_logger').exception('')
                logging.getLogger('ui_logger').warning(
                    'Could not remove spectrum for ' +
                    subject.name)

    experiment.save_experiment_settings()

    logging.getLogger('ui_logger').info('Deleted spectrum from all subjects: ' + selected_name)

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
                info = experiment.active_subject.get_raw().info
                chs = list(get_channels_by_type(info).keys())
                if 'eeg' in chs:
                    plot_spectrum_topo(experiment, selected_name, ch_type='eeg')
                if 'grad' in chs or 'mag' in chs:
                    plot_spectrum_topo(experiment, selected_name, ch_type='meg')
        except Exception as exc:
            exc_messagebox(window, exc)
            return

        logging.getLogger('ui_logger').info('Plotting spectrum.')

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def group_average(experiment, data, window):
    """ Handles group average item creation
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    name = next_available_name(
        experiment.active_subject.spectrum.keys(), 
        'group_' + selected_name)

    def handler(groups):
        try:
            group_average_spectrum(experiment, selected_name, groups, name,
                                   do_meanwhile=window.update_ui)
            experiment.save_experiment_settings()
            window.initialize_ui()

        except Exception as exc:
            exc_messagebox(window, exc)
            return

        logging.getLogger('ui_logger').info('Finished creating group average spectrum.')
    
    dialog = GroupSelectionDialog(experiment, window, handler)
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
                save_channel_averages(experiment, selected_name, 
                                      do_meanwhile=window.update_ui)
            else:
                save_all_channels(experiment, selected_name, 
                                  do_meanwhile=window.update_ui)
        except Exception as exc:
            exc_messagebox(window, exc)

    dialog = OutputOptions(window, handler=handler)
    dialog.show()


def permutation_test(experiment, data, window):
    """
    """
    try:
        selected_name = data['outputs']['spectrum'][0]
    except IndexError as exc:
        return

    meggie_item = experiment.active_subject.spectrum[selected_name]
    ch_names = meggie_item.ch_names

    def handler(groups, time_limits, frequency_limits, location_limits, threshold,
                significance, n_permutations, design):
        """
        """
        try:
            run_permutation_test(experiment, selected_name, groups, time_limits, 
                                 frequency_limits, location_limits, threshold,
                                 significance, n_permutations, design)
        except Exception as exc:
            exc_messagebox(window, exc)
            return

    dialog = PermutationTestDialog(experiment, window, handler, meggie_item, 
                                   limit_frequency=True, limit_location_vals=ch_names)
    dialog.show()


def spectrum_info(experiment, data, window):
    """
    """
    try:
        selected_name = data['outputs']['spectrum'][0]

        spectrum = experiment.active_subject.spectrum[selected_name]
        params = spectrum.params

        message = ""

        message += "Name: "+ spectrum.name + "\n\n"

        if 'fmin' in params and 'fmax' in params:
            message += 'Frequencies: {0}Hz - {1}Hz\n'.format(format_float(params['fmin']), 
                                                             format_float(params['fmax']))

        if 'nfft' in params:
            message += 'Window length (samples): {0}\n'.format(params['nfft'])

        if 'overlap' in params:
            message += 'Overlap (samples): {0}\n'.format(params['overlap'])

        if 'intervals' in params:
            message += '\nIntervals: \n'
            for key, ivals in params['intervals'].items():
                message += 'Condition ' + str(key) + ': '
                message += ', '.join(['({0}s - {1}s)'.format(format_float(ival[0]), format_float(ival[1]))
                                      for ival in ivals])
                message += '\n'

        if 'groups' in params:
            for key, names in params['groups'].items():
                message += '\nGroup ' + str(key) + ': \n'
                for name in names:
                    message += name + '\n'

    except Exception as exc:
        message = ""

    return message
