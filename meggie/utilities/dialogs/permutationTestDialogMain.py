"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.permutationTestDialogUi import Ui_permutationTestDialog
from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog


class PermutationTestDialog(QtWidgets.QDialog):

    def __init__(self, experiment, parent, handler):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_permutationTestDialog()
        self.ui.setupUi(self)

        self.handler = handler
        self.experiment = experiment

        self.groups = {}

    def on_pushButtonGroups_clicked(self, checked=None):
        if checked is None:
            return

        def handler(groups):
            if not groups:
                return

            self.groups = groups
            self.ui.listWidgetGroups.clear()
            for key, names in sorted(groups.items(), key=lambda x: x[0]):
                for name in sorted(names):
                    item_name = str(key) + ": " + str(name)
                    self.ui.listWidgetGroups.addItem(item_name)

        dialog = GroupSelectionDialog(self.experiment, self, handler)
        dialog.show()

    def accept(self):
        """
        """
        if not self.groups:
            messagebox(self, "You should select some groups first")
            return

        if not len(self.groups.keys()) > 1:
            messagebox(self, "You should selected at least two groups")

        self.handler(self.groups)
        self.close()
