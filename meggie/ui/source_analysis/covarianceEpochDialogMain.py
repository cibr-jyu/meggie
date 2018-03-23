'''
Created on 3.5.2016

@author: jaolpeso
'''
import os
import logging

from PyQt4 import QtGui

from meggie.ui.source_analysis.covarianceEpochDialogUi import Ui_covarianceEpochDialog

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.ui.utils.decorators import threaded
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class CovarianceEpochDialog(QtGui.QDialog):
    """
    The class containing the logic for the dialog for collecting the
    parameters computing the covariance for epoch collection/s.
    """

    def __init__(self, parent, experiment, on_close=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_covarianceEpochDialog()
        self.ui.setupUi(self)
        self.parent = parent
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
            messagebox(self, "No epoch collection selected", exec_=True)
            return

        epochs = self.experiment.active_subject.epochs[collection_name].raw

        name = str(self.ui.lineEditName.text()) + '-cov.fif'
        if name in self.experiment.active_subject.get_covfiles():
            messagebox(self, "Covariance matrix of this name already exists", 
                       exec_=True)
            return

        try:
            @threaded
            def compute_cov():
                cov = mne.compute_covariance(epochs, tmin=tmin, tmax=tmax)
                path = os.path.join(self.experiment.active_subject.cov_directory,
                                    name)

                mne.write_cov(path, cov)

            compute_cov(do_meanwhile=self.parent.parent.update_ui)

        except Exception as exc:
            exc_messagebox(self, exc, exec_=True) 
            return

     
        logging.getLogger('ui_logger').info('Covariance matrix has been successfully computed.')

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
         
