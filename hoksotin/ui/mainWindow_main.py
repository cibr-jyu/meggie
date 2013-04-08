  # -*- coding: utf-8 -*-
 
 
import os,sys
import pickle
#from Project import Project
 
from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
import messageBox
from mainWindow_Ui import Ui_MainWindow
from CreateProjectDialog_main import CreateProjectDialog
from UIehd1_main import MainWindow
from IPython.lib.pretty import pprint

#import measurementInfo
 
  # Create a class main window
class Main(QtGui.QMainWindow):
    def __init__(self):
        
        """
        Make imports work for every package the application directory structure,
        as long as the depth of this file in the structure stays the same
        """
        sys.path.append("../")
        sys.path.append("../../")
        sys.path.append("../../code/")
        sys.path.append("../../code/externalModules/")
        sys.path.append("../../code/tests/")
        
        QtGui.QMainWindow.__init__(self)

        """
        Reference to main application window
        """
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        #self.ui.widget.hide()
            
            
            
    # Automatically connects to clicked-signal of the button    
    def on_ButtonNewProject_clicked(self):
        """
        Creates a new CreateProjectDialog and shows it
        """       
        self.dialog = CreateProjectDialog(self)
        self.dialog.show()
        
    def on_ButtonOpenProject_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        path = str(QtGui.QFileDialog.getExistingDirectory(self, "Select project directory"))
        #path = os.path.dirname(os.path.abspath(str(fname)))
        fname = path + '/' + path.split('/')[-1] + '.pro'
        if os.path.exists(path) and os.path.isfile(fname):
            output = open(fname, 'rb')
            print output
            project = pickle.load(output)
            self.UIehd = MainWindow(project)
            self.UIehd.show()
            self.close()
        
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('Project files not found.')
            self.messageBox.show()
            

def main(): 
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()