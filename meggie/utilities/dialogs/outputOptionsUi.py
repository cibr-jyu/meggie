# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'outputOptionsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_outputOptions(object):
    def setupUi(self, outputOptions):
        outputOptions.setObjectName("outputOptions")
        outputOptions.resize(255, 149)
        self.gridLayout = QtWidgets.QGridLayout(outputOptions)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxType = QtWidgets.QGroupBox(outputOptions)
        self.groupBoxType.setObjectName("groupBoxType")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxType)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButtonAllChannels = QtWidgets.QRadioButton(self.groupBoxType)
        self.radioButtonAllChannels.setChecked(True)
        self.radioButtonAllChannels.setObjectName("radioButtonAllChannels")
        self.gridLayout_2.addWidget(self.radioButtonAllChannels, 0, 0, 1, 1)
        self.radioButtonChannelAverages = QtWidgets.QRadioButton(self.groupBoxType)
        self.radioButtonChannelAverages.setObjectName("radioButtonChannelAverages")
        self.gridLayout_2.addWidget(self.radioButtonChannelAverages, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxType, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(outputOptions)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(outputOptions)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)

        self.retranslateUi(outputOptions)
        self.pushButtonCancel.clicked.connect(outputOptions.reject)
        self.pushButtonAccept.clicked.connect(outputOptions.accept)
        QtCore.QMetaObject.connectSlotsByName(outputOptions)

    def retranslateUi(self, outputOptions):
        _translate = QtCore.QCoreApplication.translate
        outputOptions.setWindowTitle(_translate("outputOptions", "Meggie - Output options"))
        self.groupBoxType.setTitle(_translate("outputOptions", "Type"))
        self.radioButtonAllChannels.setText(_translate("outputOptions", "All channels"))
        self.radioButtonChannelAverages.setText(_translate("outputOptions", "Channel averages"))
        self.pushButtonCancel.setText(_translate("outputOptions", "Cancel"))
        self.pushButtonAccept.setText(_translate("outputOptions", "Accept"))

