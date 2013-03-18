  # -*- coding: utf-8 -*-
 
 
import os,sys
from file import File
from infoDialog_main import InfoDialog
import messageBox
from Project import Project
from UIehd1_main import MainWindow
#from Project import Project

from PyQt4 import QtCore,QtGui
 
# Import the pyuic4-compiled main UI module 
from CreateProjectDialog_Ui import Ui_CreateProjectDialog
 
# Create a dialog main window
class CreateProjectDialog(QtGui.QDialog):
    fname = ''
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.fname = ''
        """
        Reference to main dialog window
        """       
        self.ui = Ui_CreateProjectDialog() # Refers to class in file CreateProjecDialog
        self.ui.setupUi(self)
        
    def accept(self):
        try:
            if self.ui.lineEditProjectName.text() == '':
                raise Exception('Fill all required fields!')
            self.project = Project()
            self.project.set_raw_data(self.raw)
            self.project.set_author(self.ui.lineEditAuthor.text())
            #self.project.setFilePath(self.ui.lineEditProjectName.text())   TODO: Muuta project-luokkaa siten, että luo uuden kansion projektille.
            self.project.set_description(self.ui.textEditDescription.toPlainText())
            print self.project.get_description()
            print self.project.get_date()
            self.UIehd = MainWindow(self.project)
            self.UIehd.show()
            self.close()
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err[0]))
            self.messageBox.show()
    
    def on_browseButton_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/usr/local/bin/ParkkosenPurettu/meg/jn')
        print self.fname
        try:
            f = File()
            self.raw = f.open_raw(self.fname)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err[0]))
            self.messageBox.show()
                
        #QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CreateProjectDialog.openFileChooserDialog)
        self.ui.FilePathLineEdit.setText(self.fname)
        
    def on_showFileInfoButton_clicked(self):
        try:
            self.infoDialog = InfoDialog(self.raw)
            self.infoDialog.show()
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err[0]))
            self.messageBox.show()

"""    
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
""" 