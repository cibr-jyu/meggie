  # -*- coding: utf-8 -*-


from file import File
from infoDialog_main import InfoDialog
import messageBox

from experiment import Experiment
from workspace import Workspace

from UIehd1_main import MainWindow
from infoDialog_Ui import Ui_infoDialog
from CreateProjectDialog_Ui import Ui_CreateProjectDialog

from PyQt4 import QtCore,QtGui
# Import the pyuic4-compiled main UI module 

import os,sys
import pickle

# Create a dialog main window
class CreateProjectDialog(QtGui.QDialog):
    fname = ''
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.fname = ''
        self.parent = parent
        """
        Reference to main dialog window
        """
        
        # Refers to class in file CreateProjecDialog
        self.ui = Ui_CreateProjectDialog() 
        self.ui.setupUi(self)
        
    def accept(self):
        try:
            if self.ui.lineEditProjectName.text() == '':
                raise Exception('Give a experiment name!')
            
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()            
            
        try: 
            self.workspace = Workspace()
            self.experiment = Experiment()
            self.experiment.raw_data = self.raw
            self.experiment.author = self.ui.lineEditAuthor.text()
            self.experiment.experiment_name = self.ui.\
            lineEditProjectName.text()
            self.experiment.description = self.ui.textEditDescription.toPlainText()

        except AttributeError:
            print "Cannot assign attribute to project"           
            
        
        try:
            # TODO: user should set this workspace from the mainWindow UI    
            self.workspace.working_directory = '/tmp/' #'/usr/local/bin/' 
            self.experiment.save_experiment(self.workspace.working_directory)
                        
            self.experiment.save_raw(os.path.basename(str(self.ui.FilePathLineEdit.text())))
            self.experiment.save_experiment_settings()
      
        except IOError, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            
        self.UIehd = MainWindow(self.experiment)
        self.UIehd.show()
        self.close()
        self.parent.close()
        
    
    def on_browseButton_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                           '/home/'))
        if self.fname != '':
            try:
                f = File()
                self.raw = f.open_raw(self.fname)
            except Exception, err:
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText(str(err))
                self.messageBox.show()
                
        #QtCore.QObject.connect(self.browseButton, QtCore.SIGNAL(_fromUtf8("clicked()")), CreateProjectDialog.openFileChooserDialog)
        self.ui.FilePathLineEdit.setText(self.fname)
        
    def on_showFileInfoButton_clicked(self):
        try:
            info = Ui_infoDialog()
            self.infoDialog = InfoDialog(self.raw, info, True)
            self.infoDialog.show()
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
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