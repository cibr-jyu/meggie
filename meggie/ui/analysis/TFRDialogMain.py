# coding: utf-8

"""
"""
from PyQt4 import QtCore, QtGui
import numpy as np

from meggie.code_meggie.general import fileManager

from meggie.code_meggie.analysis.spectral import create_tfr

from meggie.ui.analysis.TFRDialogUi import Ui_TFRDialog

from meggie.ui.utils.validators import validate_name

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
        self.ui.doubleSpinBoxBaselineStart.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineStart.setValue(epochs.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)

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
        
        cmap = str(self.ui.comboBoxCmap.currentText())
        
        if self.ui.groupBoxBaseline.isChecked():
            mode = str(self.ui.comboBoxMode.currentText())
            blstart = self.ui.doubleSpinBoxBaselineStart.value()
            blend = self.ui.doubleSpinBoxBaselineEnd.value()
        else:
            blstart, blend, mode = None, None, None
            
        if self.ui.radioButtonInduced.isChecked():
            reptype = 'average'
        elif self.ui.radioButtonPhase.isChecked():
            reptype = 'itc'

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        freqs = np.arange(minfreq, maxfreq, interval)
        
        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()

        experiment = self.experiment
        subject = experiment.active_subject
                
        try:             
            n_jobs = self.parent.preferencesHandler.n_jobs
            create_tfr(experiment, subject, self.epoch_name, reptype=reptype, 
                       freqs=freqs, decim=decim, mode=mode, blstart=blstart, 
                       blend=blend, ncycles=ncycles, color_map=cmap, 
                       n_jobs=n_jobs)
        except Exception as e:
            exc_messagebox(self.parent, e)
            return

        self.close()


