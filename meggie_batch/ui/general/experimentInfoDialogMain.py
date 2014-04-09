'''
Created on 9.4.2014

@author: Kari Aliranta
'''

from PyQt4 import QtCore, QtGui
from experimentInfoDialogUi import Ui_experimentInfoDialog


class experimentInfoDialog(QtGui.QDialog):
    """
    Dialog for showing general info about the experiment.
    """

    def __init__(self,parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_experimentInfoDialog() 
        self.ui.setupUi(self)
        self.parent = parent
        
        
        self.ui.lineEditExperimentName.setText(self.parent.experiment.experiment_name)

        self.ui.lineEditExperimentAuthor.setText(self.parent.experiment.author)

        self.ui.textBrowserExperimentDescription.setText(self.parent.experiment.description)
        
        
    def on_ButtonClose_clicked(self, checked=None):
        if checked is None: return
        self.close()