""" Contains a class for logic of the short question box.
"""

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.shortQuestionBoxUi import Ui_shortQuestionBox


class shortQuestionBox(QtWidgets.QDialog):
    """ Contains logic for the short question box.
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
