"""
Created on Sep 22, 2013

@author: atmiraut
"""
import sys

from PyQt4 import QtGui, QtCore

class ListWidget(QtGui.QListWidget):
    """
    classdocs
    """
    def __init__(self):
        QtGui.QListWidget.__init__(self)
        
    def addItem(self, item, suffix = 1):
        """
        Add an item or items to the widget's list and sort the list.
        
        If item is a list, add all the items in it. Item text is converted to
        start with an uppercase letter and the list is also sorted in ascending
        order.
        
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
                if not self.findItems(item.text(), QtCore.Qt.MatchFixedString):
                    QtGui.QListWidget.addItem(self, item)
                    self.sortItems()
                    
                else:
                    suffix += 1
                    self.addItem(item, suffix)
                
            else:
                qstr_suffix = QtCore.QString('')
                qstr_suffix.append(QtCore.QString('(%1)').arg(suffix))

                if not self.findItems(item.text() + qstr_suffix,\
                                      QtCore.Qt.MatchFixedString):
                    
                    item.setText(item.text() + qstr_suffix)
                    QtGui.QListWidget.addItem(self, item)
                    self.sortItems()
                    
                else:
                    suffix += 1
                    self.addItem(item, suffix)   