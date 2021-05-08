# coding: utf-8

"""
"""

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.shortQuestionBoxUi import Ui_shortQuestionBox


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
        self.handler(True)
        super(shortQuestionBox, self).accept()

    def reject(self):
        self.handler(False)
        super(shortQuestionBox, self).reject()
