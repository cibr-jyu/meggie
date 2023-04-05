""" Contains implementation for evoked topomaps
"""
import logging

import matplotlib.pyplot as plt
import numpy as np
import mne

from matplotlib.gridspec import GridSpec

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.channels import get_channels_by_type
from meggie.utilities.plotting import set_figure_title

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.evoked_plot_topomap.dialogs.evokedTopomapDialogMain import EvokedTopomapDialog


class PlotEvokedTopomap(Action):
    """ Plots a sequence of topomaps.
    """

    def run(self):

        try:
            selected_name = self.data['outputs']['evoked'][0]
        except IndexError as exc:
            return

        subject = self.experiment.active_subject
        evoked = subject.evoked.get(selected_name)

        def handle_close(tmin, tmax, step, radius):
            params = {}
            params['tmin'] = tmin
            params['tmax'] = tmax
            params['step'] = step
            params['radius'] = radius
            params['name'] = selected_name

            self.handler(subject, params)

        dialog = EvokedTopomapDialog(self.window, evoked, handle_close)
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        name = params['name']
        tmin = params['tmin']
        tmax = params['tmax']
        step = params['step']
        radius = params['radius']
        evoked = subject.evoked.get(name)

        for key, evok in sorted(evoked.content.items()):
            channels = get_channels_by_type(evok.info)
            for ch_type in channels.keys():
                title_elems = [name, key, ch_type]
                times = np.arange(tmin, tmax, step)

                # Use custom figure so that mne does not remove the mpl toolbar
                fig = plt.figure()
                axes = []

                # one subplot for each topomap
                for idx in range(len(times)):
                    spec = GridSpec(5, 2*(len(times)+1)).new_subplotspec((1, 2*idx),
                                                                     rowspan=3, colspan=2)
                    axes.append(fig.add_subplot(spec))

                # and one for colorbar
                spec = GridSpec(5, 2*(len(times)+1)).new_subplotspec((1, 2*len(times)),
                                                                 rowspan=3, colspan=1)
                axes.append(fig.add_subplot(spec))

                # until there is a good solution to topomap skirts, fix a value
                sphere = None
                if ch_type in ['mag', 'grad']:
                    sphere = radius

                fig = evok.plot_topomap(
                    times=times, ch_type=ch_type,
                    axes=axes, sphere=sphere)
                set_figure_title(fig, '_'.join(title_elems))
