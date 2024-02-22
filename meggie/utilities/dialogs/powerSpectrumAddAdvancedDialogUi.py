# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerSpectrumAddAdvancedDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PowerSpectrumAddAdvancedDialog(object):
    def setupUi(self, PowerSpectrumAddAdvancedDialog):
        PowerSpectrumAddAdvancedDialog.setObjectName("PowerSpectrumAddAdvancedDialog")
        PowerSpectrumAddAdvancedDialog.resize(356, 546)
        self.gridLayout_2 = QtWidgets.QGridLayout(PowerSpectrumAddAdvancedDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxGeneral = QtWidgets.QGroupBox(PowerSpectrumAddAdvancedDialog)
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxGeneral)
        self.formLayout.setObjectName("formLayout")
        self.labelGroup = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelGroup.setObjectName("labelGroup")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelGroup)
        self.comboBoxAvgGroup = QtWidgets.QComboBox(self.groupBoxGeneral)
        self.comboBoxAvgGroup.setObjectName("comboBoxAvgGroup")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.comboBoxAvgGroup
        )
        self.gridLayout_2.addWidget(self.groupBoxGeneral, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(PowerSpectrumAddAdvancedDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtWidgets.QPushButton(PowerSpectrumAddAdvancedDialog)
        self.pushButtonAccept.setObjectName("pushButtonAccept")
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 0, 1, 1)
        self.groupBoxStartingPoints = QtWidgets.QGroupBox(
            PowerSpectrumAddAdvancedDialog
        )
        self.groupBoxStartingPoints.setObjectName("groupBoxStartingPoints")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxStartingPoints)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelStartId = QtWidgets.QLabel(self.groupBoxStartingPoints)
        self.labelStartId.setObjectName("labelStartId")
        self.gridLayout_3.addWidget(self.labelStartId, 1, 0, 1, 1)
        self.labelStartOffset = QtWidgets.QLabel(self.groupBoxStartingPoints)
        self.labelStartOffset.setObjectName("labelStartOffset")
        self.gridLayout_3.addWidget(self.labelStartOffset, 5, 0, 1, 1)
        self.labelStartMask = QtWidgets.QLabel(self.groupBoxStartingPoints)
        self.labelStartMask.setObjectName("labelStartMask")
        self.gridLayout_3.addWidget(self.labelStartMask, 2, 0, 1, 1)
        self.pushButtonStartEdit = QtWidgets.QPushButton(self.groupBoxStartingPoints)
        self.pushButtonStartEdit.setEnabled(False)
        self.pushButtonStartEdit.setObjectName("pushButtonStartEdit")
        self.gridLayout_3.addWidget(self.pushButtonStartEdit, 1, 3, 1, 1)
        self.radioButtonStartUseEvents = QtWidgets.QRadioButton(
            self.groupBoxStartingPoints
        )
        self.radioButtonStartUseEvents.setObjectName("radioButtonStartUseEvents")
        self.gridLayout_3.addWidget(self.radioButtonStartUseEvents, 0, 0, 1, 4)
        self.radioButtonStartUseStart = QtWidgets.QRadioButton(
            self.groupBoxStartingPoints
        )
        self.radioButtonStartUseStart.setChecked(True)
        self.radioButtonStartUseStart.setObjectName("radioButtonStartUseStart")
        self.gridLayout_3.addWidget(self.radioButtonStartUseStart, 3, 0, 1, 4)
        self.doubleSpinBoxStartOffset = QtWidgets.QDoubleSpinBox(
            self.groupBoxStartingPoints
        )
        self.doubleSpinBoxStartOffset.setMinimum(-100000000.0)
        self.doubleSpinBoxStartOffset.setMaximum(100000000.0)
        self.doubleSpinBoxStartOffset.setProperty("value", 5.0)
        self.doubleSpinBoxStartOffset.setObjectName("doubleSpinBoxStartOffset")
        self.gridLayout_3.addWidget(self.doubleSpinBoxStartOffset, 5, 2, 1, 1)
        self.spinBoxStartId = QtWidgets.QSpinBox(self.groupBoxStartingPoints)
        self.spinBoxStartId.setEnabled(False)
        self.spinBoxStartId.setMaximum(10000000)
        self.spinBoxStartId.setProperty("value", 1)
        self.spinBoxStartId.setObjectName("spinBoxStartId")
        self.gridLayout_3.addWidget(self.spinBoxStartId, 1, 2, 1, 1)
        self.spinBoxStartMask = QtWidgets.QSpinBox(self.groupBoxStartingPoints)
        self.spinBoxStartMask.setEnabled(False)
        self.spinBoxStartMask.setMaximum(1000000000)
        self.spinBoxStartMask.setObjectName("spinBoxStartMask")
        self.gridLayout_3.addWidget(self.spinBoxStartMask, 2, 2, 1, 1)
        self.radioButtonStartUseEnd = QtWidgets.QRadioButton(
            self.groupBoxStartingPoints
        )
        self.radioButtonStartUseEnd.setObjectName("radioButtonStartUseEnd")
        self.gridLayout_3.addWidget(self.radioButtonStartUseEnd, 4, 0, 1, 4)
        self.gridLayout_2.addWidget(self.groupBoxStartingPoints, 1, 0, 1, 1)
        self.groupBoxEndingPoints = QtWidgets.QGroupBox(PowerSpectrumAddAdvancedDialog)
        self.groupBoxEndingPoints.setObjectName("groupBoxEndingPoints")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxEndingPoints)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.doubleSpinBoxEndOffset = QtWidgets.QDoubleSpinBox(
            self.groupBoxEndingPoints
        )
        self.doubleSpinBoxEndOffset.setMinimum(-10000000.0)
        self.doubleSpinBoxEndOffset.setMaximum(10000000.99)
        self.doubleSpinBoxEndOffset.setProperty("value", -5.0)
        self.doubleSpinBoxEndOffset.setObjectName("doubleSpinBoxEndOffset")
        self.gridLayout_4.addWidget(self.doubleSpinBoxEndOffset, 6, 2, 1, 1)
        self.labelEndMask = QtWidgets.QLabel(self.groupBoxEndingPoints)
        self.labelEndMask.setObjectName("labelEndMask")
        self.gridLayout_4.addWidget(self.labelEndMask, 2, 0, 1, 1)
        self.labelEndId = QtWidgets.QLabel(self.groupBoxEndingPoints)
        self.labelEndId.setObjectName("labelEndId")
        self.gridLayout_4.addWidget(self.labelEndId, 1, 0, 1, 1)
        self.labelEndOffset = QtWidgets.QLabel(self.groupBoxEndingPoints)
        self.labelEndOffset.setObjectName("labelEndOffset")
        self.gridLayout_4.addWidget(self.labelEndOffset, 6, 0, 1, 1)
        self.pushButtonEndEdit = QtWidgets.QPushButton(self.groupBoxEndingPoints)
        self.pushButtonEndEdit.setEnabled(False)
        self.pushButtonEndEdit.setObjectName("pushButtonEndEdit")
        self.gridLayout_4.addWidget(self.pushButtonEndEdit, 1, 3, 1, 1)
        self.radioButtonEndUseEvents = QtWidgets.QRadioButton(self.groupBoxEndingPoints)
        self.radioButtonEndUseEvents.setObjectName("radioButtonEndUseEvents")
        self.gridLayout_4.addWidget(self.radioButtonEndUseEvents, 0, 0, 1, 4)
        self.radioButtonEndUseEnd = QtWidgets.QRadioButton(self.groupBoxEndingPoints)
        self.radioButtonEndUseEnd.setChecked(True)
        self.radioButtonEndUseEnd.setObjectName("radioButtonEndUseEnd")
        self.gridLayout_4.addWidget(self.radioButtonEndUseEnd, 4, 0, 1, 4)
        self.spinBoxEndId = QtWidgets.QSpinBox(self.groupBoxEndingPoints)
        self.spinBoxEndId.setEnabled(False)
        self.spinBoxEndId.setMaximum(10000000)
        self.spinBoxEndId.setProperty("value", 2)
        self.spinBoxEndId.setObjectName("spinBoxEndId")
        self.gridLayout_4.addWidget(self.spinBoxEndId, 1, 2, 1, 1)
        self.spinBoxEndMask = QtWidgets.QSpinBox(self.groupBoxEndingPoints)
        self.spinBoxEndMask.setEnabled(False)
        self.spinBoxEndMask.setMaximum(1000000000)
        self.spinBoxEndMask.setObjectName("spinBoxEndMask")
        self.gridLayout_4.addWidget(self.spinBoxEndMask, 2, 2, 1, 1)
        self.radioButtonEndUseStart = QtWidgets.QRadioButton(self.groupBoxEndingPoints)
        self.radioButtonEndUseStart.setObjectName("radioButtonEndUseStart")
        self.gridLayout_4.addWidget(self.radioButtonEndUseStart, 3, 0, 1, 4)
        self.gridLayout_2.addWidget(self.groupBoxEndingPoints, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)

        self.retranslateUi(PowerSpectrumAddAdvancedDialog)
        self.pushButtonCancel.clicked.connect(PowerSpectrumAddAdvancedDialog.reject)
        self.pushButtonAccept.clicked.connect(PowerSpectrumAddAdvancedDialog.accept)
        self.radioButtonEndUseEvents.toggled["bool"].connect(
            self.spinBoxEndId.setEnabled
        )
        self.radioButtonEndUseEvents.toggled["bool"].connect(
            self.spinBoxEndMask.setEnabled
        )
        self.radioButtonEndUseEvents.toggled["bool"].connect(
            self.pushButtonEndEdit.setEnabled
        )
        self.radioButtonStartUseEvents.toggled["bool"].connect(
            self.spinBoxStartId.setEnabled
        )
        self.radioButtonStartUseEvents.toggled["bool"].connect(
            self.spinBoxStartMask.setEnabled
        )
        self.radioButtonStartUseEvents.toggled["bool"].connect(
            self.pushButtonStartEdit.setEnabled
        )
        QtCore.QMetaObject.connectSlotsByName(PowerSpectrumAddAdvancedDialog)

    def retranslateUi(self, PowerSpectrumAddAdvancedDialog):
        _translate = QtCore.QCoreApplication.translate
        PowerSpectrumAddAdvancedDialog.setWindowTitle(
            _translate("PowerSpectrumAddAdvancedDialog", "Meggie - Add advanced")
        )
        self.groupBoxGeneral.setTitle(
            _translate("PowerSpectrumAddAdvancedDialog", "General:")
        )
        self.labelGroup.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Average group:")
        )
        self.comboBoxAvgGroup.setItemText(
            0, _translate("PowerSpectrumAddAdvancedDialog", "1")
        )
        self.comboBoxAvgGroup.setItemText(
            1, _translate("PowerSpectrumAddAdvancedDialog", "2")
        )
        self.comboBoxAvgGroup.setItemText(
            2, _translate("PowerSpectrumAddAdvancedDialog", "3")
        )
        self.comboBoxAvgGroup.setItemText(
            3, _translate("PowerSpectrumAddAdvancedDialog", "4")
        )
        self.comboBoxAvgGroup.setItemText(
            4, _translate("PowerSpectrumAddAdvancedDialog", "5")
        )
        self.comboBoxAvgGroup.setItemText(
            5, _translate("PowerSpectrumAddAdvancedDialog", "6")
        )
        self.comboBoxAvgGroup.setItemText(
            6, _translate("PowerSpectrumAddAdvancedDialog", "7")
        )
        self.comboBoxAvgGroup.setItemText(
            7, _translate("PowerSpectrumAddAdvancedDialog", "8")
        )
        self.pushButtonCancel.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Cancel")
        )
        self.pushButtonAccept.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Add")
        )
        self.groupBoxStartingPoints.setTitle(
            _translate("PowerSpectrumAddAdvancedDialog", "Starting points:")
        )
        self.labelStartId.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Event id:")
        )
        self.labelStartOffset.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Offset:")
        )
        self.labelStartMask.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Mask:")
        )
        self.pushButtonStartEdit.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Edit...")
        )
        self.radioButtonStartUseEvents.setText(
            _translate(
                "PowerSpectrumAddAdvancedDialog", "Get starting points from events:"
            )
        )
        self.radioButtonStartUseStart.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Use start of recording")
        )
        self.doubleSpinBoxStartOffset.setSuffix(
            _translate("PowerSpectrumAddAdvancedDialog", "s")
        )
        self.radioButtonStartUseEnd.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Use end of recording")
        )
        self.groupBoxEndingPoints.setTitle(
            _translate("PowerSpectrumAddAdvancedDialog", "Ending points:")
        )
        self.doubleSpinBoxEndOffset.setSuffix(
            _translate("PowerSpectrumAddAdvancedDialog", "s")
        )
        self.labelEndMask.setText(_translate("PowerSpectrumAddAdvancedDialog", "Mask:"))
        self.labelEndId.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Event id:")
        )
        self.labelEndOffset.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Offset:")
        )
        self.pushButtonEndEdit.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Edit...")
        )
        self.radioButtonEndUseEvents.setText(
            _translate(
                "PowerSpectrumAddAdvancedDialog", "Get starting points from events:"
            )
        )
        self.radioButtonEndUseEnd.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Use end of recording")
        )
        self.radioButtonEndUseStart.setText(
            _translate("PowerSpectrumAddAdvancedDialog", "Use start of recording")
        )
