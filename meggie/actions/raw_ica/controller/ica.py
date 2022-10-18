""" Contains controlling logic for the ICA.
"""

import logging

from copy import deepcopy

import numpy as np
import mne

from meggie.utilities.compare import compare_raws
from meggie.utilities.plotting import set_figure_title


def compute_ica(raw, n_components, method, max_iter, random_state):
    """ Computes ICA using MNE implementation.
    """

    ica = mne.preprocessing.ICA(
        n_components=n_components,
        method=method,
        max_iter=max_iter,
        random_state=random_state)

    ica.fit(raw)
    return ica


def plot_topographies(ica, n_components):
    """ Plots topographies from the ICA solution.
    """

    figs = ica.plot_components(title='')
    for fig in figs:
        set_figure_title(fig, 'ICA topographic maps')

    def update_topography_texts():
        """ Change texts in the axes to match names in the dialog """
        idx = 0
        for fig in figs:
            for ax in fig.get_axes():
                if idx > n_components:
                    return

                ax.set_title('Component ' + str(idx), fontsize=12)
                idx += 1

    update_topography_texts()


def plot_sources(raw, ica):
    """ Plots sources of the ica solution.
    """
    sources = ica.get_sources(raw)
    sources.plot(title='ICA time courses')


def plot_properties(raw, ica, picks):
    """ Plots properties for specific ICA components.
    """
    figs = ica.plot_properties(
        raw, picks)
    for fig in figs:
        set_figure_title(fig, 'ICA properties')

    # fix the names
    idx = 0
    for fig in figs:
        for ax_idx, ax in enumerate(fig.get_axes()):
            if ax_idx == 0:
                ax.set_title("Component " + str(picks[idx]))
                idx += 1
            break


def plot_changes(raw, ica, indices):
    """ Plot a raw comparison plot for ICA solution.
    """
    raw_removed = raw.copy()
    ica.apply(raw_removed, exclude=indices)
    compare_raws(raw, raw_removed)

