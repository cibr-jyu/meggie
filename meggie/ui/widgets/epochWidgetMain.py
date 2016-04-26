# coding: utf-8

"""
Created on May 2, 2013

@author: Jaakko Leppakangas, Atte Rautio
Contains the EpochWidget-class used for listing epoch collections.
"""
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal

from meggie.code_meggie.general.caller import Caller

from meggie.ui.widgets.epochWidgetUi import Ui_Form

class EpochWidget(QtGui.QWidget):
    """
    Creates a widget that shows a list of epoch collections.
    """
    
    #Custom signals:
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
        self.ui.listWidgetEpochs.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.ui.listWidgetEpochs.currentItemChanged.connect(self.selection_changed)
        

#    def addItem(self, collection_name):
#        """
#        Add an item or items to the widget's list
#        """
#        self.ui.listWidgetEpochs.addItem(collection_name)
        
    def clearItems(self):
        """Remove all the items from the widget's list.
        """
        while self.ui.listWidgetEpochs.count() > 0:
            self.ui.listWidgetEpochs.takeItem(0)

    def currentItem(self):
        """return The currently selected item from the widget's list."""
        if self.ui.listWidgetEpochs.count() == 0: return None
        else:
            return self.ui.listWidgetEpochs.currentItem() 

    def isEmpty(self):
        """Return True if the widget is empty, otherwise return False."""
        if self.ui.listWidgetEpochs.count() > 0:
            return False
        else:
            return True

    def remove_item(self, item):
        """Remove an item from the list.

        Keyword arguments:

        item -- The item to be removed
        """
        row = self.ui.listWidgetEpochs.row(item)
        self.ui.listWidgetEpochs.takeItem(row)

    def setCurrentItem(self, item):
        """
        sets the current item of the widget's list.

        Keyword arguments:
        item = item to be set as the current item.
        """
        self.ui.listWidgetEpochs.setCurrentItem(item)

    def selection_changed(self):
        item = self.ui.listWidgetEpochs.currentItem()
        if item is None: return
        caller = Caller.Instance()
        epochs = caller.experiment.active_subject.epochs
        key = str(item.text())
        if epochs.has_key(key):
            epoch = caller.experiment.active_subject.epochs[key]
            #if not epoch._raw is None:
            if epoch.params is not None:
                self.parent.show_epoch_collection_parameters(epoch)
        #self.parent.show_evoked_info()
