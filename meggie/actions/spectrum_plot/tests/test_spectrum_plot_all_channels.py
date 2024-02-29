from meggie.utilities.testing import BaseTestAction
from meggie.actions.spectrum_plot import PlotSpectrum
from meggie.utilities.dialogs.outputOptionsMain import OutputOptions


class TestSpectrumPlotAllChannels(BaseTestAction):
    def test_spectrum_plot_all_channels(self):

        data = {"outputs": {"spectrum": ["Spectrum"]}}

        self.run_action(
            action_name="spectrum_plot",
            handler=PlotSpectrum,
            data=data,
            patch_paths=["meggie.actions.spectrum_plot"],
        )
        dialog = self.find_dialog(OutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
