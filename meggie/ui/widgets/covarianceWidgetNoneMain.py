"""
Created on 27.1.2015

@author: Kari Aliranta
"""

from PyQt4 import QtCore, QtGui

from meggie.ui.widgets.covarianceWidgetNoneUi import Ui_Form


class CovarianceWidgetNone(QtGui.QWidget):
    """
    Widget for showing information to covariance matrix created from a
    raw file.
    """

    def __init__(self, parent=None):
        """
        Constructor
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent
