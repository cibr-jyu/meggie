from PyQt6 import QtCore

from meggie.utilities.testing import BaseTestAction
from meggie.actions.evoked_group_average import GroupAverage
from meggie.utilities.dialogs.groupSelectionDialogMain import (
    GroupSelectionDialog,
)


class TestEvokedGroupAverage(BaseTestAction):
    def test_evoked_group_average(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_group_average",
            handler=GroupAverage,
            data=data,
        )
        dialog = self.find_dialog(GroupSelectionDialog)

        dialog.ui.checkBoxGroup_0.setCheckState(QtCore.Qt.CheckState.Checked)
        dialog.ui.spinBoxGroup_0.setValue(1)
        dialog.ui.checkBoxGroup_1.setCheckState(QtCore.Qt.CheckState.Checked)
        dialog.ui.spinBoxGroup_1.setValue(1)

        dialog.accept()
