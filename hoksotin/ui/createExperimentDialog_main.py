  # -*- coding: utf-8 -*-


from file import File
from infoDialog_main import InfoDialog
import messageBox

from experiment import Experiment
from workspace import Workspace

#from mainWindow_mainTesti import MainWindow
from infoDialog_Ui import Ui_infoDialog
from createExperimentDialog_Ui import Ui_CreateExperimentDialog
from maxFilterComputeDialog_main import MaxFilterComputeDialog

from PyQt4 import QtCore,QtGui
# Import the pyuic4-compiled main UI module 

import os,sys
import StringIO
import pickle
import time
from threading import  Thread
import ConfigParser

# Create a dialog main window
class CreateExperimentDialog(QtGui.QDialog):
    fname = ''
    
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.fname = ''
        self.parent = parent
        """
        Reference to main dialog window
        """
        
        # Refers to class in file CreateProjecDialog
        self.ui = Ui_CreateExperimentDialog() 
        self.ui.setupUi(self)
        self.ui.labelCreatingExperiment.setVisible(False)
        self.ui.progressBarCreatingExperiment.setVisible(False)
        self.ui.showFileInfoButton.setEnabled(False)
        #self.computeDialog = MaxFilterComputeDialog(self)
        """
        self.computeDialog.open()
        self.computeDialog.raise_()
        self.computeDialog.activateWindow()        
        """
        
        #self.computeDialog.setVisible(False)
        #sys.stdout = OutLog(self.computeDialog.ui.textEditDetails, sys.stdout)
            
                
    def accept(self):
        self.ui.labelCreatingExperiment.setVisible(True)
        self.ui.progressBarCreatingExperiment.setVisible(True)
        #self.computeDialog.show()
        #self.computeDialog.raise_()
        QtGui.QApplication.processEvents(flags=QtCore.QEventLoop.AllEvents)
        
        self.t2 = Thread(target=self._initialize_experiment())
        t = Thread(target = self.process_events())
        
        t.start()
        self.t2.start()
        
    def on_browseButton_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                           '/home/'))
        if self.fname != '':
            try:
                f = File()
                self.raw = f.open_raw(self.fname)
                self.ui.showFileInfoButton.setEnabled(True)
            except Exception, err:
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText(str(err))
                self.messageBox.show()
                
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
        QtGui.QApplication.processEvents() 
        
    def _initialize_experiment(self):
        self.k = True
        try:
            if self.ui.lineEditProjectName.text() == '':
                raise Exception('Give experiment a name!')
            
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            #self.computeDialog.close()
            return          
        QtGui.QApplication.processEvents()
        #self.computeDialog.setValue(10)    
        try:
            self.workspace = Workspace()
            self.experiment = Experiment()
            #self.workspace.working_directory = '/usr/local/bin/'  #'/tmp/' 
            self.experiment.author = self.ui.lineEditAuthor.text()
            self.experiment.experiment_name = self.ui.\
            lineEditProjectName.text()
            self.experiment.description = self.ui.textEditDescription.toPlainText()
            print self.experiment.file_path

        except AttributeError:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText("Cannot assign attribute to project")
            self.messageBox.show()
            #self.computeDialog.close()
            return         
        try:
            # TODO: user should set this workspace from the mainWindow UI    
            self.experiment.save_experiment(self.workspace.working_directory)
            self.experiment.raw_data = self.raw
            self.experiment.create_event_set()
            self.experiment.save_raw(os.path.basename(str(self.ui.FilePathLineEdit.text())))
            self.experiment.save_experiment_settings()
            print self.experiment.raw_data.info.get('filename')
      
        except IOError, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            #self.computeDialog.close()
            return

        QtGui.QApplication.processEvents()
        self.parent.experiment = self.experiment
        self.parent.raw = self.experiment.raw_data
        InfoDialog(self.parent.experiment.raw_data, self.parent.ui, False)
        self.parent.ui.labelExperimentName.setText(self.experiment.experiment_name)
        self.parent.ui.listWidget.clear()
        events = self.experiment.event_set
        for key, value in events.iteritems():
            item = QtGui.QListWidgetItem()
            item.setText('Trigger ' + str(key) + ', ' + str(value) +
                        ' events')
            self.parent.ui.listWidget.addItem(item)
        self.k = False
        self.close()
        self.parent._initialize_ui() 

        #self.computeDialog.close()
    
    def process_events(self):
        self.k=True
        while self.k:
            QtGui.QApplication.processEvents()
        #self.computeDialog.setVisible(False)
        
class OutLog:
    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QtGui.QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.color:
            self.edit.setTextColor(tc)

        if self.out:
            self.out.write(m)
    
"""    
def main(): 
    app = QtGui.QApplication(sys.argv)
    window=Main()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
""" 