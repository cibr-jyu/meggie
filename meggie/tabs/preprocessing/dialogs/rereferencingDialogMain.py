"""
"""
import logging

import numpy as np

from PyQt5 import QtWidgets

from meggie.tabs.preprocessing.dialogs.rereferencingDialogUi import Ui_rereferencingDialog
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.decorators import threaded

import meggie.utilities.mne_wrapper as mne


class RereferencingDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_rereferencingDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.parent = parent

        subject = self.experiment.active_subject
        raw = subject.get_raw()
        sfreq = raw.info['sfreq']

        # fill the combobox
        picks = mne.pick_types(raw.info, eeg=True, meg=False, eog=True)
        ch_names = [ch_name for ch_idx, ch_name in
                    enumerate(raw.info['ch_names']) if ch_idx in picks]

        for ch_name in ch_names:
            self.ui.comboBoxChannel.addItem(ch_name)

    def accept(self):
        experiment = self.experiment

        raw = experiment.active_subject.get_raw()
        path = experiment.active_subject.raw_path

        selection = self.ui.comboBoxChannel.currentText()

        @threaded
        def rereference_fun():
            if selection == 'Use average':
                raw.set_eeg_reference(ref_channels='average', projection=False)
            elif selection == '':
                raise Exception('Empty selection')
            else:
                raw.set_eeg_reference(ref_channels=[selection])

        try:
            rereference_fun(do_meanwhile=self.parent.update_ui)
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            self.close()
            return

        experiment.active_subject.save()

        experiment.active_subject.rereferenced = True
        experiment.save_experiment_settings()

        logging.getLogger('ui_logger').info(
            'Data was successfully rereferenced using setting: ' + selection)

        self.close()
        self.parent.initialize_ui()
