# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'powerSpectrumDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_PowerSpectrumDialog(object):
    def setupUi(self, PowerSpectrumDialog):
        PowerSpectrumDialog.setObjectName("PowerSpectrumDialog")
        PowerSpectrumDialog.resize(561, 712)
        self.gridLayout = QtWidgets.QGridLayout(PowerSpectrumDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(PowerSpectrumDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 527, 840))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBoxGeneral = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxGeneral)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelName = QtWidgets.QLabel(self.groupBoxGeneral)
        self.labelName.setObjectName("labelName")
        self.gridLayout_3.addWidget(self.labelName, 0, 0, 1, 1)
        self.lineEditName = QtWidgets.QLineEdit(self.groupBoxGeneral)
        self.lineEditName.setObjectName("lineEditName")
        self.gridLayout_3.addWidget(self.lineEditName, 0, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout_3.addItem(spacerItem, 0, 1, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxGeneral, 0, 0, 1, 1)
        self.groupBoxIntervals = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.groupBoxIntervals.sizePolicy().hasHeightForWidth()
        )
        self.groupBoxIntervals.setSizePolicy(sizePolicy)
        self.groupBoxIntervals.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBoxIntervals.setObjectName("groupBoxIntervals")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBoxIntervals)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelGroup = QtWidgets.QLabel(self.groupBoxIntervals)
        self.labelGroup.setObjectName("labelGroup")
        self.gridLayout_2.addWidget(self.labelGroup, 0, 0, 1, 1)
        self.labelTmax = QtWidgets.QLabel(self.groupBoxIntervals)
        self.labelTmax.setObjectName("labelTmax")
        self.gridLayout_2.addWidget(self.labelTmax, 2, 0, 1, 1)
        self.doubleSpinBoxTmin = QtWidgets.QDoubleSpinBox(self.groupBoxIntervals)
        self.doubleSpinBoxTmin.setMaximum(1000000000.0)
        self.doubleSpinBoxTmin.setObjectName("doubleSpinBoxTmin")
        self.gridLayout_2.addWidget(self.doubleSpinBoxTmin, 1, 1, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(self.groupBoxIntervals)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout_2.addWidget(self.pushButtonAdd, 3, 0, 1, 2)
        self.comboBoxAvgGroup = QtWidgets.QComboBox(self.groupBoxIntervals)
        self.comboBoxAvgGroup.setObjectName("comboBoxAvgGroup")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.comboBoxAvgGroup.addItem("")
        self.gridLayout_2.addWidget(self.comboBoxAvgGroup, 0, 1, 1, 1)
        self.doubleSpinBoxTmax = QtWidgets.QDoubleSpinBox(self.groupBoxIntervals)
        self.doubleSpinBoxTmax.setMaximum(1000000000.0)
        self.doubleSpinBoxTmax.setObjectName("doubleSpinBoxTmax")
        self.gridLayout_2.addWidget(self.doubleSpinBoxTmax, 2, 1, 1, 1)
        self.labelTmin = QtWidgets.QLabel(self.groupBoxIntervals)
        self.labelTmin.setObjectName("labelTmin")
        self.gridLayout_2.addWidget(self.labelTmin, 1, 0, 1, 1)
        self.pushButtonAddAdvanced = QtWidgets.QPushButton(self.groupBoxIntervals)
        self.pushButtonAddAdvanced.setObjectName("pushButtonAddAdvanced")
        self.gridLayout_2.addWidget(self.pushButtonAddAdvanced, 4, 0, 1, 2)
        self.pushButtonClearRow = QtWidgets.QPushButton(self.groupBoxIntervals)
        self.pushButtonClearRow.setObjectName("pushButtonClearRow")
        self.gridLayout_2.addWidget(self.pushButtonClearRow, 5, 0, 1, 2)
        self.pushButtonClear = QtWidgets.QPushButton(self.groupBoxIntervals)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.gridLayout_2.addWidget(self.pushButtonClear, 6, 0, 1, 2)
        self.listWidgetIntervals = QtWidgets.QListWidget(self.groupBoxIntervals)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.listWidgetIntervals.sizePolicy().hasHeightForWidth()
        )
        self.listWidgetIntervals.setSizePolicy(sizePolicy)
        self.listWidgetIntervals.setObjectName("listWidgetIntervals")
        self.gridLayout_2.addWidget(self.listWidgetIntervals, 0, 2, 7, 1)
        self.gridLayout_4.addWidget(self.groupBoxIntervals, 2, 0, 1, 1)
        self.groupBoxConditions = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxConditions.setObjectName("groupBoxConditions")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxConditions)
        self.formLayout.setObjectName("formLayout")
        self.labelFmin = QtWidgets.QLabel(self.groupBoxConditions)
        self.labelFmin.setObjectName("labelFmin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelFmin)
        self.spinBoxFmin = QtWidgets.QSpinBox(self.groupBoxConditions)
        self.spinBoxFmin.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxFmin.setMaximum(1000)
        self.spinBoxFmin.setProperty("value", 1)
        self.spinBoxFmin.setObjectName("spinBoxFmin")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxFmin)
        self.labelFmax = QtWidgets.QLabel(self.groupBoxConditions)
        self.labelFmax.setObjectName("labelFmax")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelFmax)
        self.spinBoxFmax = QtWidgets.QSpinBox(self.groupBoxConditions)
        self.spinBoxFmax.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxFmax.setMaximum(1000)
        self.spinBoxFmax.setProperty("value", 40)
        self.spinBoxFmax.setObjectName("spinBoxFmax")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.spinBoxFmax)
        self.labelOverlap = QtWidgets.QLabel(self.groupBoxConditions)
        self.labelOverlap.setObjectName("labelOverlap")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelOverlap)
        self.spinBoxOverlap = QtWidgets.QSpinBox(self.groupBoxConditions)
        self.spinBoxOverlap.setMaximum(100000)
        self.spinBoxOverlap.setProperty("value", 256)
        self.spinBoxOverlap.setObjectName("spinBoxOverlap")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.spinBoxOverlap
        )
        self.labelNfft = QtWidgets.QLabel(self.groupBoxConditions)
        self.labelNfft.setObjectName("labelNfft")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelNfft)
        self.spinBoxNfft = QtWidgets.QSpinBox(self.groupBoxConditions)
        self.spinBoxNfft.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxNfft.setMaximum(100000)
        self.spinBoxNfft.setProperty("value", 512)
        self.spinBoxNfft.setObjectName("spinBoxNfft")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.spinBoxNfft)
        self.gridLayout_4.addWidget(self.groupBoxConditions, 1, 0, 1, 1)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxBatching, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayoutButtons = QtWidgets.QHBoxLayout()
        self.horizontalLayoutButtons.setObjectName("horizontalLayoutButtons")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayoutButtons.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(PowerSpectrumDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayoutButtons.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(PowerSpectrumDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayoutButtons.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(PowerSpectrumDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayoutButtons.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayoutButtons, 1, 0, 1, 1)

        self.retranslateUi(PowerSpectrumDialog)
        self.pushButtonApply.clicked.connect(PowerSpectrumDialog.accept)
        self.pushButtonCancel.clicked.connect(PowerSpectrumDialog.reject)
        self.pushButtonBatch.clicked.connect(PowerSpectrumDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(PowerSpectrumDialog)

    def retranslateUi(self, PowerSpectrumDialog):
        _translate = QtCore.QCoreApplication.translate
        PowerSpectrumDialog.setWindowTitle(
            _translate("PowerSpectrumDialog", "Meggie - Create spectrums")
        )
        self.groupBoxGeneral.setTitle(_translate("PowerSpectrumDialog", "General"))
        self.labelName.setText(_translate("PowerSpectrumDialog", "Spectrum name:"))
        self.groupBoxIntervals.setTitle(
            _translate("PowerSpectrumDialog", "Select time intervals")
        )
        self.labelGroup.setText(_translate("PowerSpectrumDialog", "Average group:"))
        self.labelTmax.setText(_translate("PowerSpectrumDialog", "End time:"))
        self.doubleSpinBoxTmin.setSuffix(_translate("PowerSpectrumDialog", " s"))
        self.pushButtonAdd.setText(_translate("PowerSpectrumDialog", "Add to list"))
        self.comboBoxAvgGroup.setItemText(0, _translate("PowerSpectrumDialog", "1"))
        self.comboBoxAvgGroup.setItemText(1, _translate("PowerSpectrumDialog", "2"))
        self.comboBoxAvgGroup.setItemText(2, _translate("PowerSpectrumDialog", "3"))
        self.comboBoxAvgGroup.setItemText(3, _translate("PowerSpectrumDialog", "4"))
        self.comboBoxAvgGroup.setItemText(4, _translate("PowerSpectrumDialog", "5"))
        self.comboBoxAvgGroup.setItemText(5, _translate("PowerSpectrumDialog", "6"))
        self.comboBoxAvgGroup.setItemText(6, _translate("PowerSpectrumDialog", "7"))
        self.comboBoxAvgGroup.setItemText(7, _translate("PowerSpectrumDialog", "8"))
        self.doubleSpinBoxTmax.setSuffix(_translate("PowerSpectrumDialog", " s"))
        self.labelTmin.setText(_translate("PowerSpectrumDialog", "Start time:"))
        self.pushButtonAddAdvanced.setText(
            _translate("PowerSpectrumDialog", "Add advanced...")
        )
        self.pushButtonClearRow.setText(_translate("PowerSpectrumDialog", "Clear row"))
        self.pushButtonClear.setText(_translate("PowerSpectrumDialog", "Clear list"))
        self.groupBoxConditions.setTitle(
            _translate("PowerSpectrumDialog", "Conditions")
        )
        self.labelFmin.setText(
            _translate("PowerSpectrumDialog", "Min frequency of interest:")
        )
        self.spinBoxFmin.setSuffix(_translate("PowerSpectrumDialog", "Hz"))
        self.labelFmax.setText(
            _translate("PowerSpectrumDialog", "Max frequency of interest:")
        )
        self.spinBoxFmax.setSuffix(_translate("PowerSpectrumDialog", "Hz"))
        self.labelOverlap.setText(_translate("PowerSpectrumDialog", "Overlap:"))
        self.labelNfft.setText(_translate("PowerSpectrumDialog", "Length of window:"))
        self.groupBoxBatching.setTitle(_translate("PowerSpectrumDialog", "Batching"))
        self.pushButtonCancel.setText(_translate("PowerSpectrumDialog", "Cancel"))
        self.pushButtonBatch.setText(_translate("PowerSpectrumDialog", "Batch"))
        self.pushButtonApply.setText(_translate("PowerSpectrumDialog", "Apply"))
