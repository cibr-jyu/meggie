"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.ui.preprocessing.cropDialogUi import Ui_cropDialog
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded


class CropDialog(QtWidgets.QDialog):
    
    def __init__(self, parent, experiment):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_cropDialog()
        self.ui.setupUi(self)
        self.parent = parent

        self.experiment = experiment

        subject = self.experiment.active_subject
        raw = subject.get_working_file()
        sfreq = raw.info['sfreq']

        
    def accept(self):
        """
        """
        self.close()
        self.parent.parent.initialize_ui()
