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
Created on Apr 29, 2013

@author: Janne Pesonen
Contains the PreferencesDialog-class used in setting the preferences for
the application.
"""

import os
import ConfigParser
from PyQt4 import QtCore, QtGui

import prefecences

from preferencesDialogUi import Ui_DialogPreferences
import messageBoxes


class PreferencesDialog(QtGui.QDialog):
    """
    Dialog to set the preferences for the application (workspace directory
    and MNE root directory).
    """

    def __init__(self, parent):
        """
        Constructor
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_DialogPreferences() 
        self.ui.setupUi(self)
        
        self.parent = parent
        
        self._workFilepath = ''
        self._MNERootPath= ''
    
        # Prefill previous values to UI and attributes from config file.
        if os.path.isfile('settings.cfg'):
            configp = ConfigParser.RawConfigParser()
            configp.read('settings.cfg')
            
            if configp.has_option('Workspace', 'workspacedir'):
                workFilePath = configp.get('Workspace', 'workspacedir')
            else: 
                workFilePath = ''
            
            if configp.has_option('EnvVariables','MNERootDir'):
                MNERootPath = configp.get('EnvVariables','MNERootDir')
            else:
                MNERootPath = ''
            
            if configp.has_option('MiscOptions, autoReloadPreviousExperiment'):
                if configp.get('MiscOptions',  
                    'autoReloadPreviousExperiment') is 'true':
                    self.ui.checkBoxAutomaticOpenPreviousExperiment.\
                    setChecked(True)
                
            self._workFilepath = workFilePath
            self._MNERootPath = MNERootPath
            self.ui.LineEditFilePath.setText(self._workFilepath)
            self.ui.lineEditMNERoot.setText(self._MNERootPath)
     
     
    
    def on_ButtonBrowseWorkingDir_clicked(self, checked=None):
        """
        Opens a filebrowser to select the workspace.
        """
        # Standard workaround for file dialog opening twice
        if checked is None: return 
        
        self._workFilepath = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select a workspace directory"))
        self.ui.LineEditFilePath.setText(self._workFilepath)
    
    
    def on_pushButton_browseMNERoot_click(self, checked=None):
        if checked is None: return  
        
        self.MNERootPath = str(QtGui.QFileDialog.getExistingDirectory(
               self, "Select the directory for MNE root"))
        self.ui.LineEditFilePath.setText(self._MNERootPath)
        
        
    def accept(self):
        
        if os.path.isdir(self._workFilepath):
            workFilePath = self._workFilepath
        else:
            message = 'No file path found for working file'
            messageBox = messageBoxes.shortMessageBox(message)
            messageBox.show()
        
        if self.ui.checkBoxAutomaticOpenPreviousExperiment.isChecked() is True:
            autoLoadLastOpenExp = True
        else: autoLoadLastOpenExp = False
        
        # MNE Root path can be empty or wrong here, we can annoy user about
        # it if he really tries to use something MNE-related.
        MNERootPath = self._MNERootPath
        
        
        prefecences.writePreferencesToDisk(workFilePath,
                                           MNERootPath, 
                                           autoLoadLastOpenExp)
        
        