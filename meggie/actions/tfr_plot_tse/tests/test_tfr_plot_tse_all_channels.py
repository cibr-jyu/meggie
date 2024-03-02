from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_plot_tse import PlotTSE
from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions


class TestTFRPlotTSEAllChannels(BaseTestAction):
    def test_tfr_plot_tse_all_channels(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_plot_tse",
            handler=PlotTSE,
            data=data,
            patch_paths=["meggie.actions.tfr_plot_tse"],
        )
        dialog = self.find_dialog(TFROutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(False)
        dialog.accept()
