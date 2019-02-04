# coding: utf-8

"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal

from meggie.ui.widgets.epochWidgetUi import Ui_Form

class EpochWidget(QtWidgets.QWidget):
    """
    Creates a widget that shows a list of epoch collections.
    """
    
    on_selection_changed = pyqtSignal()

    def __init__(self, parent, epoch_getter=None, parameter_setter=None):
        """
        Constructor 
        """
        QtWidgets.QWidget.__init__(self, parent)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.epoch_getter = epoch_getter
        self.parameter_setter = parameter_setter
        
        self.ui.listWidgetEpochs.currentItemChanged.connect(
            self.selection_changed)


    def setSelectionMode(self, mode):
        """
        """
        self.ui.listWidgetEpochs.setSelectionMode(mode)
        
        
    def clearItems(self):
        """Remove all the items from the widget's list.
        """
        while self.ui.listWidgetEpochs.count() > 0:
            self.ui.listWidgetEpochs.takeItem(0)

    def currentItem(self):
        """return The currently selected item from the widget's list."""
        if self.ui.listWidgetEpochs.count() != 0: 
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

    def add_item(self, item):
        """
        """
        self.ui.listWidgetEpochs.addItem(item)
        

    def selection_changed(self):
        item = self.currentItem()
        if item is None:
            return

        epochs = self.epoch_getter(item.text())

        if not epochs:
            return

        events = epochs.raw.event_id
        self.ui.listWidgetEvents.clear()
        for event_name, event_id in events.items():
            events_str = (event_name + ' [' + str(len(epochs.raw[event_name])) + 
                          ' events found]')

            item = QtWidgets.QListWidgetItem(events_str)
            self.ui.listWidgetEvents.addItem(item)

        # call show parameter handler
        if self.parameter_setter and epochs.params is not None:
            self.parameter_setter(epochs)

