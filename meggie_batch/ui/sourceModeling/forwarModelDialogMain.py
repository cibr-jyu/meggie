'''
Created on 30.6.2014

@author: Kari Aliranta
'''



from forwardModelDialogUi import Ui_Dialog


class ForwardModelDialog(QtGui.QDialog):
    """
    Class containing the logic for forwardModelDialog. It collects parameter
    values for creating forward models and coordinates the MVC structure related
    to views related to forward modeling and saving new forward models to disk.
    
    Removing forward models from disk and view coordination is handled by
    MainWindowMain. 
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    
    def accept(self):
        """
        Does the following:
        
        
        """
        