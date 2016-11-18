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
        channels = raw.ch_names
        
        for channel in channels:
            item = QtGui.QListWidgetItem(channel)
            self.ui.listWidgetBads.addItem(item)
            if channel in raw.info['bads']:
                item.setSelected(True)
                
        self.initialized = True

    def on_listWidgetBads_itemSelectionChanged(self):
        if not self.initialized:
            return
        raw = self.parent.caller.experiment.active_subject.get_working_file()
        raw.info['bads'] = []
        items = self.ui.listWidgetBads.selectedItems()
        for item in items:
            raw.info['bads'].append(unicode(item.text()))

    def on_pushButtonSelectAll_clicked(self, checked=None):
        if checked is None:
            return
        
        for idx in range(self.ui.listWidgetBads.count()):
            item = self.ui.listWidgetBads.item(idx)
            item.setSelected(True)

    def on_pushButtonPlot_clicked(self, checked=None):
        if checked is None:
            return
        
        raw = self.parent.caller.experiment.active_subject.get_working_file()
        fig = raw.plot()
        fig.canvas.mpl_connect('close_event', self.handle_close)
        
    def handle_close(self, event):
        raw = self.parent.caller.experiment.active_subject.get_working_file()
        bads = raw.info['bads']
        for bad in bads:
            chnls = self.ui.listWidgetBads.findItems(bad, QtCore.Qt.MatchExactly)
            for itm in chnls:
                itm.setSelected(True)        

    def accept(self):
        items = self.ui.listWidgetBads.selectedItems()
        raw = self.parent.caller.experiment.active_subject.get_working_file()
        raw.info['bads'] = []
 
        for item in items:
            raw.info['bads'].append(unicode(item.text()))
         
        experiment = self.parent.caller.experiment
        fname = raw.info['filename']
        fileManager.save_raw(experiment, raw, fname, overwrite=True)
        experiment.action_logger.log_message(''.join([
            'Raw plot bad channels selected for file: ',
            fname, '\n', str(raw.info['bads'])]))
        self.parent.initialize_ui()
        self.close()
