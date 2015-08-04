# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/shortMessageBox.ui'
#
# Created: Thu Nov  6 15:37:16 2014
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

class Ui_shortMessageBox(object):
    def setupUi(self, shortMessageBox):
        shortMessageBox.setObjectName(_fromUtf8("shortMessageBox"))
        shortMessageBox.resize(585, 425)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(shortMessageBox.sizePolicy().hasHeightForWidth())
        shortMessageBox.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(shortMessageBox)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelMessage = QtGui.QLabel(shortMessageBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy)
        self.labelMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName(_fromUtf8("labelMessage"))
        self.gridLayout.addWidget(self.labelMessage, 2, 0, 1, 1)
        self.pushButtonClose = QtGui.QPushButton(shortMessageBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonClose.sizePolicy().hasHeightForWidth())
        self.pushButtonClose.setSizePolicy(sizePolicy)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.gridLayout.addWidget(self.pushButtonClose, 3, 0, 1, 1)

        self.retranslateUi(shortMessageBox)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), shortMessageBox.close)
        QtCore.QMetaObject.connectSlotsByName(shortMessageBox)

    def retranslateUi(self, shortMessageBox):
        shortMessageBox.setWindowTitle(_translate("shortMessageBox", "Error", None))
        self.labelMessage.setText(_translate("shortMessageBox", "textLabel", None))
        self.pushButtonClose.setText(_translate("shortMessageBox", "Close", None))

