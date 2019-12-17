# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'rereferencingDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_rereferencingDialog(object):
    def setupUi(self, rereferencingDialog):
        rereferencingDialog.setObjectName("rereferencingDialog")
        rereferencingDialog.resize(423, 498)
        self.gridLayout_2 = QtWidgets.QGridLayout(rereferencingDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(rereferencingDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(rereferencingDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayout.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(rereferencingDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(rereferencingDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 403, 447))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxRereference = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
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
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxBatching, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(rereferencingDialog)
        self.pushButtonCancel.clicked.connect(rereferencingDialog.reject)
        self.pushButtonApply.clicked.connect(rereferencingDialog.accept)
        self.pushButtonBatch.clicked.connect(rereferencingDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(rereferencingDialog)

    def retranslateUi(self, rereferencingDialog):
        _translate = QtCore.QCoreApplication.translate
        rereferencingDialog.setWindowTitle(_translate("rereferencingDialog", "Meggie - Rereferencing"))
        self.pushButtonCancel.setText(_translate("rereferencingDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("rereferencingDialog", "Batch"))
        self.pushButtonApply.setText(_translate("rereferencingDialog", "Apply"))
        self.groupBoxRereference.setTitle(_translate("rereferencingDialog", "Rereferencing options"))
        self.labelSelectChannel.setText(_translate("rereferencingDialog", "Select channel:"))
        self.comboBoxChannel.setCurrentText(_translate("rereferencingDialog", "Use average"))
        self.comboBoxChannel.setItemText(0, _translate("rereferencingDialog", "Use average"))
        self.groupBoxBatching.setTitle(_translate("rereferencingDialog", "Batching"))

