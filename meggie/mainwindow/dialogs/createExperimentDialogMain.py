# coding: utf-8

"""
"""

import os

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from meggie.mainwindow.dialogs.createExperimentDialogUi import Ui_CreateExperimentDialog

from meggie.experiment import initialize_new_experiment

from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox


class CreateExperimentDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)

        # Reference to main dialog window
        self.parent = parent

        # Refers to class in file CreateProjecDialog
        self.ui = Ui_CreateExperimentDialog()
        self.ui.setupUi(self)

    def accept(self):
        """ Send parameters to initialize_new_experiment. """

        if self.ui.lineEditExperimentName.text() == '':
            message = 'Give experiment a name.'
            messagebox(self.parent, message)
            return

        try:
            experiment = initialize_new_experiment(
                self.ui.lineEditExperimentName.text(),
                self.ui.lineEditAuthor.text(),
                self.parent.prefs
            )
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.experiment = experiment
        self.parent.initialize_ui()
        self.close()
