'''
Created on May 2, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui

from epochWidget_Ui import Ui_Form

class EpochWidget(QtGui.QWidget):
    '''
    classdocs
    '''


    def __init__(self, parent):
        '''
        Constructor
        '''
        QtGui.QWidget.__init__(self, parent)
        #QtGui.QDialog.__init__(self)
        
        self.ui = Ui_Form()
        self.ui.setupUi(self)