'''
Created on 16.11.2016

@author: jaolpeso
'''
from PyQt4 import QtGui, QtCore

from meggie.ui.preprocessing.badChannelsDialogUi import Ui_Dialog
from meggie.code_meggie.general import fileManager


class BadChannelsDialog(QtGui.QDialog):

    def __init__(self, parent):    
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
        self.initialized = False
        raw = parent.caller.experiment.active_subject.get_working_file()
        self.raw = raw.copy()
        channels = raw.ch_names
        
        for channel in channels:
            item = QtGui.QListWidgetItem(channel)
            self.ui.listWidgetBads.addItem(item)
            if channel in raw.info['bads']:
                item.setSelected(True)
                
        self.initialized = True

    def on_pushButtonSelectAll_clicked(self, checked=None):
        if checked is None:
            return
        
        for idx in range(self.ui.listWidgetBads.count()):
            item = self.ui.listWidgetBads.item(idx)
            item.setSelected(True)

    def on_pushButtonPlot_clicked(self, checked=None):
        if checked is None:
            return
        
        items = self.ui.listWidgetBads.selectedItems()
        self.raw.info['bads'] = [unicode(item.text()) for item in items]
        fig = self.raw.plot()
        
        fig.canvas.mpl_connect('close_event', self.handle_close)
        
    def handle_close(self, event):
        #raw = self.parent.caller.experiment.active_subject.get_working_file()
        bads = self.raw.info['bads']
        for idx in range(self.ui.listWidgetBads.count()):
            item = self.ui.listWidgetBads.item(idx)
            if item.text() in bads:
                item.setSelected(True)
            else:
                item.setSelected(False)
     

    def accept(self):
        items = self.ui.listWidgetBads.selectedItems()
        self.raw.info['bads'] = [unicode(item.text()) for item in items]
         
        experiment = self.parent.caller.experiment
        fname = self.raw.info['filename']
        fileManager.save_raw(experiment, self.raw, fname, overwrite=True)
        experiment.action_logger.log_message(''.join([
            'Raw plot bad channels selected for file: ',
            fname, '\n', str(self.raw.info['bads'])]))
        
        original_raw = self.parent.caller.experiment.active_subject.get_working_file()
        original_raw.info['bads'] = self.raw.info['bads']

        self.parent.initialize_ui()
        self.close()
