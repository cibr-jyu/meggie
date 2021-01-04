# coding: utf-8

"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.utilities.dialogs.shortMessageBoxUi import Ui_shortMessageBox
from meggie.utilities.dialogs.shortQuestionBoxUi import Ui_shortQuestionBox


class shortMessageBox(QtWidgets.QDialog):
    """
    Class for creating simple messageboxes displaying messages
    """

    def __init__(self, message, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_shortMessageBox()
        self.ui.setupUi(self)

        self.setWindowTitle('Meggie - Info')
        self.ui.labelMessage.setText(message)

class shortQuestionBox(QtWidgets.QDialog):
    """
    Class for creating simple messageboxes displaying questions
    """

    def __init__(self, message, parent, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_shortQuestionBox()
        self.ui.setupUi(self)

        self.setWindowTitle('Meggie - Question')
        self.ui.labelMessage.setText(message)

        self.handler = handler

    def accept(self):
        self.handler()
        self.close()

