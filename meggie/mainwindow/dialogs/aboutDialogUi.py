# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'aboutDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(921, 591)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonClose = QtWidgets.QPushButton(Dialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout_2.addWidget(self.pushButtonClose)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelVersion = QtWidgets.QLabel(Dialog)
        self.labelVersion.setObjectName("labelVersion")
        self.horizontalLayout.addWidget(self.labelVersion)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.lineEditVersion = QtWidgets.QLineEdit(Dialog)
        self.lineEditVersion.setMaxLength(100)
        self.lineEditVersion.setReadOnly(True)
        self.lineEditVersion.setObjectName("lineEditVersion")
        self.horizontalLayout.addWidget(self.lineEditVersion)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(Dialog)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Meggie - About"))
        self.pushButtonClose.setText(_translate("Dialog", "Close"))
        self.labelVersion.setText(_translate("Dialog", "Current version:"))
        self.textBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; font-size:11pt;\">Meggie is realeased under the Simplified BSD lisence:</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:11pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">Copyright (c) &lt;2021&gt;, &lt;Kari Aliranta, Jaakko Leppäkangas, Janne Pesonen, Atte Rautio and CIBR&gt;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">All rights reserved.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">Redistribution and use in source and binary forms, with or without</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">modification, are permitted provided that the following conditions are met: </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">1. Redistributions of source code must retain the above copyright notice, this</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">   list of conditions and the following disclaimer. </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">2. Redistributions in binary form must reproduce the above copyright notice,</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">   this list of conditions and the following disclaimer in the documentation</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">   and/or other materials provided with the distribution. </span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS &quot;AS IS&quot; AND</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">The views and conclusions contained in the software and documentation are those</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">of the authors and should not be interpreted as representing official policies, </span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; background-color:#f9f9f9;\"><span style=\" font-family:\'monospace,Courier\'; font-size:11pt; color:#000000; background-color:#f9f9f9;\">either expressed or implied, of the FreeBSD Project.</span></p></body></html>"))
