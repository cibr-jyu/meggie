# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eventSelectionDialogUi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_EventSelectionDialog(object):
    def setupUi(self, EventSelectionDialog):
        EventSelectionDialog.setObjectName(_fromUtf8("EventSelectionDialog"))
        EventSelectionDialog.setWindowModality(QtCore.Qt.WindowModal)
        EventSelectionDialog.resize(763, 977)
        self.gridLayout = QtGui.QGridLayout(EventSelectionDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.pushButtonCancel = QtGui.QPushButton(EventSelectionDialog)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout_10.addWidget(self.pushButtonCancel)
        self.pushButtonComputeBatch = QtGui.QPushButton(EventSelectionDialog)
        self.pushButtonComputeBatch.setObjectName(_fromUtf8("pushButtonComputeBatch"))
        self.horizontalLayout_10.addWidget(self.pushButtonComputeBatch)
        self.pushButtonCompute = QtGui.QPushButton(EventSelectionDialog)
        self.pushButtonCompute.setObjectName(_fromUtf8("pushButtonCompute"))
        self.horizontalLayout_10.addWidget(self.pushButtonCompute)
        self.gridLayout.addLayout(self.horizontalLayout_10, 2, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(EventSelectionDialog)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtGui.QFrame.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 745, 920))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(700, 850))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.pushButtonFixedLength = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonFixedLength.setGeometry(QtCore.QRect(570, 430, 151, 31))
        self.pushButtonFixedLength.setObjectName(_fromUtf8("pushButtonFixedLength"))
        self.groupBox = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox.setGeometry(QtCore.QRect(350, 200, 381, 231))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.listWidgetEvents = QtGui.QListWidget(self.groupBox)
        self.listWidgetEvents.setObjectName(_fromUtf8("listWidgetEvents"))
        self.gridLayout_3.addWidget(self.listWidgetEvents, 0, 0, 1, 1)
        self.widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.widget.setGeometry(QtCore.QRect(370, 470, 311, 441))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.groupBoxEvent = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxEvent.setGeometry(QtCore.QRect(10, 200, 332, 231))
        self.groupBoxEvent.setObjectName(_fromUtf8("groupBoxEvent"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxEvent)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.labelStimChannel = QtGui.QLabel(self.groupBoxEvent)
        self.labelStimChannel.setObjectName(_fromUtf8("labelStimChannel"))
        self.horizontalLayout_11.addWidget(self.labelStimChannel)
        self.comboBoxStimChannel = QtGui.QComboBox(self.groupBoxEvent)
        self.comboBoxStimChannel.setObjectName(_fromUtf8("comboBoxStimChannel"))
        self.horizontalLayout_11.addWidget(self.comboBoxStimChannel)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelEventID = QtGui.QLabel(self.groupBoxEvent)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_7.addWidget(self.labelEventID)
        self.spinBoxEventID = QtGui.QSpinBox(self.groupBoxEvent)
        self.spinBoxEventID.setMinimum(1)
        self.spinBoxEventID.setMaximum(999999)
        self.spinBoxEventID.setObjectName(_fromUtf8("spinBoxEventID"))
        self.horizontalLayout_7.addWidget(self.spinBoxEventID)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.labelMask = QtGui.QLabel(self.groupBoxEvent)
        self.labelMask.setObjectName(_fromUtf8("labelMask"))
        self.horizontalLayout_6.addWidget(self.labelMask)
        self.spinBoxMask = QtGui.QSpinBox(self.groupBoxEvent)
        self.spinBoxMask.setEnabled(True)
        self.spinBoxMask.setMinimum(0)
        self.spinBoxMask.setMaximum(9999)
        self.spinBoxMask.setProperty("value", 0)
        self.spinBoxMask.setObjectName(_fromUtf8("spinBoxMask"))
        self.horizontalLayout_6.addWidget(self.spinBoxMask)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.pushButtonAdd = QtGui.QPushButton(self.groupBoxEvent)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.gridLayout_2.addWidget(self.pushButtonAdd, 1, 0, 1, 1)
        self.groupBoxRejection = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxRejection.setGeometry(QtCore.QRect(350, 10, 381, 191))
        self.groupBoxRejection.setObjectName(_fromUtf8("groupBoxRejection"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxRejection)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_31 = QtGui.QHBoxLayout()
        self.horizontalLayout_31.setObjectName(_fromUtf8("horizontalLayout_31"))
        self.checkBoxGrad = QtGui.QCheckBox(self.groupBoxRejection)
        self.checkBoxGrad.setChecked(True)
        self.checkBoxGrad.setObjectName(_fromUtf8("checkBoxGrad"))
        self.horizontalLayout_31.addWidget(self.checkBoxGrad)
        self.doubleSpinBoxGradReject_3 = QtGui.QDoubleSpinBox(self.groupBoxRejection)
        self.doubleSpinBoxGradReject_3.setPrefix(_fromUtf8(""))
        self.doubleSpinBoxGradReject_3.setMinimum(-1.0)
        self.doubleSpinBoxGradReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxGradReject_3.setSingleStep(100.0)
        self.doubleSpinBoxGradReject_3.setProperty("value", 3000.0)
        self.doubleSpinBoxGradReject_3.setObjectName(_fromUtf8("doubleSpinBoxGradReject_3"))
        self.horizontalLayout_31.addWidget(self.doubleSpinBoxGradReject_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_33 = QtGui.QHBoxLayout()
        self.horizontalLayout_33.setObjectName(_fromUtf8("horizontalLayout_33"))
        self.checkBoxMag = QtGui.QCheckBox(self.groupBoxRejection)
        self.checkBoxMag.setChecked(True)
        self.checkBoxMag.setObjectName(_fromUtf8("checkBoxMag"))
        self.horizontalLayout_33.addWidget(self.checkBoxMag)
        self.doubleSpinBoxMagReject_3 = QtGui.QDoubleSpinBox(self.groupBoxRejection)
        self.doubleSpinBoxMagReject_3.setMinimum(-1.0)
        self.doubleSpinBoxMagReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxMagReject_3.setSingleStep(100.0)
        self.doubleSpinBoxMagReject_3.setProperty("value", 4000.0)
        self.doubleSpinBoxMagReject_3.setObjectName(_fromUtf8("doubleSpinBoxMagReject_3"))
        self.horizontalLayout_33.addWidget(self.doubleSpinBoxMagReject_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_33)
        self.horizontalLayout_32 = QtGui.QHBoxLayout()
        self.horizontalLayout_32.setObjectName(_fromUtf8("horizontalLayout_32"))
        self.checkBoxEeg = QtGui.QCheckBox(self.groupBoxRejection)
        self.checkBoxEeg.setChecked(False)
        self.checkBoxEeg.setObjectName(_fromUtf8("checkBoxEeg"))
        self.horizontalLayout_32.addWidget(self.checkBoxEeg)
        self.doubleSpinBoxEEGReject_3 = QtGui.QDoubleSpinBox(self.groupBoxRejection)
        self.doubleSpinBoxEEGReject_3.setEnabled(False)
        self.doubleSpinBoxEEGReject_3.setMinimum(-1.0)
        self.doubleSpinBoxEEGReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxEEGReject_3.setProperty("value", 70.0)
        self.doubleSpinBoxEEGReject_3.setObjectName(_fromUtf8("doubleSpinBoxEEGReject_3"))
        self.horizontalLayout_32.addWidget(self.doubleSpinBoxEEGReject_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_32)
        self.horizontalLayout_34 = QtGui.QHBoxLayout()
        self.horizontalLayout_34.setObjectName(_fromUtf8("horizontalLayout_34"))
        self.checkBoxEog = QtGui.QCheckBox(self.groupBoxRejection)
        self.checkBoxEog.setChecked(False)
        self.checkBoxEog.setObjectName(_fromUtf8("checkBoxEog"))
        self.horizontalLayout_34.addWidget(self.checkBoxEog)
        self.doubleSpinBoxEOGReject_3 = QtGui.QDoubleSpinBox(self.groupBoxRejection)
        self.doubleSpinBoxEOGReject_3.setEnabled(False)
        self.doubleSpinBoxEOGReject_3.setMinimum(-1.0)
        self.doubleSpinBoxEOGReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxEOGReject_3.setProperty("value", 250.0)
        self.doubleSpinBoxEOGReject_3.setObjectName(_fromUtf8("doubleSpinBoxEOGReject_3"))
        self.horizontalLayout_34.addWidget(self.doubleSpinBoxEOGReject_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_34)
        self.gridLayout_4.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
        self.groupBoxEpoch = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxEpoch.setGeometry(QtCore.QRect(12, 8, 331, 191))
        self.groupBoxEpoch.setObjectName(_fromUtf8("groupBoxEpoch"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBoxEpoch)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelCollectionName = QtGui.QLabel(self.groupBoxEpoch)
        self.labelCollectionName.setObjectName(_fromUtf8("labelCollectionName"))
        self.horizontalLayout.addWidget(self.labelCollectionName)
        self.lineEditCollectionName = QtGui.QLineEdit(self.groupBoxEpoch)
        self.lineEditCollectionName.setObjectName(_fromUtf8("lineEditCollectionName"))
        self.horizontalLayout.addWidget(self.lineEditCollectionName)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelTmin = QtGui.QLabel(self.groupBoxEpoch)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout_2.addWidget(self.labelTmin)
        self.doubleSpinBoxTmin = QtGui.QDoubleSpinBox(self.groupBoxEpoch)
        self.doubleSpinBoxTmin.setDecimals(3)
        self.doubleSpinBoxTmin.setMinimum(-10.0)
        self.doubleSpinBoxTmin.setSingleStep(0.1)
        self.doubleSpinBoxTmin.setProperty("value", -0.2)
        self.doubleSpinBoxTmin.setObjectName(_fromUtf8("doubleSpinBoxTmin"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxTmin)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelTmax = QtGui.QLabel(self.groupBoxEpoch)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_3.addWidget(self.labelTmax)
        self.doubleSpinBoxTmax = QtGui.QDoubleSpinBox(self.groupBoxEpoch)
        self.doubleSpinBoxTmax.setDecimals(3)
        self.doubleSpinBoxTmax.setMaximum(9.9)
        self.doubleSpinBoxTmax.setSingleStep(0.1)
        self.doubleSpinBoxTmax.setProperty("value", 0.5)
        self.doubleSpinBoxTmax.setObjectName(_fromUtf8("doubleSpinBoxTmax"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxTmax)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.checkBoxStim = QtGui.QCheckBox(self.groupBoxEpoch)
        self.checkBoxStim.setChecked(True)
        self.checkBoxStim.setObjectName(_fromUtf8("checkBoxStim"))
        self.verticalLayout_6.addWidget(self.checkBoxStim)
        self.gridLayout_6.addLayout(self.verticalLayout_6, 0, 0, 1, 1)
        self.groupBoxInterestingChannels = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxInterestingChannels.setGeometry(QtCore.QRect(10, 430, 321, 481))
        self.groupBoxInterestingChannels.setObjectName(_fromUtf8("groupBoxInterestingChannels"))
        self.listWidgetChannels = QtGui.QListWidget(self.groupBoxInterestingChannels)
        self.listWidgetChannels.setGeometry(QtCore.QRect(20, 30, 301, 451))
        self.listWidgetChannels.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetChannels.setObjectName(_fromUtf8("listWidgetChannels"))
        self.groupBox.raise_()
        self.widget.raise_()
        self.groupBoxEvent.raise_()
        self.groupBoxRejection.raise_()
        self.groupBoxEpoch.raise_()
        self.pushButtonFixedLength.raise_()
        self.groupBoxInterestingChannels.raise_()
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(EventSelectionDialog)
        QtCore.QObject.connect(self.pushButtonCompute, QtCore.SIGNAL(_fromUtf8("clicked()")), EventSelectionDialog.accept)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), EventSelectionDialog.reject)
        QtCore.QObject.connect(self.checkBoxGrad, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxGradReject_3.setEnabled)
        QtCore.QObject.connect(self.checkBoxMag, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxMagReject_3.setEnabled)
        QtCore.QObject.connect(self.checkBoxEeg, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxEEGReject_3.setEnabled)
        QtCore.QObject.connect(self.checkBoxEog, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxEOGReject_3.setEnabled)
        QtCore.QObject.connect(self.pushButtonComputeBatch, QtCore.SIGNAL(_fromUtf8("clicked()")), EventSelectionDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(EventSelectionDialog)
        EventSelectionDialog.setTabOrder(self.scrollArea, self.lineEditCollectionName)
        EventSelectionDialog.setTabOrder(self.lineEditCollectionName, self.doubleSpinBoxTmin)
        EventSelectionDialog.setTabOrder(self.doubleSpinBoxTmin, self.doubleSpinBoxTmax)
        EventSelectionDialog.setTabOrder(self.doubleSpinBoxTmax, self.checkBoxStim)
        EventSelectionDialog.setTabOrder(self.checkBoxStim, self.spinBoxEventID)
        EventSelectionDialog.setTabOrder(self.spinBoxEventID, self.spinBoxMask)
        EventSelectionDialog.setTabOrder(self.spinBoxMask, self.checkBoxGrad)
        EventSelectionDialog.setTabOrder(self.checkBoxGrad, self.doubleSpinBoxGradReject_3)
        EventSelectionDialog.setTabOrder(self.doubleSpinBoxGradReject_3, self.checkBoxMag)
        EventSelectionDialog.setTabOrder(self.checkBoxMag, self.doubleSpinBoxMagReject_3)
        EventSelectionDialog.setTabOrder(self.doubleSpinBoxMagReject_3, self.checkBoxEeg)
        EventSelectionDialog.setTabOrder(self.checkBoxEeg, self.doubleSpinBoxEEGReject_3)
        EventSelectionDialog.setTabOrder(self.doubleSpinBoxEEGReject_3, self.checkBoxEog)
        EventSelectionDialog.setTabOrder(self.checkBoxEog, self.doubleSpinBoxEOGReject_3)
        EventSelectionDialog.setTabOrder(self.doubleSpinBoxEOGReject_3, self.pushButtonCancel)
        EventSelectionDialog.setTabOrder(self.pushButtonCancel, self.pushButtonCompute)

    def retranslateUi(self, EventSelectionDialog):
        EventSelectionDialog.setWindowTitle(_translate("EventSelectionDialog", "Meggie - Epoch Creation", None))
        self.pushButtonCancel.setText(_translate("EventSelectionDialog", "Cancel", None))
        self.pushButtonComputeBatch.setText(_translate("EventSelectionDialog", "Batch epochs", None))
        self.pushButtonCompute.setText(_translate("EventSelectionDialog", "Create epochs", None))
        self.pushButtonFixedLength.setText(_translate("EventSelectionDialog", "Fixed length events...", None))
        self.groupBox.setTitle(_translate("EventSelectionDialog", "List of given <event ID>, <event name>", None))
        self.groupBoxEvent.setTitle(_translate("EventSelectionDialog", "Select events to include in epoch collection", None))
        self.labelStimChannel.setText(_translate("EventSelectionDialog", "Stimulus channel:", None))
        self.labelEventID.setText(_translate("EventSelectionDialog", "Event ID:", None))
        self.labelMask.setText(_translate("EventSelectionDialog", "Mask", None))
        self.spinBoxMask.setToolTip(_translate("EventSelectionDialog", "<html><head/><body><p>Mask bit used for finding events. For example, if mask is set to 1, first bit is ignored.</p></body></html>", None))
        self.pushButtonAdd.setText(_translate("EventSelectionDialog", "Add to list >>", None))
        self.groupBoxRejection.setTitle(_translate("EventSelectionDialog", "Rejection parameters", None))
        self.checkBoxGrad.setToolTip(_translate("EventSelectionDialog", "Include or exclude grad channels", None))
        self.checkBoxGrad.setText(_translate("EventSelectionDialog", "Grad", None))
        self.doubleSpinBoxGradReject_3.setSuffix(_translate("EventSelectionDialog", " fT/cm", None))
        self.checkBoxMag.setToolTip(_translate("EventSelectionDialog", "Include or exclude mag channels", None))
        self.checkBoxMag.setText(_translate("EventSelectionDialog", "Mag", None))
        self.doubleSpinBoxMagReject_3.setSuffix(_translate("EventSelectionDialog", " fT", None))
        self.checkBoxEeg.setToolTip(_translate("EventSelectionDialog", "Include or exclude eeg channels", None))
        self.checkBoxEeg.setText(_translate("EventSelectionDialog", "EEG", None))
        self.doubleSpinBoxEEGReject_3.setSuffix(_translate("EventSelectionDialog", " uV", None))
        self.checkBoxEog.setToolTip(_translate("EventSelectionDialog", "Include or exclude eog channels", None))
        self.checkBoxEog.setText(_translate("EventSelectionDialog", "EOG", None))
        self.doubleSpinBoxEOGReject_3.setSuffix(_translate("EventSelectionDialog", " uV", None))
        self.groupBoxEpoch.setTitle(_translate("EventSelectionDialog", "Epoch collection", None))
        self.labelCollectionName.setText(_translate("EventSelectionDialog", "Collection name:", None))
        self.lineEditCollectionName.setText(_translate("EventSelectionDialog", "Epochs", None))
        self.labelTmin.setText(_translate("EventSelectionDialog", "Start time:", None))
        self.doubleSpinBoxTmin.setSuffix(_translate("EventSelectionDialog", " s", None))
        self.labelTmax.setText(_translate("EventSelectionDialog", "End time:", None))
        self.doubleSpinBoxTmax.setSuffix(_translate("EventSelectionDialog", " s", None))
        self.checkBoxStim.setToolTip(_translate("EventSelectionDialog", "Include or exclude stim channels", None))
        self.checkBoxStim.setText(_translate("EventSelectionDialog", "Include stim channel in collection", None))
        self.groupBoxInterestingChannels.setTitle(_translate("EventSelectionDialog", "Select interesting channels", None))

