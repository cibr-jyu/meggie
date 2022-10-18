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

    data = tfr.data
    ch_names = meggie_tfr.ch_names

    sfreq = meggie_tfr.info['sfreq']
    times = meggie_tfr.times
    freqs = meggie_tfr.freqs

    # compared to spectrums, evoked and tse, tfr is plotted with only one condition.
    # it makes the plotting a bit simpler. we will also misuse 
    # AverageTFR object to do the heavy work.

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

            tfr.plot(baseline=bline, mode=mode, title='', 
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
    else:
        dropped_names = [ch_name for ch_idx, ch_name in enumerate(tfr.info['ch_names'])
                         if ch_idx not in mne.pick_types(tfr.info, eeg=False, meg=True)]

    tfr = tfr.copy().drop_channels(dropped_names)

    title = '{0}_{1}_{2}'.format(tfr_name, tfr_condition, ch_type)
    fig = tfr.plot_topo(show=False,
                        baseline=bline, mode=mode,
                        tmin=tmin, tmax=tmax,
                        fmin=fmin, fmax=fmax,
                        title="")

    set_figure_title(fig, title)

    def onclick(event):
        """ hacky way to change title and add colorbar after creation """
        ax = plt.gca()
        fig = plt.gcf()

        channel = plt.getp(ax, 'title')
        ax.set_title('')

        title = ' '.join([tfr_name, channel])
        set_figure_title(fig, title.replace(' ', '_'))
        fig.suptitle(title)

        img = ax.get_images()[0]
        plt.colorbar(mappable=img, ax=ax)

        plt.show(block=False)

    fig.canvas.mpl_connect('button_press_event', onclick)
    fig.show()

