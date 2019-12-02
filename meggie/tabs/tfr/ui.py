import logging
import os

from pprint import pformat

from meggie.tabs.tfr.dialogs.TFRDialogMain import TFRDialog
from meggie.utilities.dialogs.groupAverageDialogMain import GroupAverageDialog


def create(experiment, data, window):
    """ Opens tfr creation dialog
    """
    selected_names = data['inputs']['epochs']

    if not selected_names:
        return

    dialog = TFRDialog(experiment, window, selected_names)
    dialog.show()


def delete(experiment, data, window):
    pass


def delete_from_all(experiment, data, window):
    pass


def plot_tfr(experiment, data, window):
    pass


def plot_tse(experiment, data, window):
    pass


def plot_tfr_averages(experiment, data, window):
    pass


def plot_tse_averages(experiment, data, window):
    pass


def save_tfr(experiment, data, window):
    pass


def save_tse(experiment, data, window):
    pass


def group_average(experiment, data, window):
    pass


def save_tfr_averages(experiment, data, window):
    pass


def save_tse_averages(experiment, data, window):
    pass


def tfr_info(experiment, data, window):
    pass
