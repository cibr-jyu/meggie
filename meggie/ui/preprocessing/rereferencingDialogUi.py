# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rereferencingDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_rereferencingDialog(object):
    def setupUi(self, rereferencingDialog):
        rereferencingDialog.setObjectName("rereferencingDialog")
        rereferencingDialog.resize(310, 409)
        self.formLayout = QtWidgets.QFormLayout(rereferencingDialog)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxRereference = QtWidgets.QGroupBox(rereferencingDialog)
        self.groupBoxRereference.setObjectName("groupBoxRereference")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBoxRereference)
        self.formLayout_2.setObjectName("formLayout_2")
        self.labelSelectChannel = QtWidgets.QLabel(self.groupBoxRereference)
        self.labelSelectChannel.setObjectName("labelSelectChannel")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelSelectChannel)
        self.comboBoxChannel = QtWidgets.QComboBox(self.groupBoxRereference)
        self.comboBoxChannel.setMinimumSize(QtCore.QSize(120, 0))
        self.comboBoxChannel.setObjectName("comboBoxChannel")
        self.comboBoxChannel.addItem("")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxChannel)
        self.gridLayout.addWidget(self.groupBoxRereference, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(rereferencingDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(rereferencingDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(rereferencingDialog)
        self.pushButtonCancel.clicked.connect(rereferencingDialog.reject)
        self.pushButtonAccept.clicked.connect(rereferencingDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(rereferencingDialog)

    def retranslateUi(self, rereferencingDialog):
        _translate = QtCore.QCoreApplication.translate
        rereferencingDialog.setWindowTitle(_translate("rereferencingDialog", "Rereferencing"))
        self.groupBoxRereference.setTitle(_translate("rereferencingDialog", "Rereferencing options:"))
        self.labelSelectChannel.setText(_translate("rereferencingDialog", "Select channel:"))
        self.comboBoxChannel.setCurrentText(_translate("rereferencingDialog", "Use average"))
        self.comboBoxChannel.setItemText(0, _translate("rereferencingDialog", "Use average"))
        self.pushButtonCancel.setText(_translate("rereferencingDialog", "Cancel"))
        self.pushButtonAccept.setText(_translate("rereferencingDialog", "Accept"))

