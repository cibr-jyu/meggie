# coding: utf-8

"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from meggie.ui.general.aboutDialogUi import Ui_Dialog


class AboutDialog(QtWidgets.QDialog):
    """
    Dialog to set the preferences for the application. Only allows choosing the
    calibration file for the experiment.
    """

    def __init__(self):
        """
        Constructor
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_Dialog() 
        self.ui.setupUi(self)
        
    def on_pushButtonClose_clicked(self, checked=None):
        if checked is None: return
        self.close()
