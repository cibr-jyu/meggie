# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resamplingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_resamplingDialog(object):
    def setupUi(self, resamplingDialog):
        resamplingDialog.setObjectName("resamplingDialog")
        resamplingDialog.resize(249, 172)
        self.formLayout = QtWidgets.QFormLayout(resamplingDialog)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxResample = QtWidgets.QGroupBox(resamplingDialog)
        self.groupBoxResample.setObjectName("groupBoxResample")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBoxResample)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelNewRateHeading = QtWidgets.QLabel(self.groupBoxResample)
        self.labelNewRateHeading.setObjectName("labelNewRateHeading")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelNewRateHeading)
        self.doubleSpinBoxNewRate = QtWidgets.QDoubleSpinBox(self.groupBoxResample)
        self.doubleSpinBoxNewRate.setMaximum(10000.0)
        self.doubleSpinBoxNewRate.setProperty("value", 100.0)
        self.doubleSpinBoxNewRate.setObjectName("doubleSpinBoxNewRate")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxNewRate)
        self.labelCurrentRateHeading = QtWidgets.QLabel(self.groupBoxResample)
        self.labelCurrentRateHeading.setObjectName("labelCurrentRateHeading")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelCurrentRateHeading)
        self.labelCurrentRateValue = QtWidgets.QLabel(self.groupBoxResample)
        self.labelCurrentRateValue.setText("")
        self.labelCurrentRateValue.setObjectName("labelCurrentRateValue")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.labelCurrentRateValue)
        self.gridLayout.addWidget(self.groupBoxResample, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(resamplingDialog)
        self.pushButtonCancel.clicked.connect(resamplingDialog.reject)
        self.pushButtonAccept.clicked.connect(resamplingDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(resamplingDialog)

    def retranslateUi(self, resamplingDialog):
        _translate = QtCore.QCoreApplication.translate
        resamplingDialog.setWindowTitle(_translate("resamplingDialog", "Resampling"))
        self.groupBoxResample.setTitle(_translate("resamplingDialog", "Resampling options:"))
        self.labelNewRateHeading.setText(_translate("resamplingDialog", "Resample to:"))
        self.labelCurrentRateHeading.setText(_translate("resamplingDialog", "Current rate:"))
        self.pushButtonCancel.setText(_translate("resamplingDialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("resamplingDialog", "Accept"))

