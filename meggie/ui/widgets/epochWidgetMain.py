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
    
    #Custom signals:
    on_selection_changed = pyqtSignal()
    item_added = pyqtSignal(QtGui.QListWidgetItem)

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
        Add an item or items to the widget's list.
        
        If item is a list, add all the items in it.
        Emit an item_added signal
        
        Keyword arguments:
        item   = a single QListWidgetItem or a list of QListWidgetItems
                 to be added.
        suffix = a suffix given to the item to make the item's text unique.
        
        """
        try:
            for i in item:
                #A recursive call for each individual item
                self.addItem(i)
        
        except TypeError:
            #If suffix is 1 there's no need to add it to the item's text. I.e.
            #Name "Epochs" doesn't have to become "Epochs1"
            if suffix is 1:
                if not self.ui.listWidgetEpochs.findItems(item.text(),\
                                                          QtCore.Qt.\
                                                          MatchFixedString):
                    self.ui.listWidgetEpochs.addItem(item)
                    self.item_added.emit(item)
                else:
                    suffix += 1
                    self.addItem(item, suffix)
                
            else:
                qstr_suffix = QtCore.QString('')
                qstr_suffix.append(QtCore.QString('%1').arg(suffix))

                if not self.ui.listWidgetEpochs.findItems(item.text() +\
                                                          qstr_suffix,\
                                                          QtCore.Qt.\
                                                          MatchFixedString):
                    item.setText(item.text() + qstr_suffix)
                    self.ui.listWidgetEpochs.addItem(item)
                    self.item_added.emit(item)
                    
                else:
                    suffix += 1
                    self.addItem(item, suffix)
                    
    def clearItems(self):
        """Remove all the items from the widget's list.
        """
        while self.ui.listWidgetEpochs.count() > 0:
            self.ui.listWidgetEpochs.takeItem(0)
            
    def setCurrentItem(self, item):
        """
        sets the current item of the widget's list.
        
        Keyword arguments:
        item = item to be set as the current item.
        """
        self.ui.listWidgetEpochs.setCurrentItem(item)
        
    def set_as_selected(self):
        item = self.ui.listWidgetEpochs.currentItem()
        self.parent.epochParamsList.show_parameters(item)
        """
        parameters = self.parent.epochParamsList.set_parameters(item)
        item.setData(33, parameters)
        self.parent.epochParamsList.show_parameters(parameters)
        #TODO: maybe give item obejct instead of parameters string to method: 
        #self.parent.epochParamsList.show_parameters(item)
        """
