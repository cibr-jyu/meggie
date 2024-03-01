from PyQt5 import QtCore

from meggie.utilities.testing import BaseTestAction
from meggie.actions.tfr_group_average import GroupAverage
from meggie.utilities.dialogs.groupSelectionDialogMain import (
    GroupSelectionDialog,
)


class TestTFRGroupAverage(BaseTestAction):
    def test_tfr_group_average(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_group_average",
            handler=GroupAverage,
            data=data,
            patch_paths=["meggie.actions.tfr_group_average"],
        )
        dialog = self.find_dialog(GroupSelectionDialog)

        dialog.ui.checkBoxGroup_0.setCheckState(QtCore.Qt.Checked)
        dialog.ui.spinBoxGroup_0.setValue(1)
        dialog.ui.checkBoxGroup_1.setCheckState(QtCore.Qt.Checked)
        dialog.ui.spinBoxGroup_1.setValue(2)

        dialog.accept()
