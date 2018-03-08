'''
Created on 7.1.2015

@author: Kari Aliranta
'''

import logging
import os

from PyQt4 import QtGui

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.ui.source_analysis.stcPlotDialogUi import Ui_stcPlotDialog


from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox


class stcPlotDialog(QtGui.QDialog):
    """
    """

    def __init__(self, experiment, stc_name):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_stcPlotDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.stc_name = stc_name
           
    def accept(self):
        """
        """

        if self.ui.radioButtonInitialTime.isChecked():
            pass
        else:
            pass
        
