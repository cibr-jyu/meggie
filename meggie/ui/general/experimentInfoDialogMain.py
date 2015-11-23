'''
Created on 9.4.2014

@author: Kari Aliranta
'''

from PyQt4 import QtCore, QtGui
from meggie.ui.general.experimentInfoDialogUi import Ui_experimentInfoDialog
from meggie.code_meggie.general.caller import Caller

class experimentInfoDialog(QtGui.QDialog):
    """
    Dialog for showing general info about the experiment.
    """

    def __init__(self):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_experimentInfoDialog() 
        self.ui.setupUi(self)        
        caller = Caller.Instance()
        self.ui.lineEditExperimentName.setText(caller.experiment.experiment_name)

        self.ui.lineEditExperimentAuthor.setText(caller.experiment.author)

        self.ui.textBrowserExperimentDescription.setText(caller.experiment.description)
        
        
    def on_ButtonClose_clicked(self, checked=None):
        if checked is None: return
        self.close()
