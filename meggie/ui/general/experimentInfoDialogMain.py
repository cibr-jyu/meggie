"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from meggie.ui.general.experimentInfoDialogUi import Ui_experimentInfoDialog

class ExperimentInfoDialog(QtWidgets.QDialog):
    """
    Dialog for showing general info about the experiment.
    """

    def __init__(self, parent):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_experimentInfoDialog() 
        self.ui.setupUi(self)        
        self.parent = parent
        self.ui.lineEditExperimentName.setText(parent.experiment.experiment_name)

        self.ui.lineEditExperimentAuthor.setText(parent.experiment.author)

        self.ui.textBrowserExperimentDescription.setText(parent.experiment.description)
        
        
    def on_ButtonClose_clicked(self, checked=None):
        if checked is None: 
            return

        self.close()
