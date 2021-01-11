"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.tabs.preprocessing.dialogs.resamplingDialogUi import Ui_resamplingDialog
from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.decorators import threaded


class ResamplingDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment):
        """
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_resamplingDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.parent = parent

        subject = self.experiment.active_subject
        raw = subject.get_raw()
        sfreq = raw.info['sfreq']

        self.ui.labelCurrentRateValue.setText(str(sfreq))

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def accept(self):
        subject = self.experiment.active_subject
        raw = subject.get_raw()

        old_rate = raw.info['sfreq']
        rate = self.ui.doubleSpinBoxNewRate.value()

        try:

            @threaded
            def resample_fun():
                raw.resample(rate)

            resample_fun(do_meanwhile=self.parent.update_ui)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        subject.save()
        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished resampling.')
        self.close()

    def acceptBatch(self):

        experiment = self.experiment

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    raw = subject.get_raw()
                    old_rate = raw.info['sfreq']
                    rate = self.ui.doubleSpinBoxNewRate.value()

                    @threaded
                    def resample_fun():
                        raw.resample(rate)
                        subject.save()
                        subject.release_memory()

                    resample_fun(do_meanwhile=self.parent.update_ui)
                except Exception as exc:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(exc)))
                    logging.getLogger('ui_logger').exception('')

        self.batching_widget.cleanup()

        self.parent.initialize_ui()

        logging.getLogger('ui_logger').info('Finished resampling.')
        self.close()
