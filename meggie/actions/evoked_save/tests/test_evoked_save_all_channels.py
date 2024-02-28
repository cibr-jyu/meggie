from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_save import SaveEvoked
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestEvokedSaveAllChannels(BaseTestAction):
    def test_evoked_save_all_channels(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_save",
            handler=SaveEvoked,
            data=data,
            patch_paths=["meggie.actions.evoked_save"],
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
