""" Contains controlling logic for the evoked plot
"""

import mne
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D

from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import create_channel_average_plot
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.plotting import set_figure_title

from meggie.utilities.units import get_unit


def _create_averages(mne_evoked, channel_groups):
    mne_evoked = mne_evoked.copy().drop_channels(mne_evoked.info['bads'])

    data_labels, averaged_data = average_to_channel_groups(
        mne_evoked.data, mne_evoked.info, 
        mne_evoked.info['ch_names'], channel_groups)

    return data_labels, averaged_data


def plot_evoked_averages(evoked, channel_groups):
    """ Plots channel averages.
    """
    conditions = evoked.content.keys()
    colors = color_cycle(len(conditions))
    times = evoked.times

    averages = {}
    for key, mne_evoked in sorted(evoked.content.items()):
        data_labels, averaged_data = _create_averages(mne_evoked, channel_groups)

        for label_idx, label in enumerate(data_labels):
            if not label in averages:
                averages[label] = []
            averages[label].append((key, averaged_data[label_idx]))

    ch_types = sorted(set([label[0] for label in averages.keys()]))
    for ch_type in ch_types:

        ch_groups = sorted([label[1] for label in averages.keys() 
                            if label[0] == ch_type])

        def plot_fun(ax_idx, ax):
            ch_group = ch_groups[ax_idx]
            ax.set_title(ch_group)

            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Amplitude ({})'.format(
                get_unit(ch_type)))

            for color_idx, (key, curve) in enumerate(averages[(ch_type, ch_group)]):
                ax.plot(times, curve, color=colors[color_idx])

            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        title = ' '.join([evoked.name, ch_type])
        legend = list(zip(conditions, colors))
        create_channel_average_plot(len(ch_groups), plot_fun, title, 
                                    legend)

    plt.show()


def plot_evoked_topo(evoked, ch_type):
    """ Plots evoked time courses arranged as a topography """
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

    fig, axes = plt.subplots()
    mne.viz.plot_evoked_topo(evokeds, color=colors, legend=False, show=False, axes=axes)
    axes.legend(handles=lines, loc='upper right')
    title = "{0}_{1}".format(evoked.name, ch_type)
    set_figure_title(fig, title)

    def onclick(event):
        try:
            # not nice:
            ax = plt.gca()

            if ax is axes:
                return

            channel = plt.getp(ax, 'title')
            ax.set_title('')

            ax.legend(handles=lines, loc='upper right')

            title = ' '.join([evoked.name, channel])
            ax.figure.suptitle(title)
            set_figure_title(ax.figure, title.replace(' ', '_'))
            plt.show()
        except Exception as exc:
            pass

    fig.canvas.mpl_connect('button_press_event', onclick)

    plt.show()

