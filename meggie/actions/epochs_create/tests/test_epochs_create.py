from PyQt5 import QtWidgets

from meggie.utilities.testing import BaseTestAction
from meggie.actions.epochs_create import CreateEpochs
from meggie.actions.epochs_create.dialogs.createEpochsFromEventsDialogMain import (
    CreateEpochsFromEventsDialog,
)


class TestEpochsCreate(BaseTestAction):
    def test_epochs_create(self):

        self.run_action(
            action_name="epochs_create",
            handler=CreateEpochs,
            patch_paths=[
                "meggie.actions.epochs_create.dialogs.createEpochsFromEventsDialogMain"
            ],
        )
        dialog = self.find_dialog(CreateEpochsFromEventsDialog)

        event = {"event_id": 1, "mask": 0}
        item = QtWidgets.QListWidgetItem(
            "%s, %s" % ("ID " + str(event["event_id"]), "mask=" + str(event["mask"]))
        )
        dialog.ui.listWidgetEvents.addItem(item)
        dialog.events = [event]

        dialog.accept()
