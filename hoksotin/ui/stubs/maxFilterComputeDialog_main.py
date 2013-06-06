# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

'''
Created on Apr 22, 2013

@author: Jaakko Leppakangas
Contains the MaxFilterComputeDialog-class used to inform the user
that MaxFilter is running. Not currently implemented.
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
        