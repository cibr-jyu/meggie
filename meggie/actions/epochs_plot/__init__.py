""" Contains implementation for epochs plot
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class PlotEpochs(Action):
    """ Plots all epochs from all channels.
    """

    def run(self):

        try:
            selected_name = self.data['outputs']['epochs'][0]
        except IndexError as exc:
            return

        subject = self.experiment.active_subject
        try:
            self.handler(subject, {'name': selected_name})
        except Exception as exc:
            exc_messagebox(self.window, exc)


    @subject_action
    def handler(self, subject, params):
        epochs = subject.epochs.get(params['name'])
        epochs.content.plot()

