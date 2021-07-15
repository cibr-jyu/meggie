""" Contains implementation for raw plot
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.decorators import threaded

from meggie.actions.resample.dialogs.resamplingDialogMain import ResamplingDialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class Resample(Action):
    """
    """

    @subject_action
    def handler(self, subject, params):
        """
        """
        @threaded
        def resample_fun():
            subject.get_raw().resample(params['rate'])

        try:
            resample_fun(do_meanwhile=self.window.update_ui)
            subject.save()
        except Exception as exc:
            exc_messagebox(self, exc)

    def run(self):
        resampling_dialog = ResamplingDialog(
            self.window, self.experiment, self.handler)
        resampling_dialog.show()
