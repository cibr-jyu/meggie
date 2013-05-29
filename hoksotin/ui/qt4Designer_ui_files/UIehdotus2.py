# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIehdotus2.ui'
#
# Created: Wed Mar  6 17:02:02 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal
import EOG

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1081, 707)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_2 = QtGui.QTreeWidgetItem(item_1)
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(265, 0, 811, 651))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        
        
        self.drawSimpleFunction = QtGui.QPushButton(self.centralwidget)
        self.drawSimpleFunction.setGeometry(QtCore.QRect(70, 280, 95, 31))
        self.drawSimpleFunction.setObjectName(_fromUtf8("drawSimpleFunction"))
        
        self.EventMarginalMin = QtGui.QLineEdit(self.centralwidget)
        self.EventMarginalMin.setGeometry(QtCore.QRect(20,220,51,31))
        self.EventMarginalMin.setObjectName(_fromUtf8("EventMinMarginLineEdit"))

        self.EventMarginalMax = QtGui.QLineEdit(self.centralwidget)
        self.EventMarginalMax.setGeometry(QtCore.QRect(90,220,51,31))
        self.EventMarginalMax.setObjectName(_fromUtf8("EventMaxMarginLineEdit"))
        
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuTools = QtGui.QMenu(self.menubar)
        self.menuTools.setObjectName(_fromUtf8("menuTools"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionLoad_file = QtGui.QAction(MainWindow)
        self.actionLoad_file.setObjectName(_fromUtf8("actionLoad_file"))
        self.actionSave_file = QtGui.QAction(MainWindow)
        self.actionSave_file.setObjectName(_fromUtf8("actionSave_file"))
        self.actionPreferences = QtGui.QAction(MainWindow)
        self.actionPreferences.setObjectName(_fromUtf8("actionPreferences"))
        self.menuFile.addAction(self.actionLoad_file)
        self.menuFile.addAction(self.actionSave_file)
        self.menuTools.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())


        self.drawSimpleFunction.clicked.connect(self.drawEOGEpochs)        

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def drawEOGEpochs(self):
        min = self.EventMarginalMin.text()
        max = self.EventMarginalMax.text()
        EOG.drawEOGEpochs(float(min), float(max), 'STI 001')
                

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "1", None))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "Alkuperäinen raakatiedosto", None))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", " sss1 (parametrejä täällä)", None))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "sss2 (muita parametrejä)", None))
        self.treeWidget.topLevelItem(0).child(1).child(0).setText(0, _translate("MainWindow", "sss2 lisäkäsiteltynä (eog?)", None))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.drawSimpleFunction.setText(_translate("MainWindow", "PushButton", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

