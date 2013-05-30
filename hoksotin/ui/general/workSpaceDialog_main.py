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

"""
Created on Apr 23, 2013

@author: Jaakko Leppakangas
Contains the WorkSpaceDialog-class containing the logic for the
WorkSpaceDialog-window.
"""
from PyQt4 import QtCore,QtGui

from workSpaceDialog_Ui import Ui_Dialog
import messageBox

import sys
import ConfigParser
import os

class WorkSpaceDialog(QtGui.QDialog):
    """
    Class containing the logic for WorkSpaceDialog. Used for setting up the
    root folder for saving and loading files.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.path = ''
        
    def on_browseButton_clicked(self, checked=None):
        """
        Opens a filebrowser to select the workspace.
        """
        # Standard workaround for file dialog opening twice
        if checked is None: return 
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