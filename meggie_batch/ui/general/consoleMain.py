'''
Created on Aug 23, 2013

@author: jaolpeso
'''

from PyQt4 import QtCore,QtGui
from consoleUi import Ui_console

class Console(QtGui.QWidget):
    """
    Logs the output of Meggie's processes.
    """
    
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.ui = Ui_console()
        self.ui.setupUi(self)
        self.output = ''
        
        
    def show_log(self, output):
        """
        Shows the logged output string.
        """
        self.ui.textEditConsole.append(output)
        # Repaint method paints the ui in real time, while update method only
        # after process ends.
        self.repaint()
        
        
    def show_error_log(self, error):
        """
        Shows the error output string.
        """
        self.ui.textEditConsoleError.append(error)
        self.repaint()