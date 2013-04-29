"""
Created on Apr 29, 2013

@author: jaolpeso
"""

from PyQt4 import QtCore, QtGui
from preferencesDialog_Ui import Ui_Dialog


class PreferencesDialog(QtGui.QDialog):
    """
    Dialog to set the preferences for the program.
    """


    def __init__(self):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)