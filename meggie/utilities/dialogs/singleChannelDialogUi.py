# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_ui_files/singleChannelDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_singleChannelDialog(object):
    def setupUi(self, singleChannelDialog):
        singleChannelDialog.setObjectName("singleChannelDialog")
        singleChannelDialog.resize(419, 523)
        self.gridLayout = QtWidgets.QGridLayout(singleChannelDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(singleChannelDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 399, 472))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem, 4, 0, 1, 1)
        self.groupBoxLegend = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxLegend.setObjectName("groupBoxLegend")
        self.formLayoutLegend = QtWidgets.QFormLayout(self.groupBoxLegend)
        self.formLayoutLegend.setObjectName("formLayoutLegend")
        self.gridLayout_2.addWidget(self.groupBoxLegend, 3, 0, 1, 1)
        self.groupBoxValueRange = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxValueRange.setObjectName("groupBoxValueRange")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBoxValueRange)
        self.formLayout_3.setObjectName("formLayout_3")
        self.labelMax = QtWidgets.QLabel(self.groupBoxValueRange)
        self.labelMax.setObjectName("labelMax")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelMax)
        self.doubleSpinBoxMax = QtWidgets.QDoubleSpinBox(self.groupBoxValueRange)
        self.doubleSpinBoxMax.setSuffix("")
        self.doubleSpinBoxMax.setDecimals(4)
        self.doubleSpinBoxMax.setMinimum(-100000000000.0)
        self.doubleSpinBoxMax.setMaximum(100000000000.0)
        self.doubleSpinBoxMax.setSingleStep(0.01)
        self.doubleSpinBoxMax.setProperty("value", 0.0)
        self.doubleSpinBoxMax.setObjectName("doubleSpinBoxMax")
        self.formLayout_3.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxMax
        )
        self.labelMin = QtWidgets.QLabel(self.groupBoxValueRange)
        self.labelMin.setObjectName("labelMin")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelMin)
        self.doubleSpinBoxMin = QtWidgets.QDoubleSpinBox(self.groupBoxValueRange)
        self.doubleSpinBoxMin.setSuffix("")
        self.doubleSpinBoxMin.setDecimals(4)
        self.doubleSpinBoxMin.setMinimum(-100000000000.0)
        self.doubleSpinBoxMin.setMaximum(100000000000.0)
        self.doubleSpinBoxMin.setSingleStep(0.01)
        self.doubleSpinBoxMin.setProperty("value", 0.0)
        self.doubleSpinBoxMin.setObjectName("doubleSpinBoxMin")
        self.formLayout_3.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxMin
        )
        self.gridLayout_2.addWidget(self.groupBoxValueRange, 2, 0, 1, 1)
        self.groupBoxGeneral = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.formLayout_4 = QtWidgets.QFormLayout(self.groupBoxGeneral)
        self.formLayout_4.setObjectName("formLayout_4")
        self.labelChannel = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelChannel.setObjectName("labelChannel")
        self.formLayout_4.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelChannel
        )
        self.comboBoxChannel = QtWidgets.QComboBox(self.groupBoxGeneral)
        self.comboBoxChannel.setObjectName("comboBoxChannel")
        self.formLayout_4.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.comboBoxChannel
        )
        self.labelTitle = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelTitle.setObjectName("labelTitle")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelTitle)
        self.lineEditTitle = QtWidgets.QLineEdit(self.groupBoxGeneral)
        self.lineEditTitle.setObjectName("lineEditTitle")
        self.formLayout_4.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.lineEditTitle
        )
        self.gridLayout_2.addWidget(self.groupBoxGeneral, 0, 0, 1, 1)
        self.groupBoxSmoothing = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxSmoothing.setObjectName("groupBoxSmoothing")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxSmoothing)
        self.formLayout.setObjectName("formLayout")
        self.labelWindowLength = QtWidgets.QLabel(self.groupBoxSmoothing)
        self.labelWindowLength.setObjectName("labelWindowLength")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelWindowLength
        )
        self.spinBoxWindowLength = QtWidgets.QSpinBox(self.groupBoxSmoothing)
        self.spinBoxWindowLength.setMaximum(10000000)
        self.spinBoxWindowLength.setProperty("value", 11)
        self.spinBoxWindowLength.setObjectName("spinBoxWindowLength")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.spinBoxWindowLength
        )
        self.labelWindow = QtWidgets.QLabel(self.groupBoxSmoothing)
        self.labelWindow.setObjectName("labelWindow")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelWindow)
        self.comboBoxWindow = QtWidgets.QComboBox(self.groupBoxSmoothing)
        self.comboBoxWindow.setObjectName("comboBoxWindow")
        self.comboBoxWindow.addItem("")
        self.comboBoxWindow.setItemText(0, "")
        self.comboBoxWindow.addItem("")
        self.comboBoxWindow.addItem("")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.comboBoxWindow
        )
        self.gridLayout_2.addWidget(self.groupBoxSmoothing, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(singleChannelDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(singleChannelDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(singleChannelDialog)
        self.pushButtonCancel.clicked.connect(singleChannelDialog.reject)
        self.pushButtonApply.clicked.connect(singleChannelDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(singleChannelDialog)

    def retranslateUi(self, singleChannelDialog):
        _translate = QtCore.QCoreApplication.translate
        singleChannelDialog.setWindowTitle(
            _translate("singleChannelDialog", "Meggie - Single channel")
        )
        self.groupBoxLegend.setTitle(_translate("singleChannelDialog", "Legend:"))
        self.groupBoxValueRange.setTitle(
            _translate("singleChannelDialog", "Value range:")
        )
        self.labelMax.setText(_translate("singleChannelDialog", "Max value:"))
        self.labelMin.setText(_translate("singleChannelDialog", "Min value:"))
        self.groupBoxGeneral.setTitle(_translate("singleChannelDialog", "General:"))
        self.labelChannel.setText(_translate("singleChannelDialog", "Channel:"))
        self.labelTitle.setText(_translate("singleChannelDialog", "Title:"))
        self.groupBoxSmoothing.setTitle(
            _translate("singleChannelDialog", "Smoothing settings:")
        )
        self.labelWindowLength.setText(
            _translate("singleChannelDialog", "Window length:")
        )
        self.labelWindow.setText(_translate("singleChannelDialog", "Window:"))
        self.comboBoxWindow.setItemText(1, _translate("singleChannelDialog", "hanning"))
        self.comboBoxWindow.setItemText(2, _translate("singleChannelDialog", "flat"))
        self.pushButtonCancel.setText(_translate("singleChannelDialog", "Cancel"))
        self.pushButtonApply.setText(_translate("singleChannelDialog", "Apply"))
