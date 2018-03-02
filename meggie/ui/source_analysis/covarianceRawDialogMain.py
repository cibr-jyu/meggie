'''
Created on 7.1.2015

@author: Kari Aliranta, Erkka Heinila
'''

from PyQt4 import QtGui

from meggie.ui.source_analysis.covarianceRawDialogUi import Ui_covarianceRawDialog

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

import os
from pickle import PickleError


class CovarianceRawDialog(QtGui.QDialog):
    """
    The class containing the logic for the dialog for collecting the
    parameters computing the noise covariance for a raw file.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_covarianceRawDialog()
        self.ui.setupUi(self)
           
           
    def accept(self):
        """
        """
        self.close()
        
        
    def on_pushButtonBrowse_clicked(self, checked=None):
        """
        Open file browser for raw data file.
        """
        if checked is None: 
            return

        fname = QtGui.QFileDialog.getOpenFileName(self, 
            'Select raw ' + 'to use')
        self.ui.lineEditRawFile.setText(fname)
        
