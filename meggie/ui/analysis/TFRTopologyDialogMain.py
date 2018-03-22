# coding: utf-8

"""
Created on Apr 26, 2013

@author: Kari Aliranta, Jaakko Leppakangas
Contains the TFRTopologyDialog-class used for creating TFR-topologies.
"""
from PyQt4 import QtCore, QtGui
import numpy as np

from meggie.code_meggie.general import fileManager

from meggie.code_meggie.analysis.spectral import TFR_topology

from meggie.ui.analysis.TFRtopologyUi import Ui_DialogTFRTopology

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox

class TFRTopologyDialog(QtGui.QDialog):
    """
    """
    
    def __init__(self, parent, epoch_name):
        """
        Initializes the TFR topology dialog.
        
        Keyword arguments:
        
        parent     --   This dialog's parent.
        epoch_name --   The name of a collection of epochs.
        tfr        --   A pre-calculated TFR to plot. Defaults to None.
        """
        QtGui.QDialog.__init__(self, parent)
        self.parent = parent
        self.epoch_name = epoch_name
        self.ui = Ui_DialogTFRTopology()
        self.ui.setupUi(self)

        subject = self.parent.experiment.active_subject
        epochs = subject.epochs[epoch_name].raw
        self.ui.labelEpochName.setText(epoch_name)
        self.ui.doubleSpinBoxScalpTmin.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxScalpTmax.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxScalpTmin.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxScalpTmax.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineStart.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxBaselineStart.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineStart.setValue(epochs.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMinimum(epochs.tmin)
        self.ui.doubleSpinBoxBaselineEnd.setMaximum(epochs.tmax)
        self.ui.doubleSpinBoxBaselineEnd.setValue(0)

    def accept(self):
        """
        """
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

        save_data = self.ui.checkBoxSaveData.isChecked()

        minfreq = self.ui.doubleSpinBoxMinFreq.value()
        maxfreq = self.ui.doubleSpinBoxMaxFreq.value()
        decim = self.ui.spinBoxDecim.value()
        interval = self.ui.doubleSpinBoxFreqInterval.value()
        freqs = np.arange(minfreq, maxfreq, interval)
        
        if self.ui.radioButtonFixed.isChecked():
            ncycles = self.ui.doubleSpinBoxNcycles.value()
        elif self.ui.radioButtonAdapted.isChecked():
            ncycles = freqs / self.ui.doubleSpinBoxCycleFactor.value()

        ch_type = str(self.ui.comboBoxChannels.currentText())

        subject = self.parent.experiment.active_subject
        epochs = subject.epochs[self.epoch_name].raw
                
        scalp = dict()
        if self.ui.groupBoxScalp.isChecked():
            scalp['tmin'] = self.ui.doubleSpinBoxScalpTmin.value()
            scalp['tmax'] = self.ui.doubleSpinBoxScalpTmax.value()
            scalp['fmin'] = self.ui.doubleSpinBoxScalpFmin.value()
            scalp['fmax'] = self.ui.doubleSpinBoxScalpFmax.value()
        else:
            scalp = None
        try:             
            experiment = self.parent.experiment
            n_jobs = self.parent.preferencesHandler.n_jobs
            TFR_topology(experiment, inst=epochs,
                collection_name=self.epoch_name, reptype=reptype, freqs=freqs, 
                decim=decim, mode=mode, blstart=blstart, blend=blend, 
                ncycles=ncycles, ch_type=ch_type, scalp=scalp, 
                color_map=cmap, save_data=save_data, n_jobs=n_jobs)
        except Exception as e:
            exc_messagebox(self.parent, e)


