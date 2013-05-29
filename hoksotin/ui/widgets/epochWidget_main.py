"""
Created on May 2, 2013

@author: Jaakko Leppakangas
"""
from PyQt4 import QtCore,QtGui

from epochWidget_Ui import Ui_Form

class EpochWidget(QtGui.QWidget):
    """
    Creates a widget that shows a list of epochs.
    """


    def __init__(self, parent):
        """
        Constructor creates a widget.
        """
        QtGui.QWidget.__init__(self, parent)
        #QtGui.QDialog.__init__(self)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)