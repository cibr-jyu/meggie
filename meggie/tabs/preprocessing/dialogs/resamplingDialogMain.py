"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.ui.preprocessing.resamplingDialogUi import Ui_resamplingDialog
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.preprocessing.resampling import resample

from meggie.ui.widgets.batchingWidgetMain import BatchingWidget


class ResamplingDialog(QtWidgets.QDialog):

    def __init__(self, parent, experiment):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_resamplingDialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.experiment = experiment

        subject = self.experiment.active_subject
        raw = subject.get_working_file()
        sfreq = raw.info['sfreq']

        self.ui.labelCurrentRateValue.setText(str(sfreq))

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.scrollAreaWidgetContents,
            geometry=self.ui.widgetBatchContainer.geometry())

    def experiment_getter(self):
        return self.experiment

    def accept(self):
        experiment = self.experiment
        raw = experiment.active_subject.get_working_file()
        fname = experiment.active_subject.working_file_path

        old_rate = raw.info['sfreq']
        rate = self.ui.doubleSpinBoxNewRate.value()

        @threaded
        def resample_fun():
            resample(experiment, raw, fname, rate)
        resample_fun(do_meanwhile=self.parent.update_ui)

        logging.getLogger('ui_logger').info('Resampling done successfully from ' +
                                            str(old_rate) + ' to ' + str(rate))

        self.parent.parent.initialize_ui()
        self.close()

    def acceptBatch(self):

        experiment = self.experiment

        selected_subject_names = self.batching_widget.selected_subjects

        recently_active_subject = experiment.active_subject.subject_name

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    experiment.activate_subject(name)
                    raw = subject.get_working_file()
                    fname = subject.working_file_path

                    old_rate = raw.info['sfreq']
                    rate = self.ui.doubleSpinBoxNewRate.value()

                    @threaded
                    def resample_fun():
                        resample(experiment, raw, fname, rate)

                    resample_fun(do_meanwhile=self.parent.update_ui)
                except Exception as e:
                    self.batching_widget.failed_subjects.append(
                        (subject, str(e)))
                    logging.getLogger('ui_logger').exception(str(e))

        experiment.activate_subject(recently_active_subject)

        self.batching_widget.cleanup()

        self.parent.parent.initialize_ui()
        self.close()
