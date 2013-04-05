'''
Created on Apr 4, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui

class Tab(object):

    def __init__(self, title, ui):
        '''
        Constructor
        '''
        ui.tab = QtGui.QWidget()
        ui.tabWidget.addTab(ui.tab, title)
        self.horizontalLayoutWidget = QtGui.QWidget(ui.tab)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 60, 341, 481))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.metaBox = QtGui.QGroupBox(self.horizontalLayoutWidget)
        self.metaBox.setTitle("Background")
        self.verticalLayout.addWidget(self.metaBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

class EpochTab(Tab):
    
    def __init__(self, title, ui):
        super(EpochTab, self).__init__( title, ui)
        
        
    