# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eegParametersDialogUi.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(620, 659)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem)
        self.pushButtonCancel = QtGui.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout_19.addWidget(self.pushButtonCancel)
        self.pushButtonCompute = QtGui.QPushButton(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCompute.sizePolicy().hasHeightForWidth())
        self.pushButtonCompute.setSizePolicy(sizePolicy)
        self.pushButtonCompute.setObjectName(_fromUtf8("pushButtonCompute"))
        self.horizontalLayout_19.addWidget(self.pushButtonCompute)
        self.gridLayout.addLayout(self.horizontalLayout_19, 1, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 602, 602))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.groupBoxEvents = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxEvents.setGeometry(QtCore.QRect(0, 0, 231, 361))
        self.groupBoxEvents.setObjectName(_fromUtf8("groupBoxEvents"))
        self.layoutWidget_2 = QtGui.QWidget(self.groupBoxEvents)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 30, 221, 231))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelEventID = QtGui.QLabel(self.layoutWidget_2)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_7.addWidget(self.labelEventID)
        self.labelBlinkId = QtGui.QLabel(self.layoutWidget_2)
        self.labelBlinkId.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.labelBlinkId.setObjectName(_fromUtf8("labelBlinkId"))
        self.horizontalLayout_7.addWidget(self.labelBlinkId)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelChannel = QtGui.QLabel(self.layoutWidget_2)
        self.labelChannel.setObjectName(_fromUtf8("labelChannel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelChannel)
        self.comboBoxChannelSelect = QtGui.QComboBox(self.layoutWidget_2)
        self.comboBoxChannelSelect.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBoxChannelSelect.setObjectName(_fromUtf8("comboBoxChannelSelect"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxChannelSelect)
        self.labelLowPass = QtGui.QLabel(self.layoutWidget_2)
        self.labelLowPass.setObjectName(_fromUtf8("labelLowPass"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelLowPass)
        self.doubleSpinBoxLowPass = QtGui.QDoubleSpinBox(self.layoutWidget_2)
        self.doubleSpinBoxLowPass.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBoxLowPass.setProperty("value", 1.0)
        self.doubleSpinBoxLowPass.setObjectName(_fromUtf8("doubleSpinBoxLowPass"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxLowPass)
        self.labelHighPass = QtGui.QLabel(self.layoutWidget_2)
        self.labelHighPass.setObjectName(_fromUtf8("labelHighPass"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelHighPass)
        self.doubleSpinBoxHighPass = QtGui.QDoubleSpinBox(self.layoutWidget_2)
        self.doubleSpinBoxHighPass.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBoxHighPass.setSingleStep(1.0)
        self.doubleSpinBoxHighPass.setProperty("value", 10.0)
        self.doubleSpinBoxHighPass.setObjectName(_fromUtf8("doubleSpinBoxHighPass"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxHighPass)
        self.labelFilterLength = QtGui.QLabel(self.layoutWidget_2)
        self.labelFilterLength.setObjectName(_fromUtf8("labelFilterLength"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelFilterLength)
        self.spinBoxFilterLength = QtGui.QSpinBox(self.layoutWidget_2)
        self.spinBoxFilterLength.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxFilterLength.setProperty("value", 10)
        self.spinBoxFilterLength.setObjectName(_fromUtf8("spinBoxFilterLength"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.spinBoxFilterLength)
        self.labelStart = QtGui.QLabel(self.layoutWidget_2)
        self.labelStart.setObjectName(_fromUtf8("labelStart"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.labelStart)
        self.doubleSpinBoxStart = QtGui.QDoubleSpinBox(self.layoutWidget_2)
        self.doubleSpinBoxStart.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBoxStart.setProperty("value", 5.0)
        self.doubleSpinBoxStart.setObjectName(_fromUtf8("doubleSpinBoxStart"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxStart)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBoxEvents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 270, 221, 91))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonAdd = QtGui.QPushButton(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAdd.sizePolicy().hasHeightForWidth())
        self.pushButtonAdd.setSizePolicy(sizePolicy)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.verticalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.verticalLayout.addWidget(self.pushButtonRemove)
        self.tableWidgetEvents = QtGui.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidgetEvents.setGeometry(QtCore.QRect(240, 30, 361, 331))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidgetEvents.sizePolicy().hasHeightForWidth())
        self.tableWidgetEvents.setSizePolicy(sizePolicy)
        self.tableWidgetEvents.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableWidgetEvents.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableWidgetEvents.setObjectName(_fromUtf8("tableWidgetEvents"))
        self.tableWidgetEvents.setColumnCount(0)
        self.tableWidgetEvents.setRowCount(0)
        self.groupBoxProjection = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxProjection.setGeometry(QtCore.QRect(0, 370, 621, 151))
        self.groupBoxProjection.setObjectName(_fromUtf8("groupBoxProjection"))
        self.gridLayoutWidget = QtGui.QWidget(self.groupBoxProjection)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 30, 601, 113))
        self.gridLayoutWidget.setObjectName(_fromUtf8("gridLayoutWidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelTmin = QtGui.QLabel(self.gridLayoutWidget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.gridLayout_2.addWidget(self.labelTmin, 0, 0, 1, 1)
        self.spinBoxVectors = QtGui.QSpinBox(self.gridLayoutWidget)
        self.spinBoxVectors.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxVectors.setMinimum(1)
        self.spinBoxVectors.setProperty("value", 2)
        self.spinBoxVectors.setObjectName(_fromUtf8("spinBoxVectors"))
        self.gridLayout_2.addWidget(self.spinBoxVectors, 2, 1, 1, 1)
        self.labelTmax = QtGui.QLabel(self.gridLayoutWidget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.gridLayout_2.addWidget(self.labelTmax, 1, 0, 1, 1)
        self.doubleSpinBoxTmax = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBoxTmax.setDecimals(3)
        self.doubleSpinBoxTmax.setMaximum(9.9)
        self.doubleSpinBoxTmax.setSingleStep(0.1)
        self.doubleSpinBoxTmax.setProperty("value", 0.5)
        self.doubleSpinBoxTmax.setObjectName(_fromUtf8("doubleSpinBoxTmax"))
        self.gridLayout_2.addWidget(self.doubleSpinBoxTmax, 1, 1, 1, 1)
        self.doubleSpinBoxTmin = QtGui.QDoubleSpinBox(self.gridLayoutWidget)
        self.doubleSpinBoxTmin.setDecimals(3)
        self.doubleSpinBoxTmin.setMinimum(-10.0)
        self.doubleSpinBoxTmin.setSingleStep(0.1)
        self.doubleSpinBoxTmin.setProperty("value", -0.2)
        self.doubleSpinBoxTmin.setObjectName(_fromUtf8("doubleSpinBoxTmin"))
        self.gridLayout_2.addWidget(self.doubleSpinBoxTmin, 0, 1, 1, 1)
        self.labelVectors = QtGui.QLabel(self.gridLayoutWidget)
        self.labelVectors.setScaledContents(False)
        self.labelVectors.setObjectName(_fromUtf8("labelVectors"))
        self.gridLayout_2.addWidget(self.labelVectors, 2, 0, 1, 1)
        self.verticalLayoutWidget_2 = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(0, 520, 291, 71))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.pushButtonShowEvents = QtGui.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonShowEvents.sizePolicy().hasHeightForWidth())
        self.pushButtonShowEvents.setSizePolicy(sizePolicy)
        self.pushButtonShowEvents.setObjectName(_fromUtf8("pushButtonShowEvents"))
        self.verticalLayout_2.addWidget(self.pushButtonShowEvents)
        self.pushButtonPlotEpochs = QtGui.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonPlotEpochs.sizePolicy().hasHeightForWidth())
        self.pushButtonPlotEpochs.setSizePolicy(sizePolicy)
        self.pushButtonPlotEpochs.setObjectName(_fromUtf8("pushButtonPlotEpochs"))
        self.verticalLayout_2.addWidget(self.pushButtonPlotEpochs)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QObject.connect(self.pushButtonCompute, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel", None))
        self.pushButtonCompute.setText(_translate("Dialog", "Compute", None))
        self.groupBoxEvents.setTitle(_translate("Dialog", "Find EOG events", None))
        self.labelEventID.setToolTip(_translate("Dialog", "The index to assign to found events.", None))
        self.labelEventID.setText(_translate("Dialog", "Event ID for blinks:", None))
        self.labelBlinkId.setText(_translate("Dialog", "998", None))
        self.labelChannel.setToolTip(_translate("Dialog", "Select specified channel for finding EOG artefacts. Preferably a channel with clear blinks.", None))
        self.labelChannel.setText(_translate("Dialog", "Event channel:", None))
        self.comboBoxChannelSelect.setToolTip(_translate("Dialog", "Select specified channel for finding EOG artefacts. Preferably a channel with clear blinks.", None))
        self.labelLowPass.setToolTip(_translate("Dialog", "Low pass filter frequency.", None))
        self.labelLowPass.setText(_translate("Dialog", "Low pass:", None))
        self.doubleSpinBoxLowPass.setToolTip(_translate("Dialog", "Low pass filter frequency.", None))
        self.doubleSpinBoxLowPass.setSuffix(_translate("Dialog", "Hz", None))
        self.labelHighPass.setToolTip(_translate("Dialog", "High pass filter frequency.", None))
        self.labelHighPass.setText(_translate("Dialog", "High pass:", None))
        self.doubleSpinBoxHighPass.setToolTip(_translate("Dialog", "High pass filter frequency.", None))
        self.doubleSpinBoxHighPass.setSuffix(_translate("Dialog", "Hz", None))
        self.labelFilterLength.setToolTip(_translate("Dialog", "Sets the number of taps used for filtering.", None))
        self.labelFilterLength.setText(_translate("Dialog", "Filter length:", None))
        self.spinBoxFilterLength.setToolTip(_translate("Dialog", "Sets the number of taps used for filtering.", None))
        self.spinBoxFilterLength.setSuffix(_translate("Dialog", "s", None))
        self.labelStart.setToolTip(_translate("Dialog", "Set starting time for blink detection.", None))
        self.labelStart.setText(_translate("Dialog", "Start time:", None))
        self.doubleSpinBoxStart.setToolTip(_translate("Dialog", "Set starting time for blink detection.", None))
        self.doubleSpinBoxStart.setSuffix(_translate("Dialog", "s", None))
        self.pushButtonAdd.setToolTip(_translate("Dialog", "Start blink detection. The previous event list will be deleted!", None))
        self.pushButtonAdd.setText(_translate("Dialog", "Add to list >>", None))
        self.pushButtonRemove.setText(_translate("Dialog", "Remove <<", None))
        self.tableWidgetEvents.setToolTip(_translate("Dialog", "Found events.", None))
        self.groupBoxProjection.setTitle(_translate("Dialog", "Projection parameters", None))
        self.labelTmin.setText(_translate("Dialog", "Start time:", None))
        self.spinBoxVectors.setToolTip(_translate("Dialog", "Number of projections calculated for events. Try increasing this if the artefact is not completely removed.", None))
        self.labelTmax.setText(_translate("Dialog", "End time:", None))
        self.doubleSpinBoxTmax.setSuffix(_translate("Dialog", " s", None))
        self.doubleSpinBoxTmin.setSuffix(_translate("Dialog", " s", None))
        self.labelVectors.setToolTip(_translate("Dialog", "Number of projections calculated for events. Try increasing this if the artefact is not completely removed.", None))
        self.labelVectors.setText(_translate("Dialog", "Number of projection vectors for EEG channels:", None))
        self.pushButtonShowEvents.setText(_translate("Dialog", "Show event locations", None))
        self.pushButtonPlotEpochs.setText(_translate("Dialog", "Plot average epochs", None))

