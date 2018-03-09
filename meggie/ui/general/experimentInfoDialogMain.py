'''
Created on 9.4.2014

@author: Kari Aliranta
'''

from PyQt4 import QtCore, QtGui
from meggie.ui.general.experimentInfoDialogUi import Ui_experimentInfoDialog

class ExperimentInfoDialog(QtGui.QDialog):
    """
    Dialog for showing general info about the experiment.
    """

    def __init__(self, parent):
        """
        """
        QtGui.QDialog.__init__(self)
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
