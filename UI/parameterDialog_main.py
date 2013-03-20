'''
Created on Mar 19, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui
from epochParameterDialog_UI import Ui_ParameterDialog
class ParameterDialog(QtGui.QDialog):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self)
        self.ui = Ui_ParameterDialog()
        self.ui.setupUi(self)
        self.fileEdit = self.ui.FilePathLineEdit

        
    def on_browseButton_clicked(self, checked=None):
        """
        Called when Browse-button is pressed. Opens a file browser.        
        """
        if checked is None: return # Standard workaround for file dialog opening twice
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '/usr/local/bin/ParkkosenPurettu/meg/jn')
        self.fileEdit.setText(self.fname)
        
    def accept(self):
        """
        Called when the OK button is pressed.
        """
        self.fname = self.fileEdit.text()
        print self.fname
        self.close()
        
        