""" Contains a class for logic of the output options dialog.
"""
import logging

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.outputOptionsUi import Ui_outputOptions


class OutputOptions(QtWidgets.QDialog):
    """ Contains logic for the output options dialog.
    """

    def __init__(self, parent, handler=None,
                 selected_option=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_outputOptions()
        self.ui.setupUi(self)
        self.parent = parent
        self.handler = handler

        if selected_option == 'channel_averages':
            self.ui.radioButtonChannelAverages.setChecked(True)

    def accept(self):
        if self.ui.radioButtonChannelAverages.isChecked():
            selected_option = 'channel_averages'
        else:
            selected_option = 'all_channels'

        if self.handler:
            self.handler(selected_option=selected_option)

        self.close()
