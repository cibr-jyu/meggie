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
        resamplingDialog.resize(319, 464)
        self.verticalLayout = QtWidgets.QVBoxLayout(resamplingDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(resamplingDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 300, 600))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(300, 600))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.formLayout_2 = QtWidgets.QFormLayout(self.scrollAreaWidgetContents)
        self.formLayout_2.setObjectName("formLayout_2")
        self.groupBoxResample = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxResample.setObjectName("groupBoxResample")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxResample)
        self.formLayout.setObjectName("formLayout")
        self.labelCurrentRateHeading = QtWidgets.QLabel(self.groupBoxResample)
        self.labelCurrentRateHeading.setObjectName("labelCurrentRateHeading")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelCurrentRateHeading)
        self.labelCurrentRateValue = QtWidgets.QLabel(self.groupBoxResample)
        self.labelCurrentRateValue.setText("")
        self.labelCurrentRateValue.setObjectName("labelCurrentRateValue")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.labelCurrentRateValue)
        self.labelNewRateHeading = QtWidgets.QLabel(self.groupBoxResample)
        self.labelNewRateHeading.setObjectName("labelNewRateHeading")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelNewRateHeading)
        self.doubleSpinBoxNewRate = QtWidgets.QDoubleSpinBox(self.groupBoxResample)
        self.doubleSpinBoxNewRate.setMaximum(10000.0)
        self.doubleSpinBoxNewRate.setProperty("value", 100.0)
        self.doubleSpinBoxNewRate.setObjectName("doubleSpinBoxNewRate")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxNewRate)
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.groupBoxResample)
        self.widgetBatchContainer = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.widgetBatchContainer.setMinimumSize(QtCore.QSize(0, 0))
        self.widgetBatchContainer.setObjectName("widgetBatchContainer")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.widgetBatchContainer)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonComputeBatch = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonComputeBatch.setObjectName("pushButtonComputeBatch")
        self.horizontalLayout.addWidget(self.pushButtonComputeBatch)
        self.pushButtonCompute = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonCompute.setObjectName("pushButtonCompute")
        self.horizontalLayout.addWidget(self.pushButtonCompute)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(resamplingDialog)
        self.pushButtonCancel.clicked.connect(resamplingDialog.reject)
        self.pushButtonCompute.clicked.connect(resamplingDialog.accept)
        self.pushButtonComputeBatch.clicked.connect(resamplingDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(resamplingDialog)

    def retranslateUi(self, resamplingDialog):
        _translate = QtCore.QCoreApplication.translate
        resamplingDialog.setWindowTitle(_translate("resamplingDialog", "Resampling"))
        self.groupBoxResample.setTitle(_translate("resamplingDialog", "Resampling options:"))
        self.labelCurrentRateHeading.setText(_translate("resamplingDialog", "Current rate:"))
        self.labelNewRateHeading.setText(_translate("resamplingDialog", "Resample to:"))
        self.pushButtonCancel.setText(_translate("resamplingDialog", "Cancel"))
        self.pushButtonComputeBatch.setText(_translate("resamplingDialog", "Batch"))
        self.pushButtonCompute.setText(_translate("resamplingDialog", "Accept"))

