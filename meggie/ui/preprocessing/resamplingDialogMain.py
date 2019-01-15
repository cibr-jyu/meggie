"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.ui.preprocessing.resamplingDialogUi import Ui_resamplingDialog
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.preprocessing.resampling import resample


class ResamplingDialog(QtWidgets.QDialog):
    
    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_resamplingDialog()
        self.ui.setupUi(self)
        self.parent = parent

        subject = self.parent.experiment.active_subject
        raw = subject.get_working_file()
        sfreq = raw.info['sfreq']

        self.ui.labelCurrentRateValue.setText(str(sfreq))
        
    def accept(self):
        experiment = self.parent.experiment
        raw = experiment.active_subject.get_working_file()
        fname = experiment.active_subject.working_file_path

        rate = self.ui.doubleSpinBoxNewRate.value()

        @threaded
        def resample_fun():
            resample(experiment, raw, fname, rate)
        resample_fun()

        logging.getLogger('ui_logger').info('Resampling done successfully.')

        self.close()
        self.parent.initialize_ui()
