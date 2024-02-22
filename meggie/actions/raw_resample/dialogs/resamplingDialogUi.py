# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resamplingDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_resamplingDialog(object):
    def setupUi(self, resamplingDialog):
        resamplingDialog.setObjectName("resamplingDialog")
        resamplingDialog.resize(406, 540)
        self.gridLayout = QtWidgets.QGridLayout(resamplingDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(resamplingDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 386, 489))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxResample = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxResample.setObjectName("groupBoxResample")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxResample)
        self.formLayout.setObjectName("formLayout")
        self.labelCurrentRateHeading = QtWidgets.QLabel(self.groupBoxResample)
        self.labelCurrentRateHeading.setObjectName("labelCurrentRateHeading")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelCurrentRateHeading
        )
        self.labelCurrentRateValue = QtWidgets.QLabel(self.groupBoxResample)
        self.labelCurrentRateValue.setText("")
        self.labelCurrentRateValue.setObjectName("labelCurrentRateValue")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.labelCurrentRateValue
        )
        self.labelNewRateHeading = QtWidgets.QLabel(self.groupBoxResample)
        self.labelNewRateHeading.setObjectName("labelNewRateHeading")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.labelNewRateHeading
        )
        self.doubleSpinBoxNewRate = QtWidgets.QDoubleSpinBox(self.groupBoxResample)
        self.doubleSpinBoxNewRate.setMaximum(10000.0)
        self.doubleSpinBoxNewRate.setProperty("value", 100.0)
        self.doubleSpinBoxNewRate.setObjectName("doubleSpinBoxNewRate")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxNewRate
        )
        self.gridLayout_2.addWidget(self.groupBoxResample, 0, 0, 1, 1)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxBatching, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayout.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(resamplingDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(resamplingDialog)
        self.pushButtonCancel.clicked.connect(resamplingDialog.reject)
        self.pushButtonApply.clicked.connect(resamplingDialog.accept)
        self.pushButtonBatch.clicked.connect(resamplingDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(resamplingDialog)

    def retranslateUi(self, resamplingDialog):
        _translate = QtCore.QCoreApplication.translate
        resamplingDialog.setWindowTitle(
            _translate("resamplingDialog", "Meggie - Resampling")
        )
        self.groupBoxResample.setTitle(
            _translate("resamplingDialog", "Resampling options:")
        )
        self.labelCurrentRateHeading.setText(
            _translate("resamplingDialog", "Current rate:")
        )
        self.labelNewRateHeading.setText(_translate("resamplingDialog", "Resample to:"))
        self.groupBoxBatching.setTitle(_translate("resamplingDialog", "Batching"))
        self.pushButtonCancel.setText(_translate("resamplingDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("resamplingDialog", "Batch"))
        self.pushButtonApply.setText(_translate("resamplingDialog", "Apply"))
