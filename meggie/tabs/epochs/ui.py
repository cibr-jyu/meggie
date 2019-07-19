"""
"""
from pprint import pformat


def epochs_info(experiment, data, parent):

    try:
        for key, values in data['outputs']:
            if key == 'epochs':
                selected_name = values[0]
                break
        epochs = experiment.active_subject.epochs[selected_name]
        params = epochs.params

        filtered = {key: params[key] for key in 
                    ['bstart', 'bend', 'tmin', 'tmax', 'events']}
        message = pformat(filtered)
    except:
        message = ""

    return message


def create(experiment, data, parent):
    pass


def delete(experiment, data, parent):
    pass


def delete_from_all(experiment, data, parent):
    pass


def plot_epochs(experiment, data, parent):
    pass
