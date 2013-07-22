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
Created on May 2, 2013

@author: Jaakko Leppakangas, Atte Rautio
Contains the EpochWidget-class used for listing epoch collections.
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from epochWidgetUi import Ui_Form

class EpochWidget(QtGui.QWidget):
    """
    Creates a widget that shows a list of epoch collections.
    """

    on_selection_changed = pyqtSignal()

    def __init__(self, parent):
        """
        Constructor 
        """
        QtGui.QWidget.__init__(self, parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.parent = parent
        
        # Connect listWidgetEpochs.currentItemChanged method to change
        # parameters on epochParamsWidget
        self.ui.listWidgetEpochs.currentItemChanged.connect(self.set_as_selected)
        
    def addItem(self, item, suffix = 1):
        """
        Add an item to the widget's list.
        
        If item is a list, adds all the items in it.
        
        Keyword arguments:
        item   = a single item or a list of items to be added.
        suffix = a suffix given to the item to make the text unique.
        """
        try:
            for i in item:
                #Check if there already is an item with the same text in the
                #list.
                if not self.ui.listWidgetEpochs.findItems(i.text(),\
                                                          QtCore.Qt.\
                                                          MatchFixedString):
                    if suffix is 1:
                        self.ui.listWidgetEpochs.addItem(i)
                    else:
                        qstr_suffix = QtCore.QString('')
                        qstr_suffix.append(QString('%1').arg(suffix))
                        i.setText(i.text() + qstr_suffix)
                        self.ui.listWidgetEpochs.addItem(i)
                
                else:
                    suffix += 1
                    self.addItem(i, suffix)
                    #reset the suffix back to zero.
                    suffix = 1
        
        except TypeError:
            if not self.ui.listWidgetEpochs.findItems(item.text(), QtCore.Qt.\
                                                      MatchFixedString):
                if suffix is 1:
                    self.ui.listWidgetEpochs.addItem(item)
                else:
                    qstr_suffix = QtCore.QString('')
                    qstr_suffix.append(QString('%1').arg(suffix))
                    item.setText(item.text() + qstr_suffix)
                    self.ui.listWidgetEpochs.addItem(item)
                
            else:
                suffix += 1
                self.addItem(item, suffix)
            
    def setCurrentItem(self, item):
        """
        sets the current item of the widget's list.
        
        Keyword arguments:
        item = item to be set as the current item.
        """
        self.ui.listWidgetEpochs.setCurrentItem(item)
        self.parent.epochParamsList.set_parameters(item)

    def set_as_selected(self):
        item = self.ui.listWidgetEpochs.currentItem()
        self.parent.epochParamsList.set_parameters(item)
        
        
        