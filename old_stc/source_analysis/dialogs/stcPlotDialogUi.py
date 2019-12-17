# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stcPlotDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_stcPlotDialog(object):
    def setupUi(self, stcPlotDialog):
        stcPlotDialog.setObjectName("stcPlotDialog")
        stcPlotDialog.resize(496, 337)
        self.gridLayout_7 = QtWidgets.QGridLayout(stcPlotDialog)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.buttonBox = QtWidgets.QDialogButtonBox(stcPlotDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout_7.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.groupBoxGeneral = QtWidgets.QGroupBox(stcPlotDialog)
        self.groupBoxGeneral.setEnabled(True)
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBoxGeneral)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelSource = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelSource.setObjectName("labelSource")
        self.horizontalLayout.addWidget(self.labelSource)
        self.comboBoxSource = QtWidgets.QComboBox(self.groupBoxGeneral)
        self.comboBoxSource.setObjectName("comboBoxSource")
        self.horizontalLayout.addWidget(self.comboBoxSource)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_6.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxGeneral, 0, 0, 1, 1)
        self.groupBoxTimeParameters = QtWidgets.QGroupBox(stcPlotDialog)
        self.groupBoxTimeParameters.setObjectName("groupBoxTimeParameters")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxTimeParameters)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.radioButtonPeak = QtWidgets.QRadioButton(self.groupBoxTimeParameters)
        self.radioButtonPeak.setChecked(True)
        self.radioButtonPeak.setObjectName("radioButtonPeak")
        self.horizontalLayout_3.addWidget(self.radioButtonPeak)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButtonInitialTime = QtWidgets.QRadioButton(self.groupBoxTimeParameters)
        self.radioButtonInitialTime.setChecked(False)
        self.radioButtonInitialTime.setObjectName("radioButtonInitialTime")
        self.horizontalLayout_2.addWidget(self.radioButtonInitialTime)
        self.doubleSpinBoxInitialTime = QtWidgets.QDoubleSpinBox(self.groupBoxTimeParameters)
        self.doubleSpinBoxInitialTime.setEnabled(False)
        self.doubleSpinBoxInitialTime.setObjectName("doubleSpinBoxInitialTime")
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxInitialTime)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxTimeParameters, 1, 0, 1, 1)

        self.retranslateUi(stcPlotDialog)
        self.buttonBox.accepted.connect(stcPlotDialog.accept)
        self.buttonBox.rejected.connect(stcPlotDialog.reject)
        self.radioButtonPeak.toggled['bool'].connect(self.doubleSpinBoxInitialTime.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(stcPlotDialog)

    def retranslateUi(self, stcPlotDialog):
        _translate = QtCore.QCoreApplication.translate
        stcPlotDialog.setWindowTitle(_translate("stcPlotDialog", "Meggie - Plot source estimate"))
        self.groupBoxGeneral.setTitle(_translate("stcPlotDialog", "General:"))
        self.labelSource.setText(_translate("stcPlotDialog", "Source epochs / evoked:"))
        self.groupBoxTimeParameters.setTitle(_translate("stcPlotDialog", "Time parameters:"))
        self.radioButtonPeak.setText(_translate("stcPlotDialog", "Use the peak value as initial time"))
        self.radioButtonInitialTime.setText(_translate("stcPlotDialog", "Initial time:"))
        self.doubleSpinBoxInitialTime.setSuffix(_translate("stcPlotDialog", " s"))

