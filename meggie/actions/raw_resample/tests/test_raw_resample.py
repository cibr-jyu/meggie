from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_resample import Resample
from meggie.actions.raw_resample.dialogs.resamplingDialogMain import (
    ResamplingDialog,
)


class TestRawResample(BaseTestAction):
    def test_raw_resample(self):

        self.run_action(
            action_name="raw_resample",
            handler=Resample,
            patch_paths=["meggie.actions.raw_resample.dialogs.resamplingDialogMain"],
        )
        dialog = self.find_dialog(ResamplingDialog)
        dialog.accept()
