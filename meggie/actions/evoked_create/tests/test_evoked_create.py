from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_create import CreateEvoked
from meggie.utilities.dialogs.simpleDialogMain import SimpleDialog


class TestEvokedCreate(BaseTestAction):
    def test_evoked_create(self):

        data = {"inputs": {"epochs": ["Epochs"]}}

        self.run_action(
            action_name="evoked_create",
            handler=CreateEvoked,
            data=data,
            patch_paths=["meggie.utilities.dialogs.simpleDialogMain"],
        )
        dialog = self.find_dialog(SimpleDialog)
        dialog.accept()
