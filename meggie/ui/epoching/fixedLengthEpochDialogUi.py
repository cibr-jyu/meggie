# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fixedLengthEpochsDialogUi.ui'
#
# Created: Thu Mar 24 22:11:32 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_FixedLengthEpochDialog(object):
    def setupUi(self, FixedLengthEpochDialog):
        FixedLengthEpochDialog.setObjectName(_fromUtf8("FixedLengthEpochDialog"))
        FixedLengthEpochDialog.resize(247, 165)
        self.gridLayout = QtGui.QGridLayout(FixedLengthEpochDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelStart = QtGui.QLabel(FixedLengthEpochDialog)
        self.labelStart.setObjectName(_fromUtf8("labelStart"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelStart)
        self.spinBoxStart = QtGui.QSpinBox(FixedLengthEpochDialog)
        self.spinBoxStart.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxStart.setObjectName(_fromUtf8("spinBoxStart"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.spinBoxStart)
        self.labelEnd = QtGui.QLabel(FixedLengthEpochDialog)
        self.labelEnd.setObjectName(_fromUtf8("labelEnd"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelEnd)
        self.spinBoxEnd = QtGui.QSpinBox(FixedLengthEpochDialog)
        self.spinBoxEnd.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinBoxEnd.setObjectName(_fromUtf8("spinBoxEnd"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.spinBoxEnd)
        self.labelInterval = QtGui.QLabel(FixedLengthEpochDialog)
        self.labelInterval.setObjectName(_fromUtf8("labelInterval"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelInterval)
        self.doubleSpinBoxInterval = QtGui.QDoubleSpinBox(FixedLengthEpochDialog)
        self.doubleSpinBoxInterval.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBoxInterval.setDecimals(3)
        self.doubleSpinBoxInterval.setProperty("value", 0.5)
        self.doubleSpinBoxInterval.setObjectName(_fromUtf8("doubleSpinBoxInterval"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxInterval)
        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(FixedLengthEpochDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(FixedLengthEpochDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FixedLengthEpochDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FixedLengthEpochDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(FixedLengthEpochDialog)
        FixedLengthEpochDialog.setTabOrder(self.spinBoxStart, self.spinBoxEnd)
        FixedLengthEpochDialog.setTabOrder(self.spinBoxEnd, self.doubleSpinBoxInterval)
        FixedLengthEpochDialog.setTabOrder(self.doubleSpinBoxInterval, self.buttonBox)

    def retranslateUi(self, FixedLengthEpochDialog):
        FixedLengthEpochDialog.setWindowTitle(_translate("FixedLengthEpochDialog", "Construct fixed length events", None))
        self.labelStart.setText(_translate("FixedLengthEpochDialog", "Start", None))
        self.spinBoxStart.setSuffix(_translate("FixedLengthEpochDialog", "s", None))
        self.labelEnd.setText(_translate("FixedLengthEpochDialog", "End", None))
        self.spinBoxEnd.setSuffix(_translate("FixedLengthEpochDialog", "s", None))
        self.labelInterval.setText(_translate("FixedLengthEpochDialog", "Interval", None))
        self.doubleSpinBoxInterval.setSuffix(_translate("FixedLengthEpochDialog", "s", None))

