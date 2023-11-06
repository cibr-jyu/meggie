""" Contains controlling logic for the tfr implementation
"""

import numpy as np
import matplotlib.pyplot as plt
import mne

from meggie.utilities.plotting import create_channel_average_plot
from meggie.utilities.channels import average_to_channel_groups
from meggie.utilities.plotting import set_figure_title


def plot_tfr_averages(subject, tfr_name, tfr_condition,
                      blmode, blstart, blend,
                      tmin, tmax, fmin, fmax, channel_groups):
    """ Plots tfr averages.
    """

    meggie_tfr = subject.tfr[tfr_name]

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = meggie_tfr.content.get(tfr_condition)

    ch_names = meggie_tfr.ch_names

    sfreq = meggie_tfr.info['sfreq']
    times = meggie_tfr.times
    freqs = meggie_tfr.freqs

    # note: baseline is corrected before channel average
    data = mne.baseline.rescale(tfr.data, times, baseline=bline, mode=mode)

    data_labels, averaged_data = average_to_channel_groups(
        data, meggie_tfr.info, ch_names, channel_groups)

    averages = {}
    for label_idx, label in enumerate(data_labels):
        averages[label] = averaged_data[label_idx]

    ch_types = sorted(set([label[0] for label in data_labels]))
    for ch_type in ch_types:

        ch_groups = sorted([label[1] for label in data_labels
                            if label[0] == ch_type])

        def plot_fun(ax_idx, ax):
            ch_group = ch_groups[ax_idx]
            ax.set_title(ch_group)

            info = mne.create_info(ch_names=['grand_average'], sfreq=sfreq, ch_types='mag')
            tfr = mne.time_frequency.tfr.AverageTFR(info,
                averages[(ch_type, ch_group)][np.newaxis, :], times, freqs, 1)

            # prevent interaction as no topography is involved now
            def onselect(*args, **kwargs):
                pass
            tfr._onselect = onselect

            tfr.plot(baseline=None, title='',
                     fmin=fmin, fmax=fmax,
                     tmin=tmin, tmax=tmax, axes=ax)

        title = ' '.join([tfr_name, tfr_condition, ch_type])
        create_channel_average_plot(len(ch_groups), plot_fun, title)


def plot_tfr_topo(subject, tfr_name, tfr_condition,
                  blmode, blstart, blend,
                  tmin, tmax, fmin, fmax, ch_type):
    """ Plots tfr topography.
    """

    meggie_tfr = subject.tfr[tfr_name]

    if blmode:
        bline = (blstart, blend)
        mode = blmode
    else:
        bline = None
        mode = None

    tfr = meggie_tfr.content.get(tfr_condition)

    if ch_type == 'eeg':
        dropped_names = [ch_name for ch_idx, ch_name in enumerate(tfr.info['ch_names'])
                         if ch_idx not in mne.pick_types(tfr.info, eeg=True, meg=False)]
    elif ch_type == 'grad':
        dropped_names = [ch_name for ch_idx, ch_name in enumerate(tfr.info['ch_names'])
                         if ch_idx not in mne.pick_types(tfr.info, eeg=False, meg='grad')]
    elif ch_type == 'mag':
        dropped_names = [ch_name for ch_idx, ch_name in enumerate(tfr.info['ch_names'])
                         if ch_idx not in mne.pick_types(tfr.info, eeg=False, meg='mag')]

    tfr = tfr.copy().drop_channels(dropped_names)

    # apply baseline here to get better vmin and vmax values
    tfr.apply_baseline(baseline=bline, mode=mode)

    values = tfr.data.flatten()
    vmax = np.percentile(np.abs(values), 99)
    vmin = -vmax

    title = '{0}_{1}_{2}'.format(tfr_name, tfr_condition, ch_type)
    fig = tfr.plot_topo(show=False,
                        baseline=None,
                        tmin=tmin, tmax=tmax,
                        fmin=fmin, fmax=fmax,
                        vmin=vmin, vmax=vmax,
                        title="")

    set_figure_title(fig, title)

    def onclick(event):
        """ hacky way to change title and add colorbar after creation """
        ax = plt.gca()
        fig = plt.gcf()

        channel = plt.getp(ax, 'title')
        if not channel:
            return

        ax.set_title('')

        title = ' '.join([tfr_name, channel])
        set_figure_title(fig, title.replace(' ', '_'))
        fig.suptitle(title)

        img = ax.get_images()[0]
        plt.colorbar(mappable=img, ax=ax)

        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.show()

