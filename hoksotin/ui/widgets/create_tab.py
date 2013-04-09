'''
Created on Apr 4, 2013

@author: jaeilepp
'''
from PyQt4 import QtCore,QtGui

from infoDialog_Ui import Ui_infoDialog

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
        self.horizontalLayout.addLayout(self.verticalLayout)
        
class EpochTab(Tab):
    
    def __init__(self, title, ui):
        super(EpochTab, self).__init__( title, ui)
        ui = Ui_infoDialog()
        ui.setupUi(self.horizontalLayoutWidget)
        """
        self.layoutWidget_2 = QtGui.QWidget(self.metaBox)
        self.layoutWidget_2.setGeometry(QtCore.QRect(26, 35, 271, 54))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_6.setMargin(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.labelDate = QtGui.QLabel(self.layoutWidget_2)
        self.labelDate.setObjectName("labelDate")
        self.labelDate.setText('Date:')

        """
        
    