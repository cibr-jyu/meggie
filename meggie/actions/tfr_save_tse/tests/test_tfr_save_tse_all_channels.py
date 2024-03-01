from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_save_tse import SaveTSE
from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions


class TestTFRSaveTSEAllChannels(BaseTestAction):
    def test_tfr_save_tse_all_channels(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_save_tse",
            handler=SaveTSE,
            data=data,
            patch_paths=["meggie.actions.tfr_save_tse"],
        )
        dialog = self.find_dialog(TFROutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
