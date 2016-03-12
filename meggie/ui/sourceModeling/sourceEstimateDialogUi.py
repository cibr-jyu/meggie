# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sourceEstimateDialog.ui'
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

class Ui_SourceEstimateDialog(object):
    def setupUi(self, SourceEstimateDialog):
        SourceEstimateDialog.setObjectName(_fromUtf8("SourceEstimateDialog"))
        SourceEstimateDialog.resize(400, 300)
        self.gridLayout = QtGui.QGridLayout(SourceEstimateDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(SourceEstimateDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.labelEvoked = QtGui.QLabel(SourceEstimateDialog)
        self.labelEvoked.setText(_fromUtf8(""))
        self.labelEvoked.setObjectName(_fromUtf8("labelEvoked"))
        self.gridLayout.addWidget(self.labelEvoked, 0, 0, 1, 1)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setContentsMargins(-1, -1, 0, -1)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelInverseOperator = QtGui.QLabel(SourceEstimateDialog)
        self.labelInverseOperator.setObjectName(_fromUtf8("labelInverseOperator"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelInverseOperator)
        self.comboBoxInverseOperator = QtGui.QComboBox(SourceEstimateDialog)
        self.comboBoxInverseOperator.setObjectName(_fromUtf8("comboBoxInverseOperator"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxInverseOperator)
        self.labelMethod = QtGui.QLabel(SourceEstimateDialog)
        self.labelMethod.setObjectName(_fromUtf8("labelMethod"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelMethod)
        self.comboBoxMethod = QtGui.QComboBox(SourceEstimateDialog)
        self.comboBoxMethod.setObjectName(_fromUtf8("comboBoxMethod"))
        self.comboBoxMethod.addItem(_fromUtf8(""))
        self.comboBoxMethod.addItem(_fromUtf8(""))
        self.comboBoxMethod.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxMethod)
        self.labelLambda = QtGui.QLabel(SourceEstimateDialog)
        self.labelLambda.setObjectName(_fromUtf8("labelLambda"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelLambda)
        self.doubleSpinBoxLambda = QtGui.QDoubleSpinBox(SourceEstimateDialog)
        self.doubleSpinBoxLambda.setDecimals(6)
        self.doubleSpinBoxLambda.setMinimum(0.001)
        self.doubleSpinBoxLambda.setSingleStep(0.1)
        self.doubleSpinBoxLambda.setProperty("value", 0.111111)
        self.doubleSpinBoxLambda.setObjectName(_fromUtf8("doubleSpinBoxLambda"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxLambda)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)

        self.retranslateUi(SourceEstimateDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SourceEstimateDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SourceEstimateDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(SourceEstimateDialog)

    def retranslateUi(self, SourceEstimateDialog):
        SourceEstimateDialog.setWindowTitle(_translate("SourceEstimateDialog", "Source estimate", None))
        self.labelInverseOperator.setText(_translate("SourceEstimateDialog", "Inverse operator", None))
        self.labelMethod.setText(_translate("SourceEstimateDialog", "Method", None))
        self.comboBoxMethod.setItemText(0, _translate("SourceEstimateDialog", "MNE", None))
        self.comboBoxMethod.setItemText(1, _translate("SourceEstimateDialog", "dSPM", None))
        self.comboBoxMethod.setItemText(2, _translate("SourceEstimateDialog", "sLORETA", None))
        self.labelLambda.setText(_translate("SourceEstimateDialog", "Regularization parameter (lambda):", None))

