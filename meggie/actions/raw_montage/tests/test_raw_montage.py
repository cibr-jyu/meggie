from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_montage import Montage
from meggie.actions.raw_montage.dialogs.montageDialogMain import (
    MontageDialog,
)


class TestRawMontage(BaseTestAction):

    def setup_experiment(self):
        BaseTestAction.setup_experiment(self)
        raw = self.experiment.active_subject.get_raw()

        # rename channels to match the one lucky montage that comes in mne
        raw.rename_channels(
            dict(
                [
                    (old, old.split(" ")[0] + old.split(" ")[1])
                    for old in raw.info["ch_names"]
                ]
            )
        )

    def test_raw_montage(self):

        self.run_action(
            action_name="raw_montage",
            handler=Montage,
            patch_paths=["meggie.actions.raw_montage.dialogs.montageDialogMain"],
        )
        dialog = self.find_dialog(MontageDialog)
        dialog.ui.comboBoxSelectFromList.setCurrentText("mgh60.elc")
        dialog.accept()
