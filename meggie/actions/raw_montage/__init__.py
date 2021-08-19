""" Contains implementation for raw montage
"""
import logging

import matplotlib.pyplot as plt
import numpy as np
import mne

from meggie.utilities.messaging import messagebox
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.threading import threaded

from meggie.actions.raw_montage.dialogs.montageDialogMain import MontageDialog

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action


class Montage(Action):
    """ Shows a dialog for gathering parameters and then
    allows setting montage for EEG.
    """

    @subject_action
    def handler(self, subject, params):
        """
        """
        @threaded
        def montage_fun():
            """
            """
            raw = subject.get_raw()

            head_size = params['head_size']

            if params['custom'] == True:
                montage_fname = params['selection']
                montage = mne.channels.read_custom_montage(
                    montage_fname, head_size=head_size)
            else:
                montage_name = params['selection']
                montage = mne.channels.make_standard_montage(
                    montage_name, head_size=head_size)

            raw.set_montage(montage)
            subject.save()

        montage_fun(do_meanwhile=self.window.update_ui)

    def run(self):
        montage_dialog = MontageDialog(
            self.window, self.experiment, self.handler)
        montage_dialog.show()
