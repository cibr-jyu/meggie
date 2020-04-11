"""
"""

import logging

from copy import deepcopy

import numpy as np
import mne

from meggie.utilities.compare import compare_raws


def compute_ica(raw, n_components, method, max_iter):
    """
    """
    ica = mne.preprocessing.ICA(
        n_components=n_components,
        method=method,
        max_iter=max_iter)

    ica.fit(raw)

    # TODO: what if ica does not converge?

    return ica


def plot_topographies(ica, n_components):
    """
    """

    figs = ica.plot_components()

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
    """
    """
    sources = ica.get_sources(raw)

    # alter amplitudes to get better plot, this is heuristic
    for source in sources._data:
        for idx, amplitude in enumerate(source):
            source[idx] = amplitude / 5000.0

    sources.plot()


def plot_properties(raw, ica, picks):
    """
    """
    figs = ica.plot_properties(
        raw, picks)

    # fix the names
    idx = 0
    for fig in figs:
        for ax_idx, ax in enumerate(fig.get_axes()):
            if ax_idx == 0:
                ax.set_title("Component " + str(picks[idx]))
                idx += 1
            break


def plot_changes(raw, ica, indices):
    """
    """
    raw_removed = raw.copy()
    ica.apply(raw_removed, exclude=indices)
    compare_raws(raw, raw_removed)


def apply_ica(raw, experiment, ica, indices):
    """
    """
    ica.apply(raw, exclude=indices)

    experiment.active_subject.save()
