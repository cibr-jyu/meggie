"""Contains implementation for delete epochs from all"""

import logging

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class DeleteEpochsFromAll(Action):
    """Deletes epochs with selected name from all subjects"""

    def run(self, params={}):

        try:
            selected_name = self.data["outputs"]["epochs"][0]
        except IndexError:
            return

        for subject in self.experiment.subjects.values():
            if selected_name in subject.epochs:
                try:
                    self.handler(subject, {"name": selected_name})
                except Exception:
                    logging.getLogger("ui_logger").exception("")
                    logging.getLogger("ui_logger").warning(
                        "Could not remove epochs for " + subject.name
                    )

        self.window.initialize_ui()

    @subject_action
    def handler(self, subject, params):
        subject.remove(params["name"], "epochs")
        self.experiment.save_experiment_settings()
