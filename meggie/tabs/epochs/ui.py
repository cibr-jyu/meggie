"""
"""
import logging

from meggie.utilities.names import next_available_name
from meggie.utilities.formats import format_float

from meggie.tabs.epochs.dialogs.createEpochsFromEventsDialogMain import CreateEpochsFromEventsDialog


def epochs_info(experiment, data, window):
    """ Fills info element
    """
    try:
        selected_name = data['outputs']['epochs'][0]

        epochs = experiment.active_subject.epochs[selected_name]
        params = epochs.params

        message = ""

        message += "Count: {0}\n".format(epochs.count)

        message += 'Baseline: {0}s - {1}s\n'.format(format_float(params['bstart']), 
                                                    format_float(params['bend']))
        message += 'Times: {0}s - {1}s\n'.format(format_float(params['tmin']), 
                                                 format_float(params['tmax']))

        message += '\nReject params: \n'
        if 'grad' in params: 
            message += 'Gradiometers: {}\n'.format(params.get('reject').get('grad'))
        if 'mag' in params:
            message += 'Magnetometers: {}\n'.format(params.get('reject').get('mag'))
        if 'eeg' in params:
            message += 'EEG: {}\n'.format(params.get('reject').get('eeg'))

        if 'events' in params:
            message += '\nCreated from events: \n'
            for event in params.get('events'):
                message += 'ID: {0}, mask: {1}\n'.format(event['event_id'], 
                                                         event['mask'])

    except BaseException:
        message = ""

    return message


def create_from_events(experiment, data, window):
    """ Opens epoch creation dialog
    """

    default_name = next_available_name(
        experiment.active_subject.epochs.keys(), 'Epochs')
    dialog = CreateEpochsFromEventsDialog(experiment, window, default_name)
    dialog.show()


def delete(experiment, data, window):
    """ Deletes selected epochs item from active subject
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['epochs'][0]
    except IndexError as exc:
        return

    subject.remove(selected_name, 'epochs')
    experiment.save_experiment_settings()
    window.initialize_ui()


def delete_from_all(experiment, data, window):
    """ Deletes selected epochs item from all subjects
    """
    try:
        selected_name = data['outputs']['epochs'][0]
    except IndexError as exc:
        return

    for subject in experiment.subjects.values():
        if selected_name in subject.epochs:
            try:
                subject.remove(selected_name, 'epochs')
            except Exception as exc:
                logging.getLogger('ui_logger').warning(
                    'Could not remove epochs for ' +
                    subject.name)
    experiment.save_experiment_settings()
    window.initialize_ui()


def plot_epochs(experiment, data, window):
    """ Plots selected item
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['epochs'][0]
    except IndexError as exc:
        return

    epochs = subject.epochs.get(selected_name)
    epochs.content.plot()


def plot_image(experiment, data, window):
    """ Plots selected item using plot_image
    """
    subject = experiment.active_subject
    try:
        selected_name = data['outputs']['epochs'][0]
    except IndexError as exc:
        return

    epochs = subject.epochs.get(selected_name)
    figs = epochs.content.plot_image()
    for fig in figs:
        ch_type = fig.canvas.get_window_title()
        title = '{0}_{1}'.format(selected_name, ch_type)
        fig.canvas.set_window_title(title)

