# coding: latin1
"""
Created on Apr 29, 2013

@author: Janne Pesonen
"""

from PyQt4 import QtCore, QtGui
from preferencesDialog_Ui import Ui_Dialog


class PreferencesDialog(QtGui.QDialog):
    """
    Dialog to set the preferences for the program. Only allows choosing the
    calibration file for the experiment.
    """

    def __init__(self):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)