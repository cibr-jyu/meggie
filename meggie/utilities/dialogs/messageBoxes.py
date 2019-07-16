# coding: utf-8

"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.utilities.dialogs.shortMessageBoxUi import Ui_shortMessageBox


class shortMessageBox(QtWidgets.QDialog):
    """
    Class for creating simple messageboxes displaying error messages.
    """

    def __init__(self, message, parent=None, title='Error'):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_shortMessageBox()
        self.ui.setupUi(self)

        self.setWindowTitle(title)
        self.ui.labelMessage.setText(message)
