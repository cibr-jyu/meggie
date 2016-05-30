# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerSpectrumEpochsDialogUi.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(276, 170)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.comboBoxChannelType = QtGui.QComboBox(self.groupBox)
        self.comboBoxChannelType.setGeometry(QtCore.QRect(10, 30, 201, 29))
        self.comboBoxChannelType.setObjectName(_fromUtf8("comboBoxChannelType"))
        self.checkBoxNormalize = QtGui.QCheckBox(self.groupBox)
        self.checkBoxNormalize.setGeometry(QtCore.QRect(10, 70, 201, 26))
        self.checkBoxNormalize.setChecked(True)
        self.checkBoxNormalize.setObjectName(_fromUtf8("checkBoxNormalize"))
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Meggie - Power spectrum epochs", None))
        self.groupBox.setTitle(_translate("Dialog", "Select channel type for visualization", None))
        self.checkBoxNormalize.setText(_translate("Dialog", "normalize", None))

