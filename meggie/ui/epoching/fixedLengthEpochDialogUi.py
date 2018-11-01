# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../fixedLengthEpochsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FixedLengthEpochDialog(object):
    def setupUi(self, FixedLengthEpochDialog):
        FixedLengthEpochDialog.setObjectName("FixedLengthEpochDialog")
        FixedLengthEpochDialog.resize(247, 165)
        self.gridLayout = QtWidgets.QGridLayout(FixedLengthEpochDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.labelStart = QtWidgets.QLabel(FixedLengthEpochDialog)
        self.labelStart.setObjectName("labelStart")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelStart)
        self.spinBoxStart = QtWidgets.QSpinBox(FixedLengthEpochDialog)
        self.spinBoxStart.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxStart.setObjectName("spinBoxStart")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxStart)
        self.labelEnd = QtWidgets.QLabel(FixedLengthEpochDialog)
        self.labelEnd.setObjectName("labelEnd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelEnd)
        self.spinBoxEnd = QtWidgets.QSpinBox(FixedLengthEpochDialog)
        self.spinBoxEnd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxEnd.setObjectName("spinBoxEnd")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxEnd)
        self.labelInterval = QtWidgets.QLabel(FixedLengthEpochDialog)
        self.labelInterval.setObjectName("labelInterval")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelInterval)
        self.doubleSpinBoxInterval = QtWidgets.QDoubleSpinBox(FixedLengthEpochDialog)
        self.doubleSpinBoxInterval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxInterval.setDecimals(3)
        self.doubleSpinBoxInterval.setProperty("value", 0.5)
        self.doubleSpinBoxInterval.setObjectName("doubleSpinBoxInterval")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxInterval)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(FixedLengthEpochDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(FixedLengthEpochDialog)
        self.buttonBox.accepted.connect(FixedLengthEpochDialog.accept)
        self.buttonBox.rejected.connect(FixedLengthEpochDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FixedLengthEpochDialog)
        FixedLengthEpochDialog.setTabOrder(self.spinBoxStart, self.spinBoxEnd)
        FixedLengthEpochDialog.setTabOrder(self.spinBoxEnd, self.doubleSpinBoxInterval)
        FixedLengthEpochDialog.setTabOrder(self.doubleSpinBoxInterval, self.buttonBox)

    def retranslateUi(self, FixedLengthEpochDialog):
        _translate = QtCore.QCoreApplication.translate
        FixedLengthEpochDialog.setWindowTitle(_translate("FixedLengthEpochDialog", "Construct fixed length events"))
        self.labelStart.setText(_translate("FixedLengthEpochDialog", "Start"))
        self.spinBoxStart.setSuffix(_translate("FixedLengthEpochDialog", "s"))
        self.labelEnd.setText(_translate("FixedLengthEpochDialog", "End"))
        self.spinBoxEnd.setSuffix(_translate("FixedLengthEpochDialog", "s"))
        self.labelInterval.setText(_translate("FixedLengthEpochDialog", "Interval"))
        self.doubleSpinBoxInterval.setSuffix(_translate("FixedLengthEpochDialog", "s"))

