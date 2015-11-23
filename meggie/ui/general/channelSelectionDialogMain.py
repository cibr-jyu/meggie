'''
Created on 5.1.2015

@author: Jaakko Leppakangas
'''

from PyQt4 import QtGui
from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QListWidgetItem

from code_meggie.general.caller import Caller
from ui.general.channelSelectionDialogUi import Ui_ChannelSelectionDialog

class ChannelSelectionDialog(QtGui.QDialog):
    channelsChanged = pyqtSignal(list)
    
    def __init__(self, selChannels=[], caption = ""):
        """
        A dialog for selecting bad channels by hand.
        parameters:
        selChannels - Used for checking channels. All the channels in this list
                      are selected on startup.
        """
        caller = Caller.Instance()
        QtGui.QDialog.__init__(self)

        self.ui = Ui_ChannelSelectionDialog()
        self.ui.setupUi(self)
        
        
        self.ui.listWidgetChannels.clear()
        channels = caller.experiment.active_subject.working_file.info['ch_names']
        for channel in channels:
            item = QListWidgetItem(channel)
            self.ui.listWidgetChannels.addItem(item)
            if channel in selChannels:
                self.ui.listWidgetChannels.setItemSelected(item, True)
        if caption == "":
            pass
        else:
            self.ui.label.setText(caption)

    def accept(self, *args, **kwargs):
        """
        Called when ok is clicked.
        """
        items = self.ui.listWidgetChannels.selectedItems()
        channels = []
        for item in items:
            channels.append(str(item.text()))
        
        self.channelsChanged.emit(channels)
        return QtGui.QDialog.accept(self, *args, **kwargs)
        
        
        
