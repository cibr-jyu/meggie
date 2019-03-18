"""
"""
import logging

from PyQt5 import QtWidgets

from meggie.ui.analysis.outputOptionsUi import Ui_outputOptions
from meggie.ui.utils.messaging import exc_messagebox


class OutputOptions(QtWidgets.QDialog):
    
    def __init__(self, parent, handler=None, 
                 row_setting=None):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_outputOptions()
        self.ui.setupUi(self)
        self.parent = parent
        self.handler = handler

        if row_setting == 'channel_averages':
            self.ui.radioButtonChannelAverages.setChecked(True)
        
    def accept(self):

        if self.ui.radioButtonChannelAverages.isChecked():
            row_setting = 'channel_averages'
        else:
            row_setting = 'all_channels'

        if self.handler:
            try:
                self.handler(row_setting=row_setting)
            except Exception as exc:
                exc_messagebox(self.parent, exc)

        self.close()

