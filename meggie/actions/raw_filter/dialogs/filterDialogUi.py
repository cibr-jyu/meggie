# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './meggie/meggie/actions/raw_filter/dialogs/filterDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DialogFilter(object):
    def setupUi(self, DialogFilter):
        DialogFilter.setObjectName("DialogFilter")
        DialogFilter.resize(712, 697)
        self.gridLayout = QtWidgets.QGridLayout(DialogFilter)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(DialogFilter)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(DialogFilter)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayout.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(DialogFilter)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(DialogFilter)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 680, 785))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBoxBandstop = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBandstop.setObjectName("groupBoxBandstop")
        self.formLayout = QtWidgets.QFormLayout(self.groupBoxBandstop)
        self.formLayout.setObjectName("formLayout")
        self.checkBoxBandstop = QtWidgets.QCheckBox(self.groupBoxBandstop)
        self.checkBoxBandstop.setChecked(False)
        self.checkBoxBandstop.setObjectName("checkBoxBandstop")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.checkBoxBandstop
        )
        self.doubleSpinBoxBandstopFreq = QtWidgets.QDoubleSpinBox(self.groupBoxBandstop)
        self.doubleSpinBoxBandstopFreq.setEnabled(False)
        self.doubleSpinBoxBandstopFreq.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxBandstopFreq.setDecimals(3)
        self.doubleSpinBoxBandstopFreq.setMaximum(10000.0)
        self.doubleSpinBoxBandstopFreq.setSingleStep(1.0)
        self.doubleSpinBoxBandstopFreq.setProperty("value", 50.0)
        self.doubleSpinBoxBandstopFreq.setObjectName("doubleSpinBoxBandstopFreq")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxBandstopFreq
        )
        self.checkBoxBandstop2 = QtWidgets.QCheckBox(self.groupBoxBandstop)
        self.checkBoxBandstop2.setObjectName("checkBoxBandstop2")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.checkBoxBandstop2
        )
        self.doubleSpinBoxBandstopFreq2 = QtWidgets.QDoubleSpinBox(
            self.groupBoxBandstop
        )
        self.doubleSpinBoxBandstopFreq2.setEnabled(False)
        self.doubleSpinBoxBandstopFreq2.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxBandstopFreq2.setDecimals(3)
        self.doubleSpinBoxBandstopFreq2.setMaximum(10000.0)
        self.doubleSpinBoxBandstopFreq2.setSingleStep(1.0)
        self.doubleSpinBoxBandstopFreq2.setProperty("value", 100.0)
        self.doubleSpinBoxBandstopFreq2.setObjectName("doubleSpinBoxBandstopFreq2")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxBandstopFreq2
        )
        self.labelBandStopNotchWidth = QtWidgets.QLabel(self.groupBoxBandstop)
        self.labelBandStopNotchWidth.setObjectName("labelBandStopNotchWidth")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelBandStopNotchWidth
        )
        self.doubleSpinBoxBandstopWidth = QtWidgets.QDoubleSpinBox(
            self.groupBoxBandstop
        )
        self.doubleSpinBoxBandstopWidth.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxBandstopWidth.setDecimals(3)
        self.doubleSpinBoxBandstopWidth.setMaximum(10000.0)
        self.doubleSpinBoxBandstopWidth.setSingleStep(1.0)
        self.doubleSpinBoxBandstopWidth.setProperty("value", 1.0)
        self.doubleSpinBoxBandstopWidth.setObjectName("doubleSpinBoxBandstopWidth")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxBandstopWidth
        )
        self.labelTransBw = QtWidgets.QLabel(self.groupBoxBandstop)
        self.labelTransBw.setObjectName("labelTransBw")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.labelTransBw)
        self.doubleSpinBoxNotchTransBw = QtWidgets.QDoubleSpinBox(self.groupBoxBandstop)
        self.doubleSpinBoxNotchTransBw.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxNotchTransBw.setDecimals(3)
        self.doubleSpinBoxNotchTransBw.setMinimum(0.1)
        self.doubleSpinBoxNotchTransBw.setSingleStep(0.1)
        self.doubleSpinBoxNotchTransBw.setProperty("value", 0.5)
        self.doubleSpinBoxNotchTransBw.setObjectName("doubleSpinBoxNotchTransBw")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxNotchTransBw
        )
        self.labelBandstopFilterLength = QtWidgets.QLabel(self.groupBoxBandstop)
        self.labelBandstopFilterLength.setObjectName("labelBandstopFilterLength")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.LabelRole, self.labelBandstopFilterLength
        )
        self.doubleSpinBoxBandStopLength = QtWidgets.QDoubleSpinBox(
            self.groupBoxBandstop
        )
        self.doubleSpinBoxBandStopLength.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxBandStopLength.setSingleStep(0.1)
        self.doubleSpinBoxBandStopLength.setProperty("value", 10.0)
        self.doubleSpinBoxBandStopLength.setObjectName("doubleSpinBoxBandStopLength")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxBandStopLength
        )
        self.gridLayout_6.addWidget(self.groupBoxBandstop, 1, 0, 1, 1)
        self.groupBoxBandpass = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBandpass.setObjectName("groupBoxBandpass")
        self.formLayout_5 = QtWidgets.QFormLayout(self.groupBoxBandpass)
        self.formLayout_5.setObjectName("formLayout_5")
        self.checkBoxHighpass = QtWidgets.QCheckBox(self.groupBoxBandpass)
        self.checkBoxHighpass.setChecked(True)
        self.checkBoxHighpass.setObjectName("checkBoxHighpass")
        self.formLayout_5.setWidget(
            0, QtWidgets.QFormLayout.LabelRole, self.checkBoxHighpass
        )
        self.doubleSpinBoxHighpassCutoff = QtWidgets.QDoubleSpinBox(
            self.groupBoxBandpass
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBoxHighpassCutoff.sizePolicy().hasHeightForWidth()
        )
        self.doubleSpinBoxHighpassCutoff.setSizePolicy(sizePolicy)
        self.doubleSpinBoxHighpassCutoff.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxHighpassCutoff.setDecimals(3)
        self.doubleSpinBoxHighpassCutoff.setMaximum(1000000000.0)
        self.doubleSpinBoxHighpassCutoff.setSingleStep(1.0)
        self.doubleSpinBoxHighpassCutoff.setProperty("value", 1.0)
        self.doubleSpinBoxHighpassCutoff.setObjectName("doubleSpinBoxHighpassCutoff")
        self.formLayout_5.setWidget(
            0, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxHighpassCutoff
        )
        self.checkBoxLowpass = QtWidgets.QCheckBox(self.groupBoxBandpass)
        self.checkBoxLowpass.setChecked(True)
        self.checkBoxLowpass.setObjectName("checkBoxLowpass")
        self.formLayout_5.setWidget(
            1, QtWidgets.QFormLayout.LabelRole, self.checkBoxLowpass
        )
        self.doubleSpinBoxLowpassCutoff = QtWidgets.QDoubleSpinBox(
            self.groupBoxBandpass
        )
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.doubleSpinBoxLowpassCutoff.sizePolicy().hasHeightForWidth()
        )
        self.doubleSpinBoxLowpassCutoff.setSizePolicy(sizePolicy)
        self.doubleSpinBoxLowpassCutoff.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxLowpassCutoff.setDecimals(3)
        self.doubleSpinBoxLowpassCutoff.setMaximum(10000.0)
        self.doubleSpinBoxLowpassCutoff.setSingleStep(1.0)
        self.doubleSpinBoxLowpassCutoff.setProperty("value", 40.0)
        self.doubleSpinBoxLowpassCutoff.setObjectName("doubleSpinBoxLowpassCutoff")
        self.formLayout_5.setWidget(
            1, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxLowpassCutoff
        )
        self.labelTransitionWidth = QtWidgets.QLabel(self.groupBoxBandpass)
        self.labelTransitionWidth.setObjectName("labelTransitionWidth")
        self.formLayout_5.setWidget(
            2, QtWidgets.QFormLayout.LabelRole, self.labelTransitionWidth
        )
        self.doubleSpinBoxTransBandwidth = QtWidgets.QDoubleSpinBox(
            self.groupBoxBandpass
        )
        self.doubleSpinBoxTransBandwidth.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxTransBandwidth.setDecimals(3)
        self.doubleSpinBoxTransBandwidth.setMaximum(10000.0)
        self.doubleSpinBoxTransBandwidth.setSingleStep(0.1)
        self.doubleSpinBoxTransBandwidth.setProperty("value", 0.5)
        self.doubleSpinBoxTransBandwidth.setObjectName("doubleSpinBoxTransBandwidth")
        self.formLayout_5.setWidget(
            2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxTransBandwidth
        )
        self.labelFilterLength = QtWidgets.QLabel(self.groupBoxBandpass)
        self.labelFilterLength.setObjectName("labelFilterLength")
        self.formLayout_5.setWidget(
            3, QtWidgets.QFormLayout.LabelRole, self.labelFilterLength
        )
        self.doubleSpinBoxLength = QtWidgets.QDoubleSpinBox(self.groupBoxBandpass)
        self.doubleSpinBoxLength.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.doubleSpinBoxLength.setSingleStep(0.1)
        self.doubleSpinBoxLength.setProperty("value", 10.0)
        self.doubleSpinBoxLength.setObjectName("doubleSpinBoxLength")
        self.formLayout_5.setWidget(
            3, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxLength
        )
        self.gridLayout_6.addWidget(self.groupBoxBandpass, 0, 0, 1, 1)
        self.groupBoxPreview = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxPreview.setObjectName("groupBoxPreview")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxPreview)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonPreview = QtWidgets.QPushButton(self.groupBoxPreview)
        self.pushButtonPreview.setEnabled(True)
        self.pushButtonPreview.setObjectName("pushButtonPreview")
        self.gridLayout_3.addWidget(self.pushButtonPreview, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBoxPreview, 2, 0, 1, 1)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_6.addWidget(self.groupBoxBatching, 3, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(DialogFilter)
        self.pushButtonApply.clicked.connect(DialogFilter.accept)  # type: ignore
        self.pushButtonCancel.clicked.connect(DialogFilter.reject)  # type: ignore
        self.pushButtonBatch.clicked.connect(DialogFilter.acceptBatch)  # type: ignore
        self.checkBoxBandstop.toggled["bool"].connect(self.doubleSpinBoxBandstopFreq.setEnabled)  # type: ignore
        self.checkBoxBandstop2.toggled["bool"].connect(self.doubleSpinBoxBandstopFreq2.setEnabled)  # type: ignore
        self.checkBoxHighpass.toggled["bool"].connect(self.doubleSpinBoxHighpassCutoff.setEnabled)  # type: ignore
        self.checkBoxLowpass.toggled["bool"].connect(self.doubleSpinBoxLowpassCutoff.setEnabled)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(DialogFilter)

    def retranslateUi(self, DialogFilter):
        _translate = QtCore.QCoreApplication.translate
        DialogFilter.setWindowTitle(_translate("DialogFilter", "Meggie - Filtering"))
        self.pushButtonCancel.setText(_translate("DialogFilter", "Cancel"))
        self.pushButtonBatch.setText(_translate("DialogFilter", "Batch"))
        self.pushButtonApply.setText(_translate("DialogFilter", "Apply"))
        self.groupBoxBandstop.setTitle(_translate("DialogFilter", "Bandstop filter"))
        self.checkBoxBandstop.setText(
            _translate("DialogFilter", "BandStop filter (notch)")
        )
        self.doubleSpinBoxBandstopFreq.setSuffix(_translate("DialogFilter", " Hz"))
        self.checkBoxBandstop2.setText(
            _translate("DialogFilter", "BandStop filter (notch)")
        )
        self.doubleSpinBoxBandstopFreq2.setSuffix(_translate("DialogFilter", " Hz"))
        self.labelBandStopNotchWidth.setText(
            _translate("DialogFilter", "Notch band width:")
        )
        self.doubleSpinBoxBandstopWidth.setSuffix(_translate("DialogFilter", " Hz"))
        self.labelTransBw.setText(_translate("DialogFilter", "Transition band width:"))
        self.doubleSpinBoxNotchTransBw.setSuffix(_translate("DialogFilter", " Hz"))
        self.labelBandstopFilterLength.setText(
            _translate("DialogFilter", "Filter length:")
        )
        self.doubleSpinBoxBandStopLength.setSuffix(_translate("DialogFilter", "s"))
        self.groupBoxBandpass.setTitle(_translate("DialogFilter", "Bandpass filter"))
        self.checkBoxHighpass.setText(_translate("DialogFilter", "Highpass filter"))
        self.doubleSpinBoxHighpassCutoff.setSuffix(_translate("DialogFilter", " Hz"))
        self.checkBoxLowpass.setText(_translate("DialogFilter", "Lowpass filter"))
        self.doubleSpinBoxLowpassCutoff.setSuffix(_translate("DialogFilter", " Hz"))
        self.labelTransitionWidth.setText(
            _translate("DialogFilter", "Transition band width:")
        )
        self.doubleSpinBoxTransBandwidth.setSuffix(_translate("DialogFilter", " Hz"))
        self.labelFilterLength.setText(_translate("DialogFilter", "Filter length:"))
        self.doubleSpinBoxLength.setSuffix(_translate("DialogFilter", "s"))
        self.groupBoxPreview.setTitle(_translate("DialogFilter", "Preview"))
        self.pushButtonPreview.setText(
            _translate("DialogFilter", "Preview with given filters")
        )
        self.groupBoxBatching.setTitle(_translate("DialogFilter", "Batching"))
