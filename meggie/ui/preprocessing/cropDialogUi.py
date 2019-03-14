# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cropDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_cropDialog(object):
    def setupUi(self, cropDialog):
        cropDialog.setObjectName("cropDialog")
        cropDialog.resize(286, 356)
        self.formLayout = QtWidgets.QFormLayout(cropDialog)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonAddToList = QtWidgets.QPushButton(cropDialog)
        self.pushButtonAddToList.setObjectName("pushButtonAddToList")
        self.gridLayout.addWidget(self.pushButtonAddToList, 1, 0, 1, 1)
        self.groupBoxCrop = QtWidgets.QGroupBox(cropDialog)
        self.groupBoxCrop.setObjectName("groupBoxCrop")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBoxCrop)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelFrom = QtWidgets.QLabel(self.groupBoxCrop)
        self.labelFrom.setObjectName("labelFrom")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelFrom)
        self.labelTo = QtWidgets.QLabel(self.groupBoxCrop)
        self.labelTo.setObjectName("labelTo")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelTo)
        self.doubleSpinBoxFrom = QtWidgets.QDoubleSpinBox(self.groupBoxCrop)
        self.doubleSpinBoxFrom.setDecimals(3)
        self.doubleSpinBoxFrom.setMaximum(1000000.0)
        self.doubleSpinBoxFrom.setObjectName("doubleSpinBoxFrom")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxFrom)
        self.doubleSpinBoxTo = QtWidgets.QDoubleSpinBox(self.groupBoxCrop)
        self.doubleSpinBoxTo.setDecimals(3)
        self.doubleSpinBoxTo.setMaximum(1000000.0)
        self.doubleSpinBoxTo.setObjectName("doubleSpinBoxTo")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxTo)
        self.gridLayout.addWidget(self.groupBoxCrop, 0, 0, 1, 1)
        self.listWidgetKeep = QtWidgets.QListWidget(cropDialog)
        self.listWidgetKeep.setObjectName("listWidgetKeep")
        self.gridLayout.addWidget(self.listWidgetKeep, 3, 0, 1, 1)
        self.labelKeep = QtWidgets.QLabel(cropDialog)
        self.labelKeep.setObjectName("labelKeep")
        self.gridLayout.addWidget(self.labelKeep, 2, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(cropDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(cropDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(cropDialog)
        self.pushButtonCancel.clicked.connect(cropDialog.reject)
        self.pushButtonAccept.clicked.connect(cropDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(cropDialog)

    def retranslateUi(self, cropDialog):
        _translate = QtCore.QCoreApplication.translate
        cropDialog.setWindowTitle(_translate("cropDialog", "Crop"))
        self.pushButtonAddToList.setText(_translate("cropDialog", "Add to list"))
        self.groupBoxCrop.setTitle(_translate("cropDialog", "Crop settings:"))
        self.labelFrom.setText(_translate("cropDialog", "From:"))
        self.labelTo.setText(_translate("cropDialog", "To:"))
        self.doubleSpinBoxFrom.setSuffix(_translate("cropDialog", "s"))
        self.doubleSpinBoxTo.setSuffix(_translate("cropDialog", "s"))
        self.labelKeep.setText(_translate("cropDialog", "Keep following intervals:"))
        self.pushButtonCancel.setText(_translate("cropDialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("cropDialog", "Accept"))

