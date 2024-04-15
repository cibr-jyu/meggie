from meggie.utilities.testing import BaseTestAction
from meggie.actions.spectrum_save import SaveSpectrum
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestSpectrumSaveAllChannels(BaseTestAction):
    def test_spectrum_save_all_channels(self):

        data = {"outputs": {"spectrum": ["Spectrum"]}}

        self.run_action(
            action_name="spectrum_save",
            handler=SaveSpectrum,
            data=data,
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
