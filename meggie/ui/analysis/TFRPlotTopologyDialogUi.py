# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TFRPlotTopologyDialogUi.ui'
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

class Ui_TFRPlotTopologyDialog(object):
    def setupUi(self, TFRPlotTopologyDialog):
        TFRPlotTopologyDialog.setObjectName(_fromUtf8("TFRPlotTopologyDialog"))
        TFRPlotTopologyDialog.resize(556, 300)
        self.gridLayout_2 = QtGui.QGridLayout(TFRPlotTopologyDialog)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(TFRPlotTopologyDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.gridLayout_2.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(TFRPlotTopologyDialog)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 538, 241))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_4 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBoxPreferences = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxPreferences.setObjectName(_fromUtf8("groupBoxPreferences"))
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBoxPreferences)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelBaselineMode = QtGui.QLabel(self.groupBoxPreferences)
        self.labelBaselineMode.setObjectName(_fromUtf8("labelBaselineMode"))
        self.horizontalLayout_2.addWidget(self.labelBaselineMode)
        self.comboBoxBaselineMode = QtGui.QComboBox(self.groupBoxPreferences)
        self.comboBoxBaselineMode.setObjectName(_fromUtf8("comboBoxBaselineMode"))
        self.comboBoxBaselineMode.addItem(_fromUtf8(""))
        self.comboBoxBaselineMode.addItem(_fromUtf8(""))
        self.comboBoxBaselineMode.addItem(_fromUtf8(""))
        self.comboBoxBaselineMode.addItem(_fromUtf8(""))
        self.comboBoxBaselineMode.addItem(_fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.comboBoxBaselineMode)
        self.gridLayout_9.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelBaselineCorrection = QtGui.QLabel(self.groupBoxPreferences)
        self.labelBaselineCorrection.setObjectName(_fromUtf8("labelBaselineCorrection"))
        self.horizontalLayout.addWidget(self.labelBaselineCorrection)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.checkBoxBaselineCorrection = QtGui.QCheckBox(self.groupBoxPreferences)
        self.checkBoxBaselineCorrection.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBoxBaselineCorrection.setText(_fromUtf8(""))
        self.checkBoxBaselineCorrection.setChecked(True)
        self.checkBoxBaselineCorrection.setObjectName(_fromUtf8("checkBoxBaselineCorrection"))
        self.horizontalLayout.addWidget(self.checkBoxBaselineCorrection)
        self.gridLayout_9.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelBaselineStart = QtGui.QLabel(self.groupBoxPreferences)
        self.labelBaselineStart.setObjectName(_fromUtf8("labelBaselineStart"))
        self.horizontalLayout_3.addWidget(self.labelBaselineStart)
        self.doubleSpinBoxBaselineStart = QtGui.QDoubleSpinBox(self.groupBoxPreferences)
        self.doubleSpinBoxBaselineStart.setObjectName(_fromUtf8("doubleSpinBoxBaselineStart"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxBaselineStart)
        self.gridLayout_9.addLayout(self.horizontalLayout_3, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelBaselineEnd = QtGui.QLabel(self.groupBoxPreferences)
        self.labelBaselineEnd.setObjectName(_fromUtf8("labelBaselineEnd"))
        self.horizontalLayout_4.addWidget(self.labelBaselineEnd)
        self.doubleSpinBoxBaselineEnd = QtGui.QDoubleSpinBox(self.groupBoxPreferences)
        self.doubleSpinBoxBaselineEnd.setObjectName(_fromUtf8("doubleSpinBoxBaselineEnd"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxBaselineEnd)
        self.gridLayout_9.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBoxPreferences, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_2.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(TFRPlotTopologyDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TFRPlotTopologyDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TFRPlotTopologyDialog.reject)
        QtCore.QObject.connect(self.checkBoxBaselineCorrection, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.comboBoxBaselineMode.setEnabled)
        QtCore.QObject.connect(self.checkBoxBaselineCorrection, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxBaselineStart.setEnabled)
        QtCore.QObject.connect(self.checkBoxBaselineCorrection, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.doubleSpinBoxBaselineEnd.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(TFRPlotTopologyDialog)
        TFRPlotTopologyDialog.setTabOrder(self.scrollArea, self.buttonBox)

    def retranslateUi(self, TFRPlotTopologyDialog):
        TFRPlotTopologyDialog.setWindowTitle(_translate("TFRPlotTopologyDialog", "Meggie - Compute TFR", None))
        self.groupBoxPreferences.setTitle(_translate("TFRPlotTopologyDialog", "Preferences", None))
        self.labelBaselineMode.setText(_translate("TFRPlotTopologyDialog", "Baseline mode:", None))
        self.comboBoxBaselineMode.setItemText(0, _translate("TFRPlotTopologyDialog", "logratio", None))
        self.comboBoxBaselineMode.setItemText(1, _translate("TFRPlotTopologyDialog", "ratio", None))
        self.comboBoxBaselineMode.setItemText(2, _translate("TFRPlotTopologyDialog", "percent", None))
        self.comboBoxBaselineMode.setItemText(3, _translate("TFRPlotTopologyDialog", "mean", None))
        self.comboBoxBaselineMode.setItemText(4, _translate("TFRPlotTopologyDialog", "zscore", None))
        self.labelBaselineCorrection.setText(_translate("TFRPlotTopologyDialog", "Baseline correction:", None))
        self.labelBaselineStart.setText(_translate("TFRPlotTopologyDialog", "Start:", None))
        self.labelBaselineEnd.setText(_translate("TFRPlotTopologyDialog", "End:", None))

