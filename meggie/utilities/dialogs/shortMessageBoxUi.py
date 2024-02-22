# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shortMessageBoxUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_shortMessageBox(object):
    def setupUi(self, shortMessageBox):
        shortMessageBox.setObjectName("shortMessageBox")
        shortMessageBox.resize(582, 117)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(shortMessageBox.sizePolicy().hasHeightForWidth())
        shortMessageBox.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(shortMessageBox)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButtonClose = QtWidgets.QPushButton(shortMessageBox)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.gridLayout.addWidget(self.pushButtonClose, 1, 1, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(shortMessageBox)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 562, 68))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelMessage = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMessage.sizePolicy().hasHeightForWidth())
        self.labelMessage.setSizePolicy(sizePolicy)
        self.labelMessage.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter
        )
        self.labelMessage.setWordWrap(True)
        self.labelMessage.setObjectName("labelMessage")
        self.gridLayout_2.addWidget(self.labelMessage, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 2)

        self.retranslateUi(shortMessageBox)
        self.pushButtonClose.clicked.connect(shortMessageBox.close)
        QtCore.QMetaObject.connectSlotsByName(shortMessageBox)

    def retranslateUi(self, shortMessageBox):
        _translate = QtCore.QCoreApplication.translate
        shortMessageBox.setWindowTitle(_translate("shortMessageBox", "Meggie"))
        self.pushButtonClose.setText(_translate("shortMessageBox", "Close"))
        self.labelMessage.setText(
            _translate(
                "shortMessageBox",
                "The was a cat behind the all mighty bird singing hallelujah. Who knew it would be so devastating if not all of us? The cries in the woods, howls of the never ending human culture vanishing into thin q numbers.",
            )
        )
