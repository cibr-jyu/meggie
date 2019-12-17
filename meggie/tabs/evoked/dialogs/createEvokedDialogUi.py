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
        self.pushButtonCancel = QtWidgets.QPushButton(CreateEvokedDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(CreateEvokedDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayoutButtons.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(CreateEvokedDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayoutButtons.addWidget(self.pushButtonApply)
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
        self.labelName = QtWidgets.QLabel(self.groupBoxInfo)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelName)
        self.lineEditName = QtWidgets.QLineEdit(self.groupBoxInfo)
        self.lineEditName.setObjectName("lineEditName")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEditName)
        self.gridLayout_2.addWidget(self.groupBoxInfo, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(CreateEvokedDialog)
        self.pushButtonCancel.clicked.connect(CreateEvokedDialog.close)
        self.pushButtonApply.clicked.connect(CreateEvokedDialog.accept)
        self.pushButtonBatch.clicked.connect(CreateEvokedDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(CreateEvokedDialog)

    def retranslateUi(self, CreateEvokedDialog):
        _translate = QtCore.QCoreApplication.translate
        CreateEvokedDialog.setWindowTitle(_translate("CreateEvokedDialog", "Meggie - Create evoked"))
        self.pushButtonCancel.setText(_translate("CreateEvokedDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("CreateEvokedDialog", "Batch"))
        self.pushButtonApply.setText(_translate("CreateEvokedDialog", "Apply"))
        self.groupBoxBatching.setTitle(_translate("CreateEvokedDialog", "Batching"))
        self.groupBoxInfo.setTitle(_translate("CreateEvokedDialog", "Info"))
        self.labelName.setText(_translate("CreateEvokedDialog", "Name:"))

