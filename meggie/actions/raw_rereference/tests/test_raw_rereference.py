from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_rereference import Rereference
from meggie.actions.raw_rereference.dialogs.rereferencingDialogMain import (
    RereferencingDialog,
)


class TestRawRereference(BaseTestAction):
    def test_raw_rereference(self):

        self.run_action(
            action_name="raw_rereference",
            handler=Rereference,
            patch_paths=[
                "meggie.actions.raw_rereference.dialogs.rereferencingDialogMain"
            ],
        )
        dialog = self.find_dialog(RereferencingDialog)
        dialog.accept()
