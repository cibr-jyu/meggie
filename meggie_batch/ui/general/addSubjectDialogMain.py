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
Created on Oct 31, 2013

@author: jaolpeso
'''
from PyQt4 import QtCore,QtGui

from addSubjectDialogUi import Ui_AddSubject
from fileManager import FileManager
from subject import Subject
from infoDialogMain import InfoDialog
import messageBox

import os, sys

from infoDialogUi import Ui_infoDialog

class AddSubjectDialog(QtGui.QDialog):
    """
    Class for creating subjects from raw measurement data files.
    
    Properties:
    parent    -- mainWindowMain is the parent class
    """
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_AddSubject()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = self.parent.experiment
    
    def accept(self):
        """Add the new subject.
        """
        #self.parent.listWidgetSubjects.addItem?
        #self.parent._initialize_ui
        #self._initialize_experiment()
        raw_path = str(self.ui.lineEditFileName.text())
        subject_name = os.path.basename(raw_path)
        self.parent.experiment.activate_subject(raw_path, \
                                                subject_name, \
                                                self.experiment)
        self.parent.experiment.update_experiment_settings()
        self.parent.enable_tabs()
        self.parent._initialize_ui()
        self.close()
        
    def on_pushButtonBrowse_clicked(self, checked=None):
        """
        Open file browser for raw data files.
        """
        if checked is None: return
        
        self.fname = str(QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                           '/home/'))
        if self.fname != '':        
            self.ui.lineEditFileName.setText(self.fname)
            
            
    def on_pushButtonShowFileInfo_clicked(self, checked = None):
        """
        Opens the infoDialog for the raw file selected.
        """
        try:
            f = FileManager()
            self.raw = f.open_raw(self.fname, pre_load = False)
            self.ui.pushButtonShowFileInfo.setEnabled(True)
            
        except IOError as e:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(e))
            self.messageBox.show()
            return
        
        except OSError as e:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(e))
            self.messageBox.show()
            return
        
        except ValueError as e:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(e))
            self.messageBox.show()
            return
            
        info = Ui_infoDialog()
        self.infoDialog = InfoDialog(self.raw, info, True)
        self.infoDialog.show()

        QtGui.QApplication.processEvents() 