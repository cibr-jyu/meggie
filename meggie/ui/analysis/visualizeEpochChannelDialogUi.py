# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../visualizeEpochChannelDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VisualizeEpochChannelDialog(object):
    def setupUi(self, VisualizeEpochChannelDialog):
        VisualizeEpochChannelDialog.setObjectName("VisualizeEpochChannelDialog")
        VisualizeEpochChannelDialog.resize(499, 328)
        self.gridLayout_3 = QtWidgets.QGridLayout(VisualizeEpochChannelDialog)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.scrollArea = QtWidgets.QScrollArea(VisualizeEpochChannelDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 479, 269))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelChannels = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelChannels.setObjectName("labelChannels")
        self.gridLayout.addWidget(self.labelChannels, 0, 0, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelSigma = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.labelSigma.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelSigma.setObjectName("labelSigma")
        self.horizontalLayout.addWidget(self.labelSigma)
        self.doubleSpinBoxSigma = QtWidgets.QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBoxSigma.setSingleStep(0.05)
        self.doubleSpinBoxSigma.setProperty("value", 0.5)
        self.doubleSpinBoxSigma.setObjectName("doubleSpinBoxSigma")
        self.horizontalLayout.addWidget(self.doubleSpinBoxSigma)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.listWidgetChannels = QtWidgets.QListWidget(self.scrollAreaWidgetContents)
        self.listWidgetChannels.setObjectName("listWidgetChannels")
        self.gridLayout.addWidget(self.listWidgetChannels, 1, 0, 1, 1)
        self.pushButtonVisualizeChannel = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonVisualizeChannel.setObjectName("pushButtonVisualizeChannel")
        self.gridLayout.addWidget(self.pushButtonVisualizeChannel, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonClose = QtWidgets.QPushButton(VisualizeEpochChannelDialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayout_2.addWidget(self.pushButtonClose)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(VisualizeEpochChannelDialog)
        self.pushButtonClose.clicked.connect(VisualizeEpochChannelDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VisualizeEpochChannelDialog)

    def retranslateUi(self, VisualizeEpochChannelDialog):
        _translate = QtCore.QCoreApplication.translate
        VisualizeEpochChannelDialog.setWindowTitle(_translate("VisualizeEpochChannelDialog", "Meggie - Visualize epoch channels"))
        self.labelChannels.setText(_translate("VisualizeEpochChannelDialog", "Pick channel:"))
        self.labelSigma.setText(_translate("VisualizeEpochChannelDialog", "Gaussian smoothing:"))
        self.pushButtonVisualizeChannel.setText(_translate("VisualizeEpochChannelDialog", "Visualize selected channel"))
        self.pushButtonClose.setText(_translate("VisualizeEpochChannelDialog", "Close"))

