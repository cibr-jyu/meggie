""" Contains create epochs action handling.
"""

from meggie.utilities.names import next_available_name
from meggie.utilities.threading import threaded

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie.actions.epochs_create.dialogs.createEpochsFromEventsDialogMain import CreateEpochsFromEventsDialog
from meggie.actions.epochs_create.controller.epoching import create_epochs_from_events


class CreateEpochs(Action):
    """ Shows a dialog for event selection and then creates epochs.
    """
    def run(self):
        default_name = next_available_name(
            self.experiment.active_subject.spectrum.keys(), 'Epochs')

        dialog = CreateEpochsFromEventsDialog(self.experiment, self.window, 
                                              default_name, self.handler)
        dialog.show()


    @subject_action
    def handler(self, subject, params):
        """
        """
        @threaded
        def create():
            create_epochs_from_events(subject, params)

        create(do_meanwhile=self.window.update_ui)
