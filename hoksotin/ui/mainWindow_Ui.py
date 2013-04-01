# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created: Tue Mar 26 14:54:51 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        MainWindow.resize(324, 221)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.widget = QtGui.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 30, 211, 91))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ButtonNewProject = QtGui.QPushButton(self.widget)
        self.ButtonNewProject.setObjectName(_fromUtf8("ButtonNewProject"))
        self.verticalLayout.addWidget(self.ButtonNewProject)
        self.ButtonOpenProject = QtGui.QPushButton(self.widget)
        self.ButtonOpenProject.setObjectName(_fromUtf8("ButtonOpenProject"))
        self.verticalLayout.addWidget(self.ButtonOpenProject)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 324, 29))
        self.menubar.setDefaultUp(False)
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
        self.actionShow_project_creation_dialog = QtGui.QAction(MainWindow)
        self.actionShow_project_creation_dialog.setObjectName(_fromUtf8("actionShow_project_creation_dialog"))
        self.menuFile.addAction(self.actionLoad_file)
        self.menuFile.addAction(self.actionSave_file)
        self.menuTools.addAction(self.actionPreferences)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.ButtonNewProject.setText(_translate("MainWindow", "Create new project", None))
        self.ButtonOpenProject.setText(_translate("MainWindow", "Open existing project", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuTools.setTitle(_translate("MainWindow", "Tools", None))
        self.actionLoad_file.setText(_translate("MainWindow", "Load file", None))
        self.actionSave_file.setText(_translate("MainWindow", "Save file", None))
        self.actionPreferences.setText(_translate("MainWindow", "Preferences", None))
        self.actionShow_project_creation_dialog.setText(_translate("MainWindow", "Show project creation dialog", None))

