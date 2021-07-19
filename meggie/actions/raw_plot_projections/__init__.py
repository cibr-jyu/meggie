""" Contains implementation for raw plot projections
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.messaging import messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotProjections(Action):
    """
    """
    def run(self):

        subject = self.experiment.active_subject
        raw = subject.get_raw()
        if not raw.info['projs']:
            messagebox(self.window, "Data does not contain any projection vectors")
            return

        fig = raw.plot_projs_topomap()

        elems = ['projections', subject.name]
        fig.canvas.set_window_title('_'.join(elems))
        fig.suptitle(' '.join(elems))
