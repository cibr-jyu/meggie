# coding: utf-8

"""
"""

import os

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal

from meggie.code_meggie.general.experiment import Experiment
from meggie.ui.general.createExperimentDialogUi import Ui_CreateExperimentDialog

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

 
class CreateExperimentDialog(QtGui.QDialog):
    """
    Class containing the logic for CreateExperimentDialog. It is used for 
    setting up a new experiment for analyzing MEG data.
    """
    fname = ''
    experimentCreated = pyqtSignal(Experiment)
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.fname = ''
        
        # Reference to main dialog window
        self.parent = parent
        
        # Refers to class in file CreateProjecDialog
        self.ui = Ui_CreateExperimentDialog() 
        self.ui.setupUi(self)
                
                
    def accept(self):
        """Send parameters to experimentHandler for the creation of a
        new experiment."""
        
        if self.ui.lineEditExperimentName.text() == '':
            message = 'Give experiment a name.'
            messagebox(self.parent, message)
            return  
        
        expDict = {
            'name': self.ui.lineEditExperimentName.text(),
            'author': self.ui.lineEditAuthor.text(),
            'description': self.ui.textEditDescription.toPlainText()
        }
        try:
            experiment = self.parent.experimentHandler.initialize_new_experiment(
                expDict,
            )
        except Exception as e:
            exc_messagebox(self, e)
        
        self.experimentCreated.emit(experiment)
        self.close()
        
