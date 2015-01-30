'''
Created on 30.1.2015

@author: Kari Aliranta
'''



from PyQt4 import QtGui
from forwardModelSkipDialogUi import Ui_DialogForwardModelSkip


class ForwardModelSkipDialog(QtGui.QDialog):
    
    def __init__(self, parent, sSpaceDict, wshedDict):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogForwardModelSkip()
        self.ui.setupUi(self)
        
    
    
        
    
    