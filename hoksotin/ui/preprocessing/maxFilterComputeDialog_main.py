'''
Created on Apr 22, 2013

@author: jaeilepp
'''
import os

from PyQt4 import QtCore,QtGui
from maxFilterComputeDialog_Ui import Ui_Dialog
import messageBox
from infoDialog_main import InfoDialog
from infoDialog_Ui import Ui_infoDialog

class MaxFilterComputeDialog(QtGui.QProgressDialog):
    """
    Class containing the logic for MaxFilterComputeDialog.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.initialize()
        QtGui.QApplication.processEvents()
    def initialize(self):
        """
        try:
           if self.parent.ui.lineEditProjectName.text() == '':
               raise Exception('Give experiment a name!')
        
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            self.close()
            return
        try:
           self.parent.workspace = Workspace()
           self.parent.experiment = Experiment()
           self.parent.workspace.working_directory = '/usr/local/bin/'  #'/tmp/' 
           self.parent.experiment.author = self.parent.ui.lineEditAuthor.text()
           self.parent.experiment.experiment_name = self.parent.ui.\
           lineEditProjectName.text()
           self.parent.experiment.description = self.parent.ui.textEditDescription.toPlainText()

        except AttributeError:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText("Cannot assign attribute to project")
            self.messageBox.show()
            self.close()
            return         
                  
        try:
            # TODO: user should set this workspace from the mainWindow UI    
            self.parent.experiment.save_experiment(self.parent.workspace.working_directory)
            self.parent.experiment.raw_data = self.parent.raw
            self.parent.experiment.create_event_set()
            self.parent.experiment.save_raw(os.path.basename(str(self.parent.ui.FilePathLineEdit.text())))
            self.parent.experiment.save_experiment_settings()
      
        except IOError, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            self.close()
            return
        
        self.parent.parent.experiment = self.parent.experiment
        self.parent.parent.raw = self.parent.experiment.raw_data
        InfoDialog(self.parent.parent.experiment.raw_data, self.parent.parent.ui, False)
        self.parent.parent.ui.labelExperimentName.setText(self.parent.experiment.experiment_name)
        self.parent.parent.ui.listWidget.clear()
        events = self.parent.experiment.event_set
        for key, value in events.iteritems():
            item = QtGui.QListWidgetItem()
            item.setText('Trigger ' + str(key) + ', ' + str(value) +
                        ' events')
            self.parent.parent.ui.listWidget.addItem(item)
        self.close()
        """