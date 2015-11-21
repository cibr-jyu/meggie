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
@author: Kari Aliranta, Jaakko Leppakangas

Contains the CreateExperimentDialog-class that holds the logic for
CreateExperimentDialog-window.
"""

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal

from code_meggie.general.experiment import Experiment
import messageBoxes
from createExperimentDialogUi import Ui_CreateExperimentDialog

 
class CreateExperimentDialog(QtGui.QDialog):
    """
    Class containing the logic for CreateExperimentDialog. It is used for 
    setting up a new experiment for analyzing MEG data.
    """
    fname = ''
    experimentCreated = pyqtSignal(Experiment)
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.fname = ''
        
        # Reference to main dialog window
        self.parent = parent
        
        # Refers to class in file CreateProjecDialog
        self.ui = Ui_CreateExperimentDialog() 
        self.ui.setupUi(self)
                
                
    def accept(self):
        """Send parameters to experimentHandler for the creation of a
        new experiment."""
        
        if self.ui.lineEditExperimentName.text() == '':
            message = 'Give experiment a name.'
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return  
        
        expDict = {'name': self.ui.lineEditExperimentName.text(),
                   'author': self.ui.lineEditAuthor.text(),
                   'description': self.ui.textEditDescription.toPlainText()
                  }
        
        experiment = self.parent.experimentHandler.initialize_new_experiment(expDict)
        
        self.experimentCreated.emit(experiment)
        self.close()
        