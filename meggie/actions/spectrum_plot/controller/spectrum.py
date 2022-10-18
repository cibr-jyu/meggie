""" Contains functions for plot spectrum action
"""

import mne

import numpy as np
import matplotlib.pyplot as plt

from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import create_channel_average_plot
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import filter_info
from meggie.utilities.plotting import set_figure_title
from meggie.utilities.units import get_power_unit


def plot_spectrum_averages(subject, channel_groups, name, log_transformed=True):
    """ Plots spectrum averages.
    """

    subject_name = subject.name

    spectrum = subject.spectrum.get(name)

    data = spectrum.content
    freqs = spectrum.freqs
    ch_names = spectrum.ch_names 
    info = spectrum.info

    colors = color_cycle(len(data))
    conditions = spectrum.content.keys()

    averages = {}
    for key, psd in sorted(data.items()):

        data_labels, averaged_data = average_to_channel_groups(
            psd, info, ch_names, channel_groups)

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
            ax.set_xlabel('Frequency (Hz)')
            ax.set_ylabel('Power ({})'.format(
                get_power_unit(ch_type, log_transformed)))

            for color_idx, (key, curve) in enumerate(averages[(ch_type, ch_group)]):
                if log_transformed:
                    curve = 10 * np.log10(curve)
                ax.plot(freqs, curve, color=colors[color_idx])

        title = ' '.join([name, ch_type])
        legend = list(zip(conditions, colors))
        create_channel_average_plot(len(ch_groups), plot_fun, title, legend)

    plt.show()


def plot_spectrum_topo(subject, name, log_transformed=True, ch_type='meg'):
    """ Plots spectrum topography.
    """

    subject_name = subject.name
    spectrum = subject.spectrum.get(name)
    data = spectrum.content
    freqs = spectrum.freqs
    ch_names = spectrum.ch_names
    info = spectrum.info
    if ch_type == 'meg':
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                           if ch_idx in mne.pick_types(info, meg=True, eeg=False)]
    else:
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                           if ch_idx in mne.pick_types(info, eeg=True, meg=False)]

    info = filter_info(info, picked_channels)

    colors = color_cycle(len(data))

    def individual_plot(ax, info_idx, names_idx):
        """
        """
        ch_name = ch_names[names_idx]
        for color_idx, (key, psd) in enumerate(sorted(data.items())):

            if log_transformed:
                curve = 10 * np.log10(psd[names_idx])
            else:
                curve = psd[names_idx]

            ax.plot(freqs, curve, color=colors[color_idx],
                    label=key)

        title = ' '.join([name, ch_name])
        set_figure_title(ax.figure, title.replace(' ', '_'))
        ax.figure.suptitle(title)
        ax.set_title('')

        ax.legend()
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(info, info_idx),
            log_transformed
        )))

        plt.show()

    fig = plt.figure()

    for ax, info_idx, names_idx in iterate_topography(
            fig, info, ch_names, individual_plot):

        handles = []
        for color_idx, (key, psd) in enumerate(sorted(data.items())):

            if log_transformed:
                curve = 10 * np.log10(psd[names_idx])
            else:
                curve = psd[names_idx]

            handles.append(ax.plot(curve, color=colors[color_idx],
                                   linewidth=0.5, label=key)[0])

    if not handles:
        return

    fig.legend(handles=handles)
    title = '{0}_{1}'.format(name, ch_type)
    set_figure_title(fig, title)
    plt.show()

