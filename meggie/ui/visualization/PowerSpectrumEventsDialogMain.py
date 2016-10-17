'''
Created on 17.10.2016

@author: jaolpeso
'''
from PyQt4 import QtGui

from meggie.ui.visualization.powerSpectrumEventsUi import Ui_Advanced 

class PowerSpectrumEvents(QtGui.QDialog):
    
    def __init__(self, parent):
        """
        Init method for the dialog.
        Constructs a set of time series from the given parameters.
        Parameters:
        parent     - The parent window for this dialog.
        """
        QtGui.QDialog.__init__(self)
        self.intervals = []
        self.ui = Ui_Advanced()
        self.ui.setupUi(self)
        self.parent = parent