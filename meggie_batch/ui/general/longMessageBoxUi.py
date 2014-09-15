# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/longMessageBox.ui'
#
# Created: Mon Sep 15 17:05:12 2014
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
        LongMessageBoxDialog.resize(436, 362)
        self.gridLayout_2 = QtGui.QGridLayout(LongMessageBoxDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.scrollArea = QtGui.QScrollArea(LongMessageBoxDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 416, 309))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textBrowser = QtGui.QTextBrowser(self.scrollAreaWidgetContents)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.gridLayout.addWidget(self.textBrowser, 0, 0, 1, 1)
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
        self.textBrowser.setHtml(_translate("LongMessageBoxDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:9.5pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:10pt;\"><br /></p></body></html>", None))
        self.pushButtonClose.setText(_translate("LongMessageBoxDialog", "Close", None))

