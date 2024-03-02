from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_plot_topomap import PlotEvokedTopomap
from meggie.actions.evoked_plot_topomap.dialogs.evokedTopomapDialogMain import (
    EvokedTopomapDialog,
)


class TestEvokedPlotTopomap(BaseTestAction):
    def test_evoked_plot_topomap(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_plot_topomap",
            handler=PlotEvokedTopomap,
            data=data,
            patch_paths=[
                "meggie.actions.evoked_plot_topomap.dialogs.evokedTopomapDialogMain"
            ],
        )
        dialog = self.find_dialog(EvokedTopomapDialog)
        dialog.accept()
