from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_create import CreateTFR
from meggie.actions.tfr_create.dialogs.TFRDialogMain import TFRDialog


class TestTFRCreate(BaseTestAction):
    def test_tfr_create(self):

        data = {"inputs": {"epochs": ["Epochs"]}}

        self.run_action(
            action_name="tfr_create",
            handler=CreateTFR,
            data=data,
            patch_paths=["meggie.actions.tfr_create.dialogs.TFRDialogMain"],
        )
        dialog = self.find_dialog(TFRDialog)
        dialog.ui.radioButtonFixed.setChecked(True)
        dialog.ui.doubleSpinBoxMinFreq.setValue(20)
        dialog.ui.doubleSpinBoxMaxFreq.setValue(40)
        dialog.ui.doubleSpinBoxNcycles.setValue(1.0)
        dialog.accept()
