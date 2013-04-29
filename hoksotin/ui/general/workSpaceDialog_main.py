'''
Created on Apr 23, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui

from workSpaceDialog_Ui import Ui_Dialog
import messageBox

import sys
import ConfigParser
import os

class WorkSpaceDialog(QtGui.QDialog):


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.path = ''
        
    def on_browseButton_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.path = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select a working space"))
        self.ui.FilePathLineEdit.setText(self.path)
        
    def accept(self):
        if os.path.isdir(self.path):
            config = ConfigParser.RawConfigParser()
            config.add_section('Workspace')
            config.set('Workspace', 'workspace', self.path)
            with open('settings.cfg', 'wb') as configfile:
                config.write(configfile)
            self.close()
            
        else:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText('No file path found')
            self.messageBox.show()