from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_save import SaveEvoked
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestEvokedSaveChannelAverages(BaseTestAction):
    def test_evoked_save_channel_averages(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_save",
            handler=SaveEvoked,
            data=data,
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(True)
        dialog.accept()
