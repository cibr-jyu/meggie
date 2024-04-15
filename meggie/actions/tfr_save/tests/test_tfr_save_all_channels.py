from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_save import SaveTFR
from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions


class TestTFRSaveAllChannels(BaseTestAction):
    def test_tfr_save_all_channels(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_save",
            handler=SaveTFR,
            data=data,
        )
        dialog = self.find_dialog(TFROutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
