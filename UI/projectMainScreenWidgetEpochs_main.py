 # -*- coding: utf-8 -*-
 
 
import os,sys
#from Project import Project
 
from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
from projectMainScreenWidgetEpochs_Ui import Ui_Form

 
  # Create a class main window
class projectMainScreenWidgetEpochs(QtGui.QWidget):
    def __init__(self,parent,task=None):
        QtGui.QWidget.__init__(self, parent)

      
        self.ui=Ui_Form()
        self.ui.setupUi(self)
