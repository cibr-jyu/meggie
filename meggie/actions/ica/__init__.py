""" Contains ICA implementation.
"""
import logging 

import numpy as np
import matplotlib.pyplot as plt

from meggie.actions.ica.dialogs.icaDialogMain import ICADialog

from meggie.mainwindow.dynamic import Action


class ICA(Action):
    """
    """


def handler(experiment, data, window, finished):
    """ Opens up the ica dialog.
    """
    subject = experiment.active_subject

    def on_apply():
        finished(subject.name)
        window.initialize_ui()

    ica_dialog = ICADialog(window, experiment, on_apply=on_apply)
    ica_dialog.show()

