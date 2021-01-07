"""
"""
import logging

import numpy as np
import mne

from PyQt5 import QtWidgets

from meggie.tabs.preprocessing.dialogs.rereferencingDialogUi import Ui_rereferencingDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.decorators import threaded


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

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def accept(self):
        """
        """
        experiment = self.experiment

        raw = experiment.active_subject.get_raw()
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
            return

        experiment.active_subject.save()
        experiment.active_subject.rereferenced = True

        experiment.save_experiment_settings()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished rereferencing.')
        self.close()

    def acceptBatch(self):
        """
        """
        experiment = self.experiment
        selection = self.ui.comboBoxChannel.currentText()

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    raw = subject.get_raw()

                    @threaded
                    def rereference_fun():
                        if selection == 'Use average':
                            raw.set_eeg_reference(ref_channels='average', 
                                                  projection=False)
                        elif selection == '':
                            raise Exception('Empty selection')
                        else:
                            raw.set_eeg_reference(ref_channels=[selection])

                    rereference_fun(do_meanwhile=self.parent.update_ui)
                    subject.save()
                    subject.rereferenced = True
                    subject.release_memory()

                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        experiment.save_experiment_settings()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished rereferencing.')
        self.close()

