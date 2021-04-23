"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.permutationTestDialogUi import Ui_permutationTestDialog
from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog


class PermutationTestDialog(QtWidgets.QDialog):

    def __init__(self, parent, handler):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_permutationTestDialog()
        self.ui.setupUi(self)
        self.handler = handler

    def on_pushButtonGroups_clicked(self, checked=None):
        if checked is None:
            return

    def accept(self):
        """
        """
        self.handler()
