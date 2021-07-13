""" Contains ICA action handling.
"""
import logging 

import numpy as np
import matplotlib.pyplot as plt

from meggie.actions.ica.dialogs.icaDialogMain import ICADialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class ICA(Action):

    def __init__(self, experiment, data, window, action_spec):
        Action.__init__(self, experiment, data, window, action_spec)

        ica_dialog = ICADialog(window, experiment, on_apply=self.handler)
        ica_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """
        """

