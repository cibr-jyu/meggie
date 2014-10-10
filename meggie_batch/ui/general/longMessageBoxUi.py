# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/longMessageBox.ui'
#
# Created: Fri Oct 10 13:12:08 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_LongMessageBoxDialog(object):
    def setupUi(self, LongMessageBoxDialog):
        LongMessageBoxDialog.setObjectName(_fromUtf8("LongMessageBoxDialog"))
        LongMessageBoxDialog.resize(614, 480)
        self.gridLayout_2 = QtGui.QGridLayout(LongMessageBoxDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scrollArea = QtGui.QScrollArea(LongMessageBoxDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 594, 427))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(self.scrollAreaWidgetContents)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.pushButtonClose = QtGui.QPushButton(LongMessageBoxDialog)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.gridLayout_2.addWidget(self.pushButtonClose, 1, 0, 1, 1)

        self.retranslateUi(LongMessageBoxDialog)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), LongMessageBoxDialog.close)
        QtCore.QMetaObject.connectSlotsByName(LongMessageBoxDialog)

    def retranslateUi(self, LongMessageBoxDialog):
        LongMessageBoxDialog.setWindowTitle(_translate("LongMessageBoxDialog", "Dialog", None))
        self.pushButtonClose.setText(_translate("LongMessageBoxDialog", "Close", None))

