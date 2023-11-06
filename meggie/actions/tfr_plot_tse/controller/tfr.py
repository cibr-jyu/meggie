""" Contains controlling logic for the tfr implementation
"""

import numpy as np
import matplotlib.pyplot as plt
import mne

from meggie.utilities.plotting import color_cycle
from meggie.utilities.plotting import create_channel_average_plot
from meggie.utilities.plotting import set_figure_title
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.channels import iterate_topography
from meggie.utilities.channels import filter_info
from meggie.utilities.units import get_power_unit


def _compute_tse(meggie_tfr, fmin, fmax):
    tfrs = meggie_tfr.content

    fmin_idx = np.where(meggie_tfr.freqs >= fmin)[0][0]
    fmax_idx = np.where(meggie_tfr.freqs <= fmax)[0][-1]

    if fmax_idx <= fmin_idx:
        raise Exception('Something wrong with the frequencies')

    tses = {}
    for key, tfr in tfrs.items():
        tse = np.mean(tfr.data[:, fmin_idx:fmax_idx+1, :], axis=1)
        tses[key] = tse

    return tses


def _crop_and_correct_to_baseline(tse, blmode, blstart, blend, tmin, tmax, times):
    tmin_idx = np.where(times >= tmin)[0][0]
    tmax_idx = np.where(times <= tmax)[0][-1]

    if blmode:
        if blstart < tmin:
            raise Exception(
                'Baseline start should not be earlier than crop start.')

        if blend > tmax:
            raise Exception(
                'Baseline end should not be later than crop end.')

        # correct to baseline
        tse = mne.baseline.rescale(tse, times, baseline=(blstart, blend), 
                                   mode=blmode)

        # crop
        tse = tse[:, tmin_idx:tmax_idx+1]

    return times[tmin_idx:tmax_idx+1], tse


def plot_tse_topo(subject, tfr_name, blmode, blstart, blend, 
                  tmin, tmax, fmin, fmax, ch_type):
    """ Plots a tse topography.
    """
    meggie_tfr = subject.tfr.get(tfr_name)

    tses = _compute_tse(meggie_tfr, fmin, fmax)

    info = meggie_tfr.info
    if ch_type == 'meg':
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                            if ch_idx in mne.pick_types(info, meg=True, eeg=False)]
    else:
        picked_channels = [ch_name for ch_idx, ch_name in enumerate(info['ch_names'])
                            if ch_idx in mne.pick_types(info, meg=False, eeg=True)]

    info = filter_info(info, picked_channels)

    ch_names = meggie_tfr.ch_names
    colors = color_cycle(len(tses))

    def individual_plot(ax, info_idx, names_idx):
        """
        """
        ch_name = ch_names[names_idx]

        title = ' '.join([tfr_name, ch_name])
        set_figure_title(ax.figure, title.replace(' ', '_'))
        ax.figure.suptitle(title)
        ax.set_title('')

        for color_idx, (key, tse) in enumerate(sorted(tses.items())):
            times, tse = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, meggie_tfr.times)
            ax.plot(times, tse[names_idx], color=colors[color_idx], label=key)
            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        ax.legend()

        ax.set_xlabel('Time (s)')
        ax.set_ylabel('Power ({})'.format(get_power_unit(
            mne.io.pick.channel_type(info, info_idx),
            False
        )))

        plt.show()

    fig = plt.figure()
    for ax, info_idx, names_idx in iterate_topography(
            fig, info, ch_names, individual_plot):

        handles = []
        for color_idx, (key, tse) in enumerate(sorted(tses.items())):
            times, tse = _crop_and_correct_to_baseline(
                tse, blmode, blstart, blend, tmin, tmax, meggie_tfr.times)
            handles.append(ax.plot(times, tse[names_idx], linewidth=0.2, 
                           color=colors[color_idx],
                           label=key)[0])

    fig.legend(handles=handles)
    title = '{0}_{1}'.format(tfr_name, ch_type)
    set_figure_title(fig, title)
    plt.show()


def plot_tse_averages(subject, tfr_name, blmode, blstart, blend,
                      tmin, tmax, fmin, fmax, channel_groups):
    """ Plots tse averages.
    """
    meggie_tfr = subject.tfr.get(tfr_name)

    tses = _compute_tse(meggie_tfr, fmin, fmax)

    ch_names = meggie_tfr.ch_names
    info = meggie_tfr.info
    colors = color_cycle(len(tses))
    conditions = meggie_tfr.content.keys()

    averages = {}
    for key, tse in sorted(tses.items()):

        # note: baseline is corrected before channel average
        times, ch_data = _crop_and_correct_to_baseline(
            tse, blmode, blstart, blend, tmin, tmax, meggie_tfr.times)

        data_labels, averaged_data = average_to_channel_groups(
            ch_data, info, ch_names, channel_groups)

        for label_idx, label in enumerate(data_labels):
            if not label in averages:
                averages[label] = []
            averages[label].append((key, times, averaged_data[label_idx]))

    ch_types = sorted(set([label[0] for label in averages.keys()]))
    for ch_type in ch_types:

        ch_groups = sorted([label[1] for label in averages.keys()
                            if label[0] == ch_type])

        def plot_fun(ax_idx, ax):
            ch_group = ch_groups[ax_idx]
            ax.set_title(ch_group)
            ax.set_xlabel('Time (s)')
            ax.set_ylabel('Power ({})'.format(get_power_unit(
                ch_type, False)))

            for color_idx, (key, times, curve) in enumerate(averages[(ch_type, ch_group)]):
                ax.plot(times, curve, color=colors[color_idx], label=key)

            ax.axhline(0, color='black')
            ax.axvline(0, color='black')

        title = ' '.join([tfr_name, ch_type])
        legend = list(zip(conditions, colors))
        create_channel_average_plot(len(ch_groups), plot_fun, title, 
                                    legend)

    plt.show()

