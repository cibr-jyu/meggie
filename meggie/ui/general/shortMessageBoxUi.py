# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../shortMessageBoxUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_shortMessageBox(object):
    def setupUi(self, shortMessageBox):
        shortMessageBox.setObjectName("shortMessageBox")
        shortMessageBox.resize(582, 249)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(shortMessageBox.sizePolicy().hasHeightForWidth())
        shortMessageBox.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(shortMessageBox)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.labelMessage = QtWidgets.QLabel(shortMessageBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy)
        self.labelMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName("labelMessage")
        self.gridLayout.addWidget(self.labelMessage, 2, 0, 1, 1)
        self.pushButtonClose = QtWidgets.QPushButton(shortMessageBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonClose.sizePolicy().hasHeightForWidth())
        self.pushButtonClose.setSizePolicy(sizePolicy)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout.addWidget(self.pushButtonClose, 3, 0, 1, 1)

        self.retranslateUi(shortMessageBox)
        self.pushButtonClose.clicked.connect(shortMessageBox.close)
        QtCore.QMetaObject.connectSlotsByName(shortMessageBox)

    def retranslateUi(self, shortMessageBox):
        _translate = QtCore.QCoreApplication.translate
        shortMessageBox.setWindowTitle(_translate("shortMessageBox", "Error"))
        self.labelMessage.setText(_translate("shortMessageBox", "textLabel"))
        self.pushButtonClose.setText(_translate("shortMessageBox", "Close"))

