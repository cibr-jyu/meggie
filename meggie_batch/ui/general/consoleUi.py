# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'console.ui'
#
# Created: Fri Aug 23 12:05:14 2013
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

class Ui_console(object):
    def setupUi(self, console):
        console.setObjectName(_fromUtf8("console"))
        console.resize(759, 169)
        self.gridLayout = QtGui.QGridLayout(console)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEditConsole = QtGui.QTextEdit(console)
        self.textEditConsole.setObjectName(_fromUtf8("textEditConsole"))
        self.gridLayout.addWidget(self.textEditConsole, 0, 0, 1, 1)

        self.retranslateUi(console)
        QtCore.QMetaObject.connectSlotsByName(console)

    def retranslateUi(self, console):
        console.setWindowTitle(_translate("console", "Meggie - Console", None))

