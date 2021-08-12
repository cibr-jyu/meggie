""" Contains implementation for raw rereference
"""
import logging

import matplotlib.pyplot as plt
import numpy as np

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.threading import threaded

from meggie.actions.raw_rereference.dialogs.rereferencingDialogMain import RereferencingDialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class Rereference(Action):
    """
    """

    @subject_action
    def handler(self, subject, params):
        """
        """
        @threaded
        def rereference_fun():
            raw = subject.get_raw()
            if params['selection'] == 'Use average':
                raw.set_eeg_reference(ref_channels='average', 
                                      projection=False)
            elif params['selection'] == '':
                raise Exception('Empty selection')
            else:
                raw.set_eeg_reference(ref_channels=[selection])

        rereference_fun(do_meanwhile=self.window.update_ui)
        subject.rereferenced = True
        subject.save()

    def run(self):
        rereference_dialog = RereferencingDialog(
            self.window, self.experiment, self.handler)
        rereference_dialog.show()
