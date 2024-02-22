# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_ui_files/tabs/tfr/TFRDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TFRDialog(object):
    def setupUi(self, TFRDialog):
        TFRDialog.setObjectName("TFRDialog")
        TFRDialog.resize(512, 535)
        self.gridLayout_2 = QtWidgets.QGridLayout(TFRDialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutButtons.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(TFRDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(TFRDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayoutButtons.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(TFRDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayoutButtons.addWidget(self.pushButtonApply)
        self.gridLayout_2.addLayout(self.horizontalLayoutButtons, 1, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(TFRDialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 480, 783))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBoxMisc = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxMisc.setObjectName("groupBoxMisc")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBoxMisc)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.gridLayout_10 = QtWidgets.QGridLayout()
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.spinBoxDecim = QtWidgets.QSpinBox(self.groupBoxMisc)
        self.spinBoxDecim.setMinimum(1)
        self.spinBoxDecim.setMaximum(1000)
        self.spinBoxDecim.setProperty("value", 1)
        self.spinBoxDecim.setObjectName("spinBoxDecim")
        self.gridLayout_10.addWidget(self.spinBoxDecim, 0, 1, 1, 1)
        self.labelDecim = QtWidgets.QLabel(self.groupBoxMisc)
        self.labelDecim.setObjectName("labelDecim")
        self.gridLayout_10.addWidget(self.labelDecim, 0, 0, 1, 1)
        self.gridLayout_9.addLayout(self.gridLayout_10, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelSubtractEvoked = QtWidgets.QLabel(self.groupBoxMisc)
        self.labelSubtractEvoked.setObjectName("labelSubtractEvoked")
        self.horizontalLayout.addWidget(self.labelSubtractEvoked)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.checkBoxSubtractEvoked = QtWidgets.QCheckBox(self.groupBoxMisc)
        self.checkBoxSubtractEvoked.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBoxSubtractEvoked.setText("")
        self.checkBoxSubtractEvoked.setObjectName("checkBoxSubtractEvoked")
        self.horizontalLayout.addWidget(self.checkBoxSubtractEvoked)
        self.gridLayout_9.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxMisc, 4, 0, 1, 1)
        self.groupBoxFrequencies = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(
            self.groupBoxFrequencies.sizePolicy().hasHeightForWidth()
        )
        self.groupBoxFrequencies.setSizePolicy(sizePolicy)
        self.groupBoxFrequencies.setObjectName("groupBoxFrequencies")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBoxFrequencies)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.labelMinFreq = QtWidgets.QLabel(self.groupBoxFrequencies)
        self.labelMinFreq.setObjectName("labelMinFreq")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelMinFreq)
        self.doubleSpinBoxMinFreq = QtWidgets.QDoubleSpinBox(self.groupBoxFrequencies)
        self.doubleSpinBoxMinFreq.setMinimum(0.0)
        self.doubleSpinBoxMinFreq.setMaximum(1000.0)
        self.doubleSpinBoxMinFreq.setProperty("value", 5.0)
        self.doubleSpinBoxMinFreq.setObjectName("doubleSpinBoxMinFreq")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxMinFreq
        )
        self.labelMaxFreq = QtWidgets.QLabel(self.groupBoxFrequencies)
        self.labelMaxFreq.setObjectName("labelMaxFreq")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelMaxFreq)
        self.doubleSpinBoxMaxFreq = QtWidgets.QDoubleSpinBox(self.groupBoxFrequencies)
        self.doubleSpinBoxMaxFreq.setMinimum(0.0)
        self.doubleSpinBoxMaxFreq.setMaximum(1000.0)
        self.doubleSpinBoxMaxFreq.setProperty("value", 30.0)
        self.doubleSpinBoxMaxFreq.setObjectName("doubleSpinBoxMaxFreq")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxMaxFreq
        )
        self.labelFrequencyInterval = QtWidgets.QLabel(self.groupBoxFrequencies)
        self.labelFrequencyInterval.setObjectName("labelFrequencyInterval")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelFrequencyInterval
        )
        self.doubleSpinBoxFreqInterval = QtWidgets.QDoubleSpinBox(
            self.groupBoxFrequencies
        )
        self.doubleSpinBoxFreqInterval.setMinimum(0.1)
        self.doubleSpinBoxFreqInterval.setMaximum(99.99)
        self.doubleSpinBoxFreqInterval.setProperty("value", 0.5)
        self.doubleSpinBoxFreqInterval.setObjectName("doubleSpinBoxFreqInterval")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxFreqInterval
        )
        self.label_7 = QtWidgets.QLabel(self.groupBoxFrequencies)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.radioButtonFixed = QtWidgets.QRadioButton(self.groupBoxFrequencies)
        self.radioButtonFixed.setChecked(False)
        self.radioButtonFixed.setObjectName("radioButtonFixed")
        self.horizontalLayout_18.addWidget(self.radioButtonFixed)
        self.formLayout.setLayout(
            4, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_18
        )
        self.doubleSpinBoxNcycles = QtWidgets.QDoubleSpinBox(self.groupBoxFrequencies)
        self.doubleSpinBoxNcycles.setEnabled(False)
        self.doubleSpinBoxNcycles.setMinimum(1.0)
        self.doubleSpinBoxNcycles.setMaximum(100.0)
        self.doubleSpinBoxNcycles.setProperty("value", 5.0)
        self.doubleSpinBoxNcycles.setObjectName("doubleSpinBoxNcycles")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxNcycles
        )
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.radioButtonAdapted = QtWidgets.QRadioButton(self.groupBoxFrequencies)
        self.radioButtonAdapted.setToolTip("")
        self.radioButtonAdapted.setCheckable(True)
        self.radioButtonAdapted.setChecked(True)
        self.radioButtonAdapted.setObjectName("radioButtonAdapted")
        self.horizontalLayout_19.addWidget(self.radioButtonAdapted)
        self.formLayout.setLayout(
            5, QtWidgets.QFormLayout.LabelRole, self.horizontalLayout_19
        )
        self.doubleSpinBoxCycleFactor = QtWidgets.QDoubleSpinBox(
            self.groupBoxFrequencies
        )
        self.doubleSpinBoxCycleFactor.setEnabled(True)
        self.doubleSpinBoxCycleFactor.setToolTip("")
        self.doubleSpinBoxCycleFactor.setMinimum(0.0)
        self.doubleSpinBoxCycleFactor.setMaximum(10.0)
        self.doubleSpinBoxCycleFactor.setSingleStep(1.0)
        self.doubleSpinBoxCycleFactor.setProperty("value", 2.0)
        self.doubleSpinBoxCycleFactor.setObjectName("doubleSpinBoxCycleFactor")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxCycleFactor
        )
        self.gridLayout_5.addLayout(self.formLayout, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxFrequencies, 3, 0, 1, 2)
        self.groupBoxGeneral = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.groupBoxGeneral)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.labelEpochName = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelEpochName.setObjectName("labelEpochName")
        self.gridLayout_6.addWidget(self.labelEpochName, 1, 0, 1, 1)
        self.lineEditEpochName = QtWidgets.QLineEdit(self.groupBoxGeneral)
        self.lineEditEpochName.setEnabled(False)
        self.lineEditEpochName.setObjectName("lineEditEpochName")
        self.gridLayout_6.addWidget(self.lineEditEpochName, 1, 1, 1, 1)
        self.labelTFRName = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelTFRName.setObjectName("labelTFRName")
        self.gridLayout_6.addWidget(self.labelTFRName, 2, 0, 1, 1)
        self.lineEditTFRName = QtWidgets.QLineEdit(self.groupBoxGeneral)
        self.lineEditTFRName.setObjectName("lineEditTFRName")
        self.gridLayout_6.addWidget(self.lineEditTFRName, 2, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxGeneral, 0, 0, 1, 1)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxBatching, 5, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_4.addItem(spacerItem2, 6, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(TFRDialog)
        self.radioButtonAdapted.toggled["bool"].connect(
            self.doubleSpinBoxCycleFactor.setEnabled
        )
        self.radioButtonFixed.toggled["bool"].connect(
            self.doubleSpinBoxNcycles.setEnabled
        )
        self.pushButtonCancel.clicked.connect(TFRDialog.reject)
        self.pushButtonBatch.clicked.connect(TFRDialog.acceptBatch)
        self.pushButtonApply.clicked.connect(TFRDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(TFRDialog)
        TFRDialog.setTabOrder(self.scrollArea, self.radioButtonFixed)
        TFRDialog.setTabOrder(self.radioButtonFixed, self.radioButtonAdapted)

    def retranslateUi(self, TFRDialog):
        _translate = QtCore.QCoreApplication.translate
        TFRDialog.setWindowTitle(_translate("TFRDialog", "Meggie - Compute TFR"))
        self.pushButtonCancel.setText(_translate("TFRDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("TFRDialog", "Batch"))
        self.pushButtonApply.setText(_translate("TFRDialog", "Apply"))
        self.groupBoxMisc.setTitle(_translate("TFRDialog", "Miscellaneous"))
        self.labelDecim.setText(_translate("TFRDialog", "Decimation factor:"))
        self.labelSubtractEvoked.setText(_translate("TFRDialog", "Subtract evoked:"))
        self.groupBoxFrequencies.setTitle(_translate("TFRDialog", "Frequency window"))
        self.labelMinFreq.setText(_translate("TFRDialog", "Min frequency:"))
        self.doubleSpinBoxMinFreq.setSuffix(_translate("TFRDialog", "Hz"))
        self.labelMaxFreq.setText(_translate("TFRDialog", "Max frequency:"))
        self.doubleSpinBoxMaxFreq.setSuffix(_translate("TFRDialog", "Hz"))
        self.labelFrequencyInterval.setText(
            _translate("TFRDialog", "Frequency interval:")
        )
        self.doubleSpinBoxFreqInterval.setSuffix(_translate("TFRDialog", "Hz"))
        self.label_7.setText(_translate("TFRDialog", "Number of cycles"))
        self.radioButtonFixed.setText(_translate("TFRDialog", "Fixed"))
        self.radioButtonAdapted.setText(_translate("TFRDialog", "Freqs divided by"))
        self.groupBoxGeneral.setTitle(_translate("TFRDialog", "General:"))
        self.labelEpochName.setText(_translate("TFRDialog", "Epoch name: "))
        self.labelTFRName.setText(_translate("TFRDialog", "TFR name:"))
        self.groupBoxBatching.setTitle(_translate("TFRDialog", "Batching"))
