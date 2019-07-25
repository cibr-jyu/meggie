# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'createEvokedDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CreateEvokedDialog(object):
    def setupUi(self, CreateEvokedDialog):
        CreateEvokedDialog.setObjectName("CreateEvokedDialog")
        CreateEvokedDialog.resize(364, 530)
        self.gridLayout = QtWidgets.QGridLayout(CreateEvokedDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutButtons.addItem(spacerItem)
        self.pushButtonComputeBatch = QtWidgets.QPushButton(CreateEvokedDialog)
        self.pushButtonComputeBatch.setObjectName("pushButtonComputeBatch")
        self.horizontalLayoutButtons.addWidget(self.pushButtonComputeBatch)
        self.pushButtonCompute = QtWidgets.QPushButton(CreateEvokedDialog)
        self.pushButtonCompute.setObjectName("pushButtonCompute")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCompute)
        self.pushButtonClose = QtWidgets.QPushButton(CreateEvokedDialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.horizontalLayoutButtons.addWidget(self.pushButtonClose)
        self.gridLayout.addLayout(self.horizontalLayoutButtons, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(CreateEvokedDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 344, 479))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setContentsMargins(9, 9, 9, 9)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxBatching, 1, 0, 1, 1)
        self.groupBoxInfo = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxInfo.setObjectName("groupBoxInfo")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxInfo)
        self.formLayout.setObjectName("formLayout")
        self.lineEditSource = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditSource.setReadOnly(True)
        self.lineEditSource.setObjectName("lineEditSource")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEditSource)
        self.lineEditName = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.lineEditName)
        self.labelSource = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelSource.setObjectName("labelSource")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelSource)
        self.labelName = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelName)
        self.gridLayout_2.addWidget(self.groupBoxInfo, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(CreateEvokedDialog)
        self.pushButtonClose.clicked.connect(CreateEvokedDialog.close)
        self.pushButtonCompute.clicked.connect(CreateEvokedDialog.accept)
        self.pushButtonComputeBatch.clicked.connect(CreateEvokedDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(CreateEvokedDialog)

    def retranslateUi(self, CreateEvokedDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateEvokedDialog.setWindowTitle(_translate("CreateEvokedDialog", "Create evoked"))
        self.pushButtonComputeBatch.setText(_translate("CreateEvokedDialog", "Batch"))
        self.pushButtonCompute.setText(_translate("CreateEvokedDialog", "Apply"))
        self.pushButtonClose.setText(_translate("CreateEvokedDialog", "Close"))
        self.groupBoxBatching.setTitle(_translate("CreateEvokedDialog", "Batching"))
        self.groupBoxInfo.setTitle(_translate("CreateEvokedDialog", "Info"))
        self.labelSource.setText(_translate("CreateEvokedDialog", "Source:"))
        self.labelName.setText(_translate("CreateEvokedDialog", "Name:"))

