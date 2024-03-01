from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_save import SaveTFR
from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions


class TestTFRSaveChannelAverages(BaseTestAction):
    def test_tfr_save_channel_averages(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_save",
            handler=SaveTFR,
            data=data,
            patch_paths=["meggie.actions.tfr_save"],
        )
        dialog = self.find_dialog(TFROutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(True)
        dialog.accept()
