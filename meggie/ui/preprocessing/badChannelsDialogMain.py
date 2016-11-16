'''
Created on 16.11.2016

@author: jaolpeso
'''
from PyQt4 import QtGui, QtCore

from meggie.ui.preprocessing.badChannelsDialogUi import Ui_Dialog
from PyQt4.Qt import QMimeData

class BadChannelsDialog(QtGui.QDialog):

    def __init__(self, parent):    
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        raw = parent.caller.experiment.active_subject.get_working_file()
        channels = raw.ch_names
        for channel in channels:
            self.ui.listWidgetBads.addItem(channel)
            
    def on_pushButtonSelectAll_clicked(self, checked=None):
        if checked is None:
            return
        
        for idx in range(self.ui.listWidgetBads.count()):
            item = self.ui.listWidgetBads.item(idx)
            item.setSelected(True)
