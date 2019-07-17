# coding: utf-8

"""
"""

import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.utilities.dialogs.createExperimentDialogUi import Ui_CreateExperimentDialog

from meggie.experiment import Experiment
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class CreateExperimentDialog(QtWidgets.QDialog):
    """
    Class containing the logic for CreateExperimentDialog. It is used for
    setting up a new experiment for analyzing MEG data.
    """
    fname = ''
    experimentCreated = QtCore.pyqtSignal(Experiment)

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self)
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
            return

        self.experimentCreated.emit(experiment)
        self.close()
