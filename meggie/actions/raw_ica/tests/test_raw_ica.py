from meggie.utilities.testing import BaseTestAction
from meggie.actions.raw_ica import ICA
from meggie.actions.raw_ica.dialogs.icaDialogMain import (
    ICADialog,
)


class TestRawICA(BaseTestAction):
    def test_raw_ica(self):

        self.run_action(
            action_name="raw_ica",
            handler=ICA,
            patch_paths=["meggie.actions.raw_ica.dialogs.icaDialogMain"],
        )
        dialog = self.find_dialog(ICADialog)

        # Compute the components
        dialog.ui.doubleSpinBoxNComponents.setValue(0.3)
        dialog.ui.pushButtonCompute.click()

        # Select first item
        dialog.ui.listWidgetNotRemoved.setCurrentRow(0)

        # Try all the plots
        dialog.ui.pushButtonPlotTopographies.click()
        dialog.ui.pushButtonPlotSources.click()
        dialog.ui.pushButtonPlotProperties.click()

        # Transfer to be removed
        dialog.ui.pushButtonTransfer.click()

        # Try plotting changes
        dialog.ui.pushButtonPlotChanges.click()

        # Finish
        dialog.accept()
