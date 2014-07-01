'''
Created on 30.6.2014

@author: Kari Aliranta
'''

from sourceModeling import forwardModels
from forwardModelDialogUi import Ui_Dialog


class ForwardModelDialog(QtGui.QDialog):
    """
    Class containing the logic for forwardModelDialog. It collects parameter
    values for creating forward models and passes them to ***
    
    TODO passes to something that coordinates the MVC structure related
    to views related to forward modeling and saving new forward models to disk.
    
    TODO Removing forward models from disk and view coordination is handled by
    ***
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    
    def accept(self):
        """
        Does the following:

        1. Collects the parameters from the dialog
        2. Passes the parameters to forwardModeling for actual creation of
        forward model.
        """
        
        # tähän se parametrit dictiin ratkaisu