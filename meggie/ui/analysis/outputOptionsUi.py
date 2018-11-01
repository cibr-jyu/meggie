# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../outputOptions.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_outputOptions(object):
    def setupUi(self, outputOptions):
        outputOptions.setObjectName("outputOptions")
        outputOptions.resize(313, 175)
        self.formLayout = QtWidgets.QFormLayout(outputOptions)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxRows = QtWidgets.QGroupBox(outputOptions)
        self.groupBoxRows.setObjectName("groupBoxRows")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxRows)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.radioButtonAllChannels = QtWidgets.QRadioButton(self.groupBoxRows)
        self.radioButtonAllChannels.setChecked(True)
        self.radioButtonAllChannels.setObjectName("radioButtonAllChannels")
        self.gridLayout_2.addWidget(self.radioButtonAllChannels, 0, 0, 1, 1)
        self.radioButtonChannelAverages = QtWidgets.QRadioButton(self.groupBoxRows)
        self.radioButtonChannelAverages.setObjectName("radioButtonChannelAverages")
        self.gridLayout_2.addWidget(self.radioButtonChannelAverages, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxRows, 0, 0, 1, 1)
        self.groupBoxColumns = QtWidgets.QGroupBox(outputOptions)
        self.groupBoxColumns.setObjectName("groupBoxColumns")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxColumns)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.radioButtonAllData = QtWidgets.QRadioButton(self.groupBoxColumns)
        self.radioButtonAllData.setChecked(True)
        self.radioButtonAllData.setObjectName("radioButtonAllData")
        self.gridLayout_3.addWidget(self.radioButtonAllData, 0, 0, 1, 1)
        self.radioButtonStatistics = QtWidgets.QRadioButton(self.groupBoxColumns)
        self.radioButtonStatistics.setObjectName("radioButtonStatistics")
        self.gridLayout_3.addWidget(self.radioButtonStatistics, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxColumns, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
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
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(outputOptions)
        self.pushButtonCancel.clicked.connect(outputOptions.reject)
        self.pushButtonAccept.clicked.connect(outputOptions.accept)
        QtCore.QMetaObject.connectSlotsByName(outputOptions)

    def retranslateUi(self, outputOptions):
        _translate = QtCore.QCoreApplication.translate
        outputOptions.setWindowTitle(_translate("outputOptions", "Output options"))
        self.groupBoxRows.setTitle(_translate("outputOptions", "Rows"))
        self.radioButtonAllChannels.setText(_translate("outputOptions", "All channels"))
        self.radioButtonChannelAverages.setText(_translate("outputOptions", "Channel averages"))
        self.groupBoxColumns.setTitle(_translate("outputOptions", "Columns"))
        self.radioButtonAllData.setText(_translate("outputOptions", "All data"))
        self.radioButtonStatistics.setText(_translate("outputOptions", "Statistics"))
        self.pushButtonCancel.setText(_translate("outputOptions", "Cancel"))
        self.pushButtonAccept.setText(_translate("outputOptions", "Accept"))

