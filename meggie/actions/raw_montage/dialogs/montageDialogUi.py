# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'montageDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_montageDialog(object):
    def setupUi(self, montageDialog):
        montageDialog.setObjectName("montageDialog")
        montageDialog.resize(403, 557)
        self.gridLayout = QtWidgets.QGridLayout(montageDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(montageDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 369, 517))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem, 3, 1, 1, 1)
        self.groupBoxMontage = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxMontage.setObjectName("groupBoxMontage")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBoxMontage)
        self.formLayout_2.setObjectName("formLayout_2")
        self.radioButtonMontageFromList = QtWidgets.QRadioButton(self.groupBoxMontage)
        self.radioButtonMontageFromList.setObjectName("radioButtonMontageFromList")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.radioButtonMontageFromList
        )
        self.comboBoxSelectFromList = QtWidgets.QComboBox(self.groupBoxMontage)
        self.comboBoxSelectFromList.setObjectName("comboBoxSelectFromList")
        self.formLayout_2.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.comboBoxSelectFromList
        )
        self.radioButtonMontageFromFile = QtWidgets.QRadioButton(self.groupBoxMontage)
        self.radioButtonMontageFromFile.setObjectName("radioButtonMontageFromFile")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.radioButtonMontageFromFile
        )
        self.pushButtonSelectFromFile = QtWidgets.QPushButton(self.groupBoxMontage)
        self.pushButtonSelectFromFile.setObjectName("pushButtonSelectFromFile")
        self.formLayout_2.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.pushButtonSelectFromFile
        )
        self.labelCurrentLabel = QtWidgets.QLabel(self.groupBoxMontage)
        self.labelCurrentLabel.setObjectName("labelCurrentLabel")
        self.formLayout_2.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelCurrentLabel
        )
        self.labelCurrentContent = QtWidgets.QLabel(self.groupBoxMontage)
        self.labelCurrentContent.setText("")
        self.labelCurrentContent.setObjectName("labelCurrentContent")
        self.formLayout_2.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.labelCurrentContent
        )
        self.labelHeadSize = QtWidgets.QLabel(self.groupBoxMontage)
        self.labelHeadSize.setObjectName("labelHeadSize")
        self.formLayout_2.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.labelHeadSize
        )
        self.doubleSpinBoxHeadSize = QtWidgets.QDoubleSpinBox(self.groupBoxMontage)
        self.doubleSpinBoxHeadSize.setDecimals(4)
        self.doubleSpinBoxHeadSize.setMaximum(1.0)
        self.doubleSpinBoxHeadSize.setSingleStep(0.001)
        self.doubleSpinBoxHeadSize.setProperty("value", 0.095)
        self.doubleSpinBoxHeadSize.setObjectName("doubleSpinBoxHeadSize")
        self.formLayout_2.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxHeadSize
        )
        self.gridLayout_2.addWidget(self.groupBoxMontage, 0, 0, 2, 2)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxBatching, 2, 0, 1, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(montageDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(montageDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayout.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(montageDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(montageDialog)
        self.pushButtonCancel.clicked.connect(montageDialog.reject)
        self.pushButtonApply.clicked.connect(montageDialog.accept)
        self.pushButtonBatch.clicked.connect(montageDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(montageDialog)
        montageDialog.setTabOrder(self.pushButtonCancel, self.pushButtonBatch)
        montageDialog.setTabOrder(self.pushButtonBatch, self.pushButtonApply)
        montageDialog.setTabOrder(self.pushButtonApply, self.scrollArea)
        montageDialog.setTabOrder(self.scrollArea, self.radioButtonMontageFromList)
        montageDialog.setTabOrder(
            self.radioButtonMontageFromList, self.comboBoxSelectFromList
        )
        montageDialog.setTabOrder(
            self.comboBoxSelectFromList, self.radioButtonMontageFromFile
        )
        montageDialog.setTabOrder(
            self.radioButtonMontageFromFile, self.pushButtonSelectFromFile
        )

    def retranslateUi(self, montageDialog):
        _translate = QtCore.QCoreApplication.translate
        montageDialog.setWindowTitle(
            _translate("montageDialog", "Meggie - Set standard montage")
        )
        self.groupBoxMontage.setTitle(
            _translate("montageDialog", "Select EEG montage:")
        )
        self.radioButtonMontageFromList.setText(
            _translate("montageDialog", "Select from list:")
        )
        self.radioButtonMontageFromFile.setText(
            _translate("montageDialog", "Select from file:")
        )
        self.pushButtonSelectFromFile.setText(_translate("montageDialog", "Browse..."))
        self.labelCurrentLabel.setText(
            _translate("montageDialog", "Current selection:")
        )
        self.labelHeadSize.setText(_translate("montageDialog", "Head size:"))
        self.doubleSpinBoxHeadSize.setSuffix(_translate("montageDialog", "m"))
        self.groupBoxBatching.setTitle(_translate("montageDialog", "Batching"))
        self.pushButtonCancel.setText(_translate("montageDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("montageDialog", "Batch"))
        self.pushButtonApply.setText(_translate("montageDialog", "Apply"))
