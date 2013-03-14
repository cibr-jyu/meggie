  # -*- coding: utf-8 -*-
 
 
import os,sys
#from Project import Project
 
from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
from CreateProjectDialog import Ui_CreateProjectDialog
 
# Create a dialog main window
class CreateProjectDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)

        """
        Reference to main dialog window
        """       
        self.ui = Ui_CreateProjectDialog() # Refers to class in file CreateProjecDialog
        self.ui.setupUi(self)
 
    
    def on_browseButton_clicked(self, checked=None):
        if checked is None: return # Standard for file dialog opening twice
        fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/home')
        print fname
          
          
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 