 # -*- coding: utf-8 -*-
 
 
import os,sys
#from Project import Project
 
from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
from projectMainScreenWidget import Ui_projectMainScreenWidget

 
  # Create a class main window
class Main(QtGui.QtGui.QWidget):
    def __init__(self):
        QtGui.QtGui.QWidget.__init__(self)

        """
        Reference to main application window
        """
        self.ui=Ui_Form()
        self.ui.setupUi(self)
