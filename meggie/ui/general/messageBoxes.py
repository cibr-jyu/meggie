# coding: utf-8

"""
"""

from PyQt4 import QtCore, QtGui
from meggie.ui.general.shortMessageBoxUi import Ui_shortMessageBox


class shortMessageBox(QtGui.QDialog):
    """
    Class for creating simple messageboxes displaying error messages.
    """
    
    def __init__(self, message, parent=None, title='Error'):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_shortMessageBox()
        self.ui.setupUi(self)
    
        self.setWindowTitle(title)

        try:
            message = unicode(message, 'utf-8')
        except TypeError:
            message = unicode(message)

        self.ui.labelMessage.setText(message.encode('utf-8'))


