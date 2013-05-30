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

# coding: latin1
"""
@author: Kari Aliranta, Jaakko Leppakangas
Contains the AppForm-class used for simple messageboxes.
"""

from PyQt4 import QtCore,QtGui


class AppForm(QtGui.QDialog):
    """
    Class for creating simple messageboxes displaying error messages.
    """
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.create_main_frame()       

    def create_main_frame(self):        
        page = QtGui.QWidget()
        
        self.setWindowTitle('Error') 
        self.buttonOk = QtGui.QPushButton('Ok', page)
        self.labelException = QtGui.QLabel()
        self.buttonOk.move(150,0)
        vbox1 = QtGui.QVBoxLayout(self)
        vbox1.addWidget(self.labelException)
        vbox1.addWidget(self.buttonOk)

        self.connect(self.buttonOk, QtCore.SIGNAL("clicked()"), self.accept)

    def accept(self):
        self.close()
