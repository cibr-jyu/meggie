# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UIehdotus1.ui'
#
# Created: Thu Feb 14 15:21:59 2013
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui



try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1081, 707)
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.treeWidget = QtGui.QTreeWidget(self.centralwidget)
        self.treeWidget.setGeometry(QtCore.QRect(0, 0, 256, 192))
        self.treeWidget.setObjectName(_fromUtf8("treeWidget"))
        self.treeWidget.headerItem().setText(0, QtGui.QApplication.translate("MainWindow", "1", None, QtGui.QApplication.UnicodeUTF8))
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget)
        self.treeWidget.topLevelItem(0).setText(0, QtGui.QApplication.translate("MainWindow", "Alkuperäinen raakatiedosto", None, QtGui.QApplication.UnicodeUTF8))
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.treeWidget.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("MainWindow", " sss1 (parametrejä täällä)", None, QtGui.QApplication.UnicodeUTF8))
        item_1 = QtGui.QTreeWidgetItem(item_0)
        self.treeWidget.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("MainWindow", "sss2 (muita parametrejä)", None, QtGui.QApplication.UnicodeUTF8))
        item_2 = QtGui.QTreeWidgetItem(item_1)
        self.treeWidget.topLevelItem(0).child(1).child(0).setText(0, QtGui.QApplication.translate("MainWindow", "sss2 lisäkäsiteltynä (eog?)", None, QtGui.QApplication.UnicodeUTF8))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(265, 0, 811, 651))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1081, 29))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        


    def retranslateUi(self, MainWindow):
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.setSortingEnabled(__sortingEnabled)

"""
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

"""