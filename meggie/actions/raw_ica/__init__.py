""" Contains ICA action handling.
"""
import logging 

import numpy as np
import matplotlib.pyplot as plt

from meggie.actions.raw_ica.dialogs.icaDialogMain import ICADialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class ICA(Action):
    """
    """
    def run(self):
        ica_dialog = ICADialog(self.window, self.experiment, on_apply=self.handler)
        ica_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """

