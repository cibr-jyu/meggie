'''
Created on 3.5.2016

@author: jaolpeso, erpipehe
'''
import mne

from PyQt4 import QtGui

from meggie.ui.source_analysis.covarianceEpochDialogUi import Ui_covarianceEpochDialog

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class CovarianceEpochDialog(QtGui.QDialog):
    """
    The class containing the logic for the dialog for collecting the
    parameters computing the noise covariance for epoch collection/s.
    """

    def __init__(self, experiment, on_close=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_covarianceEpochDialog()
        self.ui.setupUi(self)
        self.experiment = experiment
        self.on_close = on_close

        epochs = experiment.active_subject.epochs
        for collection_name in epochs.keys():
            item = QtGui.QListWidgetItem(collection_name)
            self.ui.listWidgetEpochs.addItem(item)
            
    def accept(self):
        """
        """
        try:
            collection_name = str(self.ui.listWidgetEpochs.currentItem().text())
            tmin = self.ui.doubleSpinBoxTmin.value()
            tmax = self.ui.doubleSpinBoxTmax.value()
        except Exception as exc:
            messagebox(self, "No epoch collection selected")
            return

        epochs = self.experiment.active_subject.epochs[collection_name].raw

        try:
            noise_cov = mne.compute_covariance(epochs, tmin=tmin, tmax=tmax)
            path = self.experiment.active_subject.covfile_path
            mne.write_cov(path, noise_cov)
        except Exception as exc:
            exc_messagebox(self, exc) 

        if self.on_close:
            self.on_close() 

        self.close()

    def on_listWidgetEpochs_currentItemChanged(self, current_item, **kwargs):

        collection_name = str(current_item.text())

        epochs = self.experiment.active_subject.epochs[collection_name]
        tmin = epochs.params['tmin']
        tmax = 0.0

        self.ui.doubleSpinBoxTmin.setValue(tmin)
        self.ui.doubleSpinBoxTmax.setValue(tmax)

         
