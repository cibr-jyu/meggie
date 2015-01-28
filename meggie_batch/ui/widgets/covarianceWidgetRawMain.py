"""
Created on 27.1.2015

@author: Kari Aliranta
"""

from PyQt4 import QtCore, QtGui
from covarianceWidgetRawUi import Ui_covarianceRawWidget


class CovarianceWidgetRaw(QtGui.QWidget):
    """
    Widget for showing information to covariance matrix created from a
    raw file.
    """

    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_covarianceRawWidget()
        self.ui.setupUi(self)
        self.parent = parent
        
        
    