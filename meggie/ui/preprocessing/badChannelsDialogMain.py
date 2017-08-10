"""
Created on 16.11.2016

@author: jaolpeso
"""

from PyQt4 import QtGui

from meggie.ui.preprocessing.badChannelsDialogUi import Ui_Dialog
from meggie.code_meggie.general import fileManager


class BadChannelsDialog(QtGui.QDialog):
    """ Handles bad channel selection by allowing bad channels to be selected
    either on a list widget or the raw plot
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.raw = None

        raw = parent.experiment.active_subject.get_working_file()
        channels = raw.ch_names

        for channel in channels:
            item = QtGui.QListWidgetItem(channel)
            self.ui.listWidgetBads.addItem(item)
            if channel in raw.info['bads']:
                item.setSelected(True)

    def on_pushButtonSelectAll_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        for idx in range(self.ui.listWidgetBard.count()):
            self.ui.listWidgetBads.item(idx).setSelected(True)

    def on_pushButtonPlot_clicked(self, checked=None):
        """ Sync channels from list to plot
        """
        if checked is None:
            return

        self.raw = self.parent.experiment.active_subject.get_working_file().copy()
        items = self.ui.listWidgetBads.selectedItems()
        self.raw.info['bads'] = [unicode(item.text()) for item in items]
        fig = self.raw.plot()
        fig.canvas.mpl_connect('close_event', self.handle_close)

    def handle_close(self, event):
        """ Sync bad channels from plot to list
        """
        bads = self.raw.info['bads']
        for idx in range(self.ui.listWidgetBads.count()):
            item = self.ui.listWidgetBads.item(idx)
            if item.text() in bads:
                item.setSelected(True)
            else:
                item.setSelected(False)

        self.raw = None

    def accept(self):
        """
        """
        items = self.ui.listWidgetBads.selectedItems()

        raw = self.parent.experiment.active_subject.get_working_file()

        raw.info['bads'] = [unicode(item.text()) for item in items]
        experiment = self.parent.experiment
        fname = raw.info['filename']
        fileManager.save_raw(experiment, raw, fname, overwrite=True)
        experiment.action_logger.log_message(''.join([
            'Raw plot bad channels selected for file: ',
            fname, '\n', str(raw.info['bads'])]))

        self.parent.initialize_ui()
        self.close()
