# coding: utf-8

"""
"""
from PyQt4 import QtCore, QtGui
import numpy as np

from meggie.code_meggie.general import fileManager

from meggie.code_meggie.analysis.spectral import create_tfr

from meggie.ui.analysis.TFRDialogUi import Ui_TFRDialog

from meggie.ui.utils.validators import validate_name

from meggie.ui.utils.decorators import threaded
from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox

class TFRDialog(QtGui.QDialog):
    """
    """
    
    def __init__(self, parent, experiment, epoch_name):
        """
        """
        QtGui.QDialog.__init__(self, parent)
        self.ui = Ui_TFRDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.epoch_name = epoch_name
        self.experiment = experiment

        subject = experiment.active_subject
        epochs = subject.epochs[epoch_name].raw

        self.ui.lineEditEpochName.setText(epoch_name)

        if epochs.info.get('highpass'):
            if self.ui.doubleSpinBoxMinFreq.value() < epochs.info['highpass']:
                self.ui.doubleSpinBoxMinFreq.setValue(
                    int(np.ceil(epochs.info['highpass'])))

        if epochs.info.get('lowpass'):
            if self.ui.doubleSpinBoxMaxFreq.value() > epochs.info['lowpass']:
                self.ui.doubleSpinBoxMaxFreq.setValue(
                    int(np.ceil(epochs.info['lowpass'])))


    def accept(self):
        """
        """

        tfr_name = self.ui.lineEditTFRName.text()

        try:
            validate_name(tfr_name)
        except Exception as exc:
            exc_messagebox(self, exc)
            return
        
        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        freqs = np.arange(minfreq, maxfreq, interval)

        subtract_evoked = self.ui.checkBoxSubtractEvoked.isChecked()
        
        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()

        experiment = self.experiment
        subject = experiment.active_subject
        n_jobs = self.parent.preferencesHandler.n_jobs

        @threaded
        def do_tfr(*args, **kwargs):
            create_tfr(experiment, subject, tfr_name, self.epoch_name, 
                       freqs=freqs, decim=decim, ncycles=ncycles, 
                       subtract_evoked=subtract_evoked, n_jobs=n_jobs)
                
        try:             
            do_tfr(do_meanwhile=self.parent.update_ui)
            experiment.save_experiment_settings()
            self.parent.initialize_ui()
        except Exception as e:
            exc_messagebox(self.parent, e)
            return

        self.close()


