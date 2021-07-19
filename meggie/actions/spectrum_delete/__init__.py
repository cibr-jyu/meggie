""" Contains implementation for raw plot
"""
import logging

import numpy as np

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class DeleteSpectrum(Action):
    """
    """

    def run(self):

        subject = self.experiment.active_subject

        try:
            selected_name = self.data['outputs']['spectrum'][0]
        except IndexError as exc:
            return

        try:
            self.handler(subject, {'name': selected_name})
        except Exception as exc:
            exc_messagebox(self.window, exc)
            return

        self.experiment.save_experiment_settings()
        self.window.initialize_ui()

    @subject_action
    def handler(self, subject, params):
        subject.remove(params['name'], 'spectrum')


