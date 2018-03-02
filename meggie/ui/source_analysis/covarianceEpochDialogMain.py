'''
Created on 3.5.2016

@author: jaolpeso, erpipehe
'''
from PyQt4 import QtGui

from meggie.ui.source_analysis.covarianceEpochDialogUi import Ui_covarianceEpochDialog

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class CovarianceEpochDialog(QtGui.QDialog):
    """
    The class containing the logic for the dialog for collecting the
    parameters computing the noise covariance for epoch collection/s.
    """

    def __init__(self, experiment):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_covarianceEpochDialog()
        self.ui.setupUi(self)
        self.experiment = experiment

        epochs = experiment.active_subject.epochs
        
        for collection_name in epochs.keys():
            item = QtGui.QListWidgetItem(collection_name)
            self.ui.listWidgetEpochs.addItem(item)
            
    def accept(self):
        """
        """
        pass

