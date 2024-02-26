from meggie.utilities.testing import BaseTestAction
from meggie.actions.epochs_plot_image import PlotEpochsImage


class TestPlotEpochsImage(BaseTestAction):
    def test_epochs_plot_image(self):

        data = {"outputs": {"epochs": ["Epochs"]}}

        self.run_action(
            action_name="epochs_plot_image",
            handler=PlotEpochsImage,
            data=data,
            patch_paths=["meggie.actions.epochs_plot_image"],
        )
