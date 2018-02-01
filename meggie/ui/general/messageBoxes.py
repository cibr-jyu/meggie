# coding: utf-8


"""
@author: Kari Aliranta, Jaakko Leppakangas
Contains the shortMessageBox class used for simple messageboxes,and the 
longMessageBox for longer messages that need a scrolling content area.
"""

from PyQt4 import QtCore, QtGui
from meggie.ui.general.longMessageBoxUi import Ui_LongMessageBoxDialog
from meggie.ui.general.shortMessageBoxUi import Ui_shortMessageBox
from meggie.ui.general.shortMessageBoxQuestionYesNoUi import Ui_shortMessageBoxQuestionYesNo


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


class shortMessageBoxQuestionYesNo(QtGui.QDialog):
    """
    A class for simple non-modal question messageBox in the
    style of QMessageBox.question. 
    """
    def __init__(self, message, parent=None, title='title'):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_shortMessageBoxQuestionYesNo()
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.ui.labelMessage.setText(message)
        self.returnValue = 'no'
        
    def get_return_value(self):
        return self.returnValue
        
    def accept(self):
        self.returnValue = 'yes'
        self.close()
        
    def reject(self):
        self.close()


class longMessageBox(QtGui.QDialog):
    """
    Class for larger, scrollable messageboxes, needed for longer errors and
    output.
    """
    
    def __init__(self, title, message, parent=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_LongMessageBoxDialog()
        self.ui.setupUi(self)
    
        self.setWindowTitle(title)
        self.ui.textEdit.setText(message)
            
            
    def updateOutputField(self):
        cursor = self.output.textCursor()
        cursor.movePosition(cursor.End)
        cursor.insertText(str(self.process.readAll()))
        self.output.ensureCursorVisible()
    
    
    def accept(self):
        self.close()


