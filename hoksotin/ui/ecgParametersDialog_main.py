"""
Created on Apr 16, 2013

@author: jaeilepp
"""

from PyQt4 import QtCore,QtGui
from eogParametersDialog import Ui_Dialog

from caller import Caller

class EcgParametersDialog(QtGui.QDialog):


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def accept(self):
        pass

