from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_plot import PlotTFR
from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions


class TestTFRPlotAllChannels(BaseTestAction):
    def test_tfr_plot_all_channels(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_plot",
            handler=PlotTFR,
            data=data,
            patch_paths=["meggie.actions.tfr_plot"],
        )
        dialog = self.find_dialog(TFROutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
