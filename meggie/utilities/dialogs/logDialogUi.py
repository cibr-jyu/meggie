# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LogDialog(object):
    def setupUi(self, LogDialog):
        LogDialog.setObjectName("LogDialog")
        LogDialog.resize(649, 710)
        self.gridLayout = QtWidgets.QGridLayout(LogDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textEditBrowser = QtWidgets.QTextEdit(LogDialog)
        self.textEditBrowser.setObjectName("textEditBrowser")
        self.verticalLayout.addWidget(self.textEditBrowser)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonClose = QtWidgets.QPushButton(LogDialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout.addWidget(self.pushButtonClose)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 3, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelBufferSize = QtWidgets.QLabel(LogDialog)
        self.labelBufferSize.setObjectName("labelBufferSize")
        self.horizontalLayout_3.addWidget(self.labelBufferSize)
        self.spinBoxBufferSize = QtWidgets.QSpinBox(LogDialog)
        self.spinBoxBufferSize.setMinimumSize(QtCore.QSize(80, 0))
        self.spinBoxBufferSize.setMaximum(1000000)
        self.spinBoxBufferSize.setSingleStep(100)
        self.spinBoxBufferSize.setProperty("value", 5000)
        self.spinBoxBufferSize.setObjectName("spinBoxBufferSize")
        self.horizontalLayout_3.addWidget(self.spinBoxBufferSize)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButtonBufferSize = QtWidgets.QPushButton(LogDialog)
        self.pushButtonBufferSize.setObjectName("pushButtonBufferSize")
        self.horizontalLayout_3.addWidget(self.pushButtonBufferSize)
        self.gridLayout.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBoxShowMeggie = QtWidgets.QCheckBox(LogDialog)
        self.checkBoxShowMeggie.setChecked(True)
        self.checkBoxShowMeggie.setObjectName("checkBoxShowMeggie")
        self.horizontalLayout_2.addWidget(self.checkBoxShowMeggie)
        self.checkBoxShowMNE = QtWidgets.QCheckBox(LogDialog)
        self.checkBoxShowMNE.setObjectName("checkBoxShowMNE")
        self.horizontalLayout_2.addWidget(self.checkBoxShowMNE)
        self.checkBoxShowMNEcall = QtWidgets.QCheckBox(LogDialog)
        self.checkBoxShowMNEcall.setObjectName("checkBoxShowMNEcall")
        self.horizontalLayout_2.addWidget(self.checkBoxShowMNEcall)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(LogDialog)
        self.pushButtonClose.clicked.connect(LogDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(LogDialog)

    def retranslateUi(self, LogDialog):
        _translate = QtCore.QCoreApplication.translate
        LogDialog.setWindowTitle(_translate("LogDialog", "Dialog"))
        self.pushButtonClose.setText(_translate("LogDialog", "Close"))
        self.labelBufferSize.setText(_translate("LogDialog", "Buffer size (lines):"))
        self.pushButtonBufferSize.setText(_translate("LogDialog", "Accept"))
        self.checkBoxShowMeggie.setText(_translate("LogDialog", "Meggie"))
        self.checkBoxShowMNE.setText(_translate("LogDialog", "MNE"))
        self.checkBoxShowMNEcall.setText(_translate("LogDialog", "MNE call"))

