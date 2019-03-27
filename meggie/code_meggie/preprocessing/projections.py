"""
"""

import os
import logging

import matplotlib.pyplot as plt
import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.code_meggie.utils.units import get_scaling

from meggie.ui.utils.decorators import threaded


def read_projections(fname):
    """
    """
    projs = mne.read_proj(fname)
    return projs


def preview_projections(raw, projs):
    """
    """
    raw = raw.copy()
    raw.apply_proj()
    raw.info['projs'] = []

    raw.add_proj(projs)
    raw.plot()

def plot_projs_topomap(experiment, raw):
    fig = raw.plot_projs_topomap()
    name = experiment.active_subject.subject_name
    fig.canvas.set_window_title('Projections for ' + name)


