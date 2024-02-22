# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TFROutputOptionsUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_TFROutputOptions(object):
    def setupUi(self, TFROutputOptions):
        TFROutputOptions.setObjectName("TFROutputOptions")
        TFROutputOptions.resize(546, 577)
        self.gridLayout_2 = QtWidgets.QGridLayout(TFROutputOptions)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(TFROutputOptions)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 514, 541))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.doubleSpinBoxTimeStart = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxTimeStart.setSingleStep(0.1)
        self.doubleSpinBoxTimeStart.setObjectName("doubleSpinBoxTimeStart")
        self.gridLayout_3.addWidget(self.doubleSpinBoxTimeStart, 0, 1, 1, 1)
        self.labelTimeStart = QtWidgets.QLabel(self.groupBox)
        self.labelTimeStart.setObjectName("labelTimeStart")
        self.gridLayout_3.addWidget(self.labelTimeStart, 0, 0, 1, 1)
        self.labelTimeEnd = QtWidgets.QLabel(self.groupBox)
        self.labelTimeEnd.setObjectName("labelTimeEnd")
        self.gridLayout_3.addWidget(self.labelTimeEnd, 1, 0, 1, 1)
        self.doubleSpinBoxTimeEnd = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBoxTimeEnd.setMinimum(0.0)
        self.doubleSpinBoxTimeEnd.setSingleStep(0.1)
        self.doubleSpinBoxTimeEnd.setProperty("value", 0.0)
        self.doubleSpinBoxTimeEnd.setObjectName("doubleSpinBoxTimeEnd")
        self.gridLayout_3.addWidget(self.doubleSpinBoxTimeEnd, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 4, 0, 1, 1)
        self.groupBoxBaseline = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBaseline.setObjectName("groupBoxBaseline")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBoxBaseline)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.labelBaselineCorrection = QtWidgets.QLabel(self.groupBoxBaseline)
        self.labelBaselineCorrection.setObjectName("labelBaselineCorrection")
        self.gridLayout_9.addWidget(self.labelBaselineCorrection, 0, 0, 1, 1)
        self.doubleSpinBoxBaselineStart = QtWidgets.QDoubleSpinBox(
            self.groupBoxBaseline
        )
        self.doubleSpinBoxBaselineStart.setSingleStep(0.1)
        self.doubleSpinBoxBaselineStart.setObjectName("doubleSpinBoxBaselineStart")
        self.gridLayout_9.addWidget(self.doubleSpinBoxBaselineStart, 2, 1, 1, 1)
        self.doubleSpinBoxBaselineEnd = QtWidgets.QDoubleSpinBox(self.groupBoxBaseline)
        self.doubleSpinBoxBaselineEnd.setSingleStep(0.1)
        self.doubleSpinBoxBaselineEnd.setObjectName("doubleSpinBoxBaselineEnd")
        self.gridLayout_9.addWidget(self.doubleSpinBoxBaselineEnd, 3, 1, 1, 1)
        self.comboBoxBaselineMode = QtWidgets.QComboBox(self.groupBoxBaseline)
        self.comboBoxBaselineMode.setObjectName("comboBoxBaselineMode")
        self.comboBoxBaselineMode.addItem("")
        self.comboBoxBaselineMode.addItem("")
        self.comboBoxBaselineMode.addItem("")
        self.comboBoxBaselineMode.addItem("")
        self.comboBoxBaselineMode.addItem("")
        self.gridLayout_9.addWidget(self.comboBoxBaselineMode, 1, 1, 1, 1)
        self.labelBaselineStart = QtWidgets.QLabel(self.groupBoxBaseline)
        self.labelBaselineStart.setObjectName("labelBaselineStart")
        self.gridLayout_9.addWidget(self.labelBaselineStart, 2, 0, 1, 1)
        self.labelBaselineEnd = QtWidgets.QLabel(self.groupBoxBaseline)
        self.labelBaselineEnd.setObjectName("labelBaselineEnd")
        self.gridLayout_9.addWidget(self.labelBaselineEnd, 3, 0, 1, 1)
        self.labelBaselineMode = QtWidgets.QLabel(self.groupBoxBaseline)
        self.labelBaselineMode.setObjectName("labelBaselineMode")
        self.gridLayout_9.addWidget(self.labelBaselineMode, 1, 0, 1, 1)
        self.checkBoxBaselineCorrection = QtWidgets.QCheckBox(self.groupBoxBaseline)
        self.checkBoxBaselineCorrection.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBoxBaselineCorrection.setText("")
        self.checkBoxBaselineCorrection.setChecked(True)
        self.checkBoxBaselineCorrection.setObjectName("checkBoxBaselineCorrection")
        self.gridLayout_9.addWidget(self.checkBoxBaselineCorrection, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxBaseline, 2, 0, 1, 1)
        self.groupBoxGrouping = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGrouping.setObjectName("groupBoxGrouping")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxGrouping)
        self.formLayout.setObjectName("formLayout")
        self.labelChannels = QtWidgets.QLabel(self.groupBoxGrouping)
        self.labelChannels.setObjectName("labelChannels")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.labelChannels
        )
        self.radioButtonAllChannels = QtWidgets.QRadioButton(self.groupBoxGrouping)
        self.radioButtonAllChannels.setChecked(True)
        self.radioButtonAllChannels.setObjectName("radioButtonAllChannels")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.radioButtonAllChannels
        )
        self.radioButtonChannelAverages = QtWidgets.QRadioButton(self.groupBoxGrouping)
        self.radioButtonChannelAverages.setObjectName("radioButtonChannelAverages")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.radioButtonChannelAverages
        )
        self.gridLayout_4.addWidget(self.groupBoxGrouping, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_4.addItem(spacerItem, 7, 0, 1, 1)
        self.groupBoxFrequency = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxFrequency.setObjectName("groupBoxFrequency")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBoxFrequency)
        self.gridLayout.setObjectName("gridLayout")
        self.labelFrequencyMax = QtWidgets.QLabel(self.groupBoxFrequency)
        self.labelFrequencyMax.setObjectName("labelFrequencyMax")
        self.gridLayout.addWidget(self.labelFrequencyMax, 1, 0, 1, 1)
        self.labelFrequencyMin = QtWidgets.QLabel(self.groupBoxFrequency)
        self.labelFrequencyMin.setObjectName("labelFrequencyMin")
        self.gridLayout.addWidget(self.labelFrequencyMin, 0, 0, 1, 1)
        self.doubleSpinBoxFrequencyMin = QtWidgets.QDoubleSpinBox(
            self.groupBoxFrequency
        )
        self.doubleSpinBoxFrequencyMin.setSingleStep(0.1)
        self.doubleSpinBoxFrequencyMin.setObjectName("doubleSpinBoxFrequencyMin")
        self.gridLayout.addWidget(self.doubleSpinBoxFrequencyMin, 0, 1, 1, 1)
        self.doubleSpinBoxFrequencyMax = QtWidgets.QDoubleSpinBox(
            self.groupBoxFrequency
        )
        self.doubleSpinBoxFrequencyMax.setSingleStep(0.1)
        self.doubleSpinBoxFrequencyMax.setObjectName("doubleSpinBoxFrequencyMax")
        self.gridLayout.addWidget(self.doubleSpinBoxFrequencyMax, 1, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxFrequency, 3, 0, 1, 1)
        self.groupBoxCondition = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxCondition.setObjectName("groupBoxCondition")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBoxCondition)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.labelCondition = QtWidgets.QLabel(self.groupBoxCondition)
        self.labelCondition.setObjectName("labelCondition")
        self.gridLayout_5.addWidget(self.labelCondition, 0, 0, 1, 1)
        self.comboBoxCondition = QtWidgets.QComboBox(self.groupBoxCondition)
        self.comboBoxCondition.setObjectName("comboBoxCondition")
        self.gridLayout_5.addWidget(self.comboBoxCondition, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxCondition, 5, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(TFROutputOptions)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonOk = QtWidgets.QPushButton(TFROutputOptions)
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.horizontalLayout.addWidget(self.pushButtonOk)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(TFROutputOptions)
        self.checkBoxBaselineCorrection.toggled["bool"].connect(
            self.comboBoxBaselineMode.setEnabled
        )
        self.checkBoxBaselineCorrection.toggled["bool"].connect(
            self.doubleSpinBoxBaselineStart.setEnabled
        )
        self.checkBoxBaselineCorrection.toggled["bool"].connect(
            self.doubleSpinBoxBaselineEnd.setEnabled
        )
        self.pushButtonCancel.clicked.connect(TFROutputOptions.reject)
        self.pushButtonOk.clicked.connect(TFROutputOptions.accept)
        QtCore.QMetaObject.connectSlotsByName(TFROutputOptions)
        TFROutputOptions.setTabOrder(self.scrollArea, self.checkBoxBaselineCorrection)
        TFROutputOptions.setTabOrder(
            self.checkBoxBaselineCorrection, self.comboBoxBaselineMode
        )
        TFROutputOptions.setTabOrder(
            self.comboBoxBaselineMode, self.doubleSpinBoxBaselineStart
        )
        TFROutputOptions.setTabOrder(
            self.doubleSpinBoxBaselineStart, self.doubleSpinBoxBaselineEnd
        )
        TFROutputOptions.setTabOrder(
            self.doubleSpinBoxBaselineEnd, self.doubleSpinBoxFrequencyMin
        )
        TFROutputOptions.setTabOrder(
            self.doubleSpinBoxFrequencyMin, self.doubleSpinBoxFrequencyMax
        )
        TFROutputOptions.setTabOrder(
            self.doubleSpinBoxFrequencyMax, self.doubleSpinBoxTimeStart
        )
        TFROutputOptions.setTabOrder(
            self.doubleSpinBoxTimeStart, self.doubleSpinBoxTimeEnd
        )
        TFROutputOptions.setTabOrder(self.doubleSpinBoxTimeEnd, self.comboBoxCondition)
        TFROutputOptions.setTabOrder(
            self.comboBoxCondition, self.radioButtonAllChannels
        )
        TFROutputOptions.setTabOrder(
            self.radioButtonAllChannels, self.radioButtonChannelAverages
        )
        TFROutputOptions.setTabOrder(
            self.radioButtonChannelAverages, self.pushButtonCancel
        )
        TFROutputOptions.setTabOrder(self.pushButtonCancel, self.pushButtonOk)

    def retranslateUi(self, TFROutputOptions):
        _translate = QtCore.QCoreApplication.translate
        TFROutputOptions.setWindowTitle(
            _translate("TFROutputOptions", "Meggie - Output options")
        )
        self.groupBox.setTitle(_translate("TFROutputOptions", "Time settings:"))
        self.labelTimeStart.setText(_translate("TFROutputOptions", "Start (s):"))
        self.labelTimeEnd.setText(_translate("TFROutputOptions", "End (s):"))
        self.groupBoxBaseline.setTitle(_translate("TFROutputOptions", "Baseline:"))
        self.labelBaselineCorrection.setText(
            _translate("TFROutputOptions", "Baseline correction:")
        )
        self.comboBoxBaselineMode.setItemText(0, _translate("TFROutputOptions", "mean"))
        self.comboBoxBaselineMode.setItemText(
            1, _translate("TFROutputOptions", "ratio")
        )
        self.comboBoxBaselineMode.setItemText(
            2, _translate("TFROutputOptions", "logratio")
        )
        self.comboBoxBaselineMode.setItemText(
            3, _translate("TFROutputOptions", "percent")
        )
        self.comboBoxBaselineMode.setItemText(
            4, _translate("TFROutputOptions", "zscore")
        )
        self.labelBaselineStart.setText(
            _translate("TFROutputOptions", "Baseline start (s):")
        )
        self.labelBaselineEnd.setText(
            _translate("TFROutputOptions", "Baseline end (s):")
        )
        self.labelBaselineMode.setText(_translate("TFROutputOptions", "Baseline mode:"))
        self.groupBoxGrouping.setTitle(_translate("TFROutputOptions", "Grouping:"))
        self.labelChannels.setText(_translate("TFROutputOptions", "Type:"))
        self.radioButtonAllChannels.setText(
            _translate("TFROutputOptions", "All channels")
        )
        self.radioButtonChannelAverages.setText(
            _translate("TFROutputOptions", "Channel averages")
        )
        self.groupBoxFrequency.setTitle(
            _translate("TFROutputOptions", "Frequency settings:")
        )
        self.labelFrequencyMax.setText(
            _translate("TFROutputOptions", "Maximum frequency (Hz):")
        )
        self.labelFrequencyMin.setText(
            _translate("TFROutputOptions", "Minimum frequency (Hz):")
        )
        self.groupBoxCondition.setTitle(_translate("TFROutputOptions", "Condition:"))
        self.labelCondition.setText(_translate("TFROutputOptions", "Select condition:"))
        self.pushButtonCancel.setText(_translate("TFROutputOptions", "Cancel"))
        self.pushButtonOk.setText(_translate("TFROutputOptions", "Accept"))
