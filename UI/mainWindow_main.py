  # -*- coding: utf-8 -*-
 
 
import os,sys
#from Project import Project
 
from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
from mainWindow_Ui import Ui_MainWindow
from CreateProjectDialog_main import CreateProjectDialog

#import measurementInfo
 
  # Create a class main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        """
        Reference to main application window
        """
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
 
        #self.createProjectDialog
        #self.createProjectDialog.setupUi(self)
        
        #self.infoDialog
        #self.infodialog.setupUi(self)
 
        """Buttons automatically have clicked signal, no need to define
        it in Qt designer
        """
            
    # Automatically connects to clicked-signal of the button    
    def on_ButtonNewProject_clicked(self):
        """
        Creates a new CreateProjectDialog and shows it
        """       
        self.dialog = CreateProjectDialog()
        self.dialog.show()
        
        
#        
#        self.dialog = QtGui.QDialog() # New blank QDialog
#        createProjectDialog = Ui_CreateProjectDialog() # Refers to class in file CreateProjecDialog
#        createProjectDialog.setupUi(self.dialog) # populates the blank QDialog with actual content
#        self.dialog.show()
        
        #self.
        
        #self.dialog.CreateProjectDialog.
        
        #self.dialog.pushButton.clicked.connect()
        
        
        
        
        #dialog = self.createProjectDialog()
        #dialog.show()
        
        
        #projectDialog.setupUi(self)
        #projectDialog = CreateProjectDialog.CreateProjectDialog()
        
        #createProjectDialog.setupUi(self)   
        
        #self.createProjectDialog.setupUi(self)
        
        
        #self.createProjectDialog.showInfoButton.clicked.connect(self.showInfo)
        #self.createProjectDialog.show() 
       
        
    #def showInfo(self):
        #self.  = measurementInfo.MeasurementInfo

def main(): 
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()