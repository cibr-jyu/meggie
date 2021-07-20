""" Contains implementation for delete tfr from all
"""
import logging

import numpy as np

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class DeleteTFRFromAll(Action):
    """
    """

    def run(self):

        try:
            selected_name = self.data['outputs']['tfr'][0]
        except IndexError as exc:
            return

        for subject in self.experiment.subjects.values():
            if selected_name in subject.tfr:
                try:
                    self.handler(subject, {'name': selected_name})
                except Exception as exc:
                    logging.getLogger('ui_logger').exception('')
                    logging.getLogger('ui_logger').warning(
                        'Could not remove TFR for ' +
                        subject.name)

        self.experiment.save_experiment_settings()
        self.window.initialize_ui()

    @subject_action
    def handler(self, subject, params):
        subject.remove(params['name'], 'tfr')


