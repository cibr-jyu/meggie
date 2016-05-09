'''
Created on 4.5.2016

@author: jaolpeso
'''
from PyQt4 import QtCore, QtGui
from meggie.ui.widgets.covarianceWidgetEpochsUi import Ui_Form


class CovarianceWidgetEpochs(QtGui.QWidget):
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
