"""Contains ICA action handling."""

from meggie.actions.raw_ica.dialogs.icaDialogMain import ICADialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class ICA(Action):
    """Shows a dialog which can be used to compute ICA decompositions
    and selecting components for removal.
    """

    random_state = 10

    def run(self, params={}):
        ica_dialog = ICADialog(
            self.window, self.experiment, self.random_state, on_apply=self.handler
        )
        ica_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """
