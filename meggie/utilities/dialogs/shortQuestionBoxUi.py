# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortQuestionBoxUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_shortQuestionBox(object):
    def setupUi(self, shortQuestionBox):
        shortQuestionBox.setObjectName("shortQuestionBox")
        shortQuestionBox.resize(582, 117)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(shortQuestionBox.sizePolicy().hasHeightForWidth())
        shortQuestionBox.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(shortQuestionBox)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(shortQuestionBox)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayout.addWidget(self.pushButtonCancel, 1, 1, 1, 1)
        self.pushButtonOk = QtWidgets.QPushButton(shortQuestionBox)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.gridLayout.addWidget(self.pushButtonOk, 1, 2, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(shortQuestionBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 562, 68))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelMessage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy)
        self.labelMessage.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName("labelMessage")
        self.gridLayout_2.addWidget(self.labelMessage, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 3)

        self.retranslateUi(shortQuestionBox)
        self.pushButtonOk.clicked.connect(shortQuestionBox.accept)
        self.pushButtonCancel.clicked.connect(shortQuestionBox.reject)
        QtCore.QMetaObject.connectSlotsByName(shortQuestionBox)

    def retranslateUi(self, shortQuestionBox):
        _translate = QtCore.QCoreApplication.translate
        shortQuestionBox.setWindowTitle(_translate("shortQuestionBox", "Meggie"))
        self.pushButtonCancel.setText(_translate("shortQuestionBox", "Cancel"))
        self.pushButtonOk.setText(_translate("shortQuestionBox", "Ok"))
        self.labelMessage.setText(_translate("shortQuestionBox", "The was a cat behind the all mighty bird singing hallelujah. Who knew it would be so devastating if not all of us? The cries in the woods, howls of the never ending human culture vanishing into thin q numbers."))

