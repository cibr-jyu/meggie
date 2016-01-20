# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logDialog.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        LogDialog.setObjectName(_fromUtf8("LogDialog"))
        LogDialog.resize(1089, 710)
        self.gridLayout = QtGui.QGridLayout(LogDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.textEdit = QtGui.QTextEdit(LogDialog)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonClose = QtGui.QPushButton(LogDialog)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(LogDialog)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), LogDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(LogDialog)

    def retranslateUi(self, LogDialog):
        LogDialog.setWindowTitle(_translate("LogDialog", "Dialog", None))
        self.pushButtonClose.setText(_translate("LogDialog", "Close", None))

