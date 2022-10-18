""" Contains implementation for raw plot projections
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.plotting import set_figure_title

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotProjections(Action):
    """ Shows a plot of existing projection vectors.
    """
    def run(self):

        subject = self.experiment.active_subject
        try:
            self.handler(subject, {})
        except Exception as exc:
            exc_messagebox(self.window, exc)

    @subject_action
    def handler(self, subject, params):
        raw = subject.get_raw()
        if not raw.info['projs']:
            messagebox(self.window, "Data does not contain any projection vectors")
            return
        fig = raw.plot_projs_topomap()

        elems = ['projections', subject.name]
        set_figure_title(fig, '_'.join(elems))
        fig.suptitle(' '.join(elems))

