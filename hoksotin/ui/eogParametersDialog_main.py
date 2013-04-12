'''
Created on Apr 12, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from eogParametersDialog import Ui_Dialog

class EogParametersDialog(QtGui.QDialog):


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in module eogParametersDialog
        self.ui.setupUi(self)