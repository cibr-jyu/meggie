# coding: latin1
"""
Created on May 2, 2013

@author: Jaakko Leppakangas
"""
from PyQt4 import QtCore,QtGui

from epochWidget_Ui import Ui_Form

class EpochWidget(QtGui.QWidget):
    """
    Creates a widget that shows a list of epoch collections.
    """


    def __init__(self, parent):
        """
        Constructor creates a widget.
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)