'''
Created on Apr 4, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui

from infoDialog_Ui import Ui_infoDialog

class Tab(object):

    
    def __init__(self, title, ui, id):
        '''
        Constructor
        '''
        
        ui.tab = QtGui.QWidget()
        ui.tabWidget.addTab(ui.tab, title)
        ui.tab.winId = id
        self.horizontalLayoutWidget = QtGui.QWidget(ui.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 341, 481))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.horizontalLayout.addLayout(self.verticalLayout)
        
class EpochTab(Tab):
    
    def __init__(self, title, ui, id):
        super(EpochTab, self).__init__(title, ui, id)
        ui = Ui_infoDialog()
        ui.setupUi(self.horizontalLayoutWidget)
        
        
        
    @property    
    def id(self):
        return self._id
    
    @id.setter
    def id(self, id):
        self._id = id