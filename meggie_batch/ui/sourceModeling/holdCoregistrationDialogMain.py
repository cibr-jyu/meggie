'''
Created on 10.11.2014

@author: Kari Aliranta
'''

from PyQt4 import QtCore, QtGui
from holdCoregistrationDialogUi import Ui_DialogHoldCoregistration
import fileManager
import os

class holdCoregistrationDialog(QtGui.QDialog):
    
    
    def __init__(self, parent, activeSubject, selectedFmodelName):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogHoldCoregistration()
        self.ui.setupUi(self)
        
        self.subject = activeSubject
        self.fModel = selectedFmodelName
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.center()
    
    
    def center(self):
        """
        Center the window on screen.
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        mysize = self.geometry()
        hpos = ( screen.width() - mysize.width() ) / 2
        vpos = ( screen.height() - mysize.height() ) / 2
        self.move(hpos, vpos)

    
    def on_pushButtonCancel_clicked(self, checked=None):
        if checked is None: return
        self.close()
    
        
    def on_pushButtonCopy_clicked(self, checked=None):
        if checked is None: return
        
        transFilePath = os.path.join(self.subject._subject_path, 
                                     'reconFiles-trans.fif')
        
        if not os.path.isfile(transFilePath):
            self.ui.labelTransFileWarning.setHidden(False)
            return
        
        if fileManager.move_trans_file(self.subject, self.fModel):
            self.close()
        else: 
            message = 'There was an unknown problem copying the trans file. '
            self.ui.labelTransFileWarning.setText(message)
            self.ui.labelTransFileWarning.setHidden(False)