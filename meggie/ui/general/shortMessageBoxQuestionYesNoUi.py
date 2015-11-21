# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/shortMessageBoxQuestionYesNo.ui'
#
# Created: Mon Feb 23 18:28:00 2015
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

class Ui_shortMessageBoxQuestionYesNo(object):
    def setupUi(self, shortMessageBoxQuestionYesNo):
        shortMessageBoxQuestionYesNo.setObjectName(_fromUtf8("shortMessageBoxQuestionYesNo"))
        shortMessageBoxQuestionYesNo.resize(582, 249)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(shortMessageBoxQuestionYesNo.sizePolicy().hasHeightForWidth())
        shortMessageBoxQuestionYesNo.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(shortMessageBoxQuestionYesNo)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelMessage = QtGui.QLabel(shortMessageBoxQuestionYesNo)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy)
        self.labelMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName(_fromUtf8("labelMessage"))
        self.gridLayout.addWidget(self.labelMessage, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(shortMessageBoxQuestionYesNo)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(shortMessageBoxQuestionYesNo)
        QtCore.QMetaObject.connectSlotsByName(shortMessageBoxQuestionYesNo)

    def retranslateUi(self, shortMessageBoxQuestionYesNo):
        shortMessageBoxQuestionYesNo.setWindowTitle(_translate("shortMessageBoxQuestionYesNo", "title", None))
        self.labelMessage.setText(_translate("shortMessageBoxQuestionYesNo", "textLabel", None))

