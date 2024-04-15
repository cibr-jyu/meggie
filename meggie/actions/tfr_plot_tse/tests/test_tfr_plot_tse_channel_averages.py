from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_plot_tse import PlotTSE
from meggie.utilities.dialogs.TFROutputOptionsMain import TFROutputOptions


class TestTFRPlotTSEChannelAverages(BaseTestAction):
    def test_tfr_plot_tse_channel_averages(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_plot_tse",
            handler=PlotTSE,
            data=data,
        )
        dialog = self.find_dialog(TFROutputOptions)
        dialog.ui.radioButtonChannelAverages.setChecked(True)
        dialog.accept()
