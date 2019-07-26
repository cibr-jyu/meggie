"""
"""
import logging

import mne
import matplotlib.pyplot as plt 

from meggie.utilities.channels import read_layout
from meggie.utilities.channels import get_channels

from meggie.tabs.evoked.dialogs.createEvokedDialogMain import CreateEvokedDialog


def create(experiment, data, window):
    selected_names = data['inputs']['epochs']

    if not selected_names:
        return

    dialog = CreateEvokedDialog(experiment, window, selected_names)
    dialog.show()


def delete(experiment, data, window):
    pass


def delete_from_all(experiment, data, window):
    pass


def plot_topo(experiment, data, window):
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

    fig = mne.plot_evoked_topo(evokeds)
    fig.canvas.mpl_connect('button_press_event', onclick)

def plot_topomap(experiment, data, window):
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
            mne.plot_evoked_topomap(
                evoked, ch_type=ch_type, layout=layout,
                title=title)


def group_average(experiment, data, window):
    pass


def save(experiment, data, window):
    pass


def save_from_all(experiment, data, window):
    pass


def evoked_info(experiment, data, window):
    return ""

