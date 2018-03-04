# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inverseOperatorDialogUi.ui'
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

class Ui_inverseOperatorDialog(object):
    def setupUi(self, inverseOperatorDialog):
        inverseOperatorDialog.setObjectName(_fromUtf8("inverseOperatorDialog"))
        inverseOperatorDialog.resize(572, 215)
        inverseOperatorDialog.setModal(True)
        self.formLayout_3 = QtGui.QFormLayout(inverseOperatorDialog)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.labelInverseOperatorName = QtGui.QLabel(inverseOperatorDialog)
        self.labelInverseOperatorName.setObjectName(_fromUtf8("labelInverseOperatorName"))
        self.horizontalLayout_6.addWidget(self.labelInverseOperatorName)
        self.lineEditInverseOperatorName = QtGui.QLineEdit(inverseOperatorDialog)
        self.lineEditInverseOperatorName.setObjectName(_fromUtf8("lineEditInverseOperatorName"))
        self.horizontalLayout_6.addWidget(self.lineEditInverseOperatorName)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelIBasedOn = QtGui.QLabel(inverseOperatorDialog)
        self.labelIBasedOn.setObjectName(_fromUtf8("labelIBasedOn"))
        self.horizontalLayout.addWidget(self.labelIBasedOn)
        self.lineEditBasedOn = QtGui.QLineEdit(inverseOperatorDialog)
        self.lineEditBasedOn.setEnabled(False)
        self.lineEditBasedOn.setObjectName(_fromUtf8("lineEditBasedOn"))
        self.horizontalLayout.addWidget(self.lineEditBasedOn)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout_3.setLayout(0, QtGui.QFormLayout.SpanningRole, self.verticalLayout)
        self.groupBoxInverseOperatorParameters = QtGui.QGroupBox(inverseOperatorDialog)
        self.groupBoxInverseOperatorParameters.setObjectName(_fromUtf8("groupBoxInverseOperatorParameters"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxInverseOperatorParameters)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelLoose = QtGui.QLabel(self.groupBoxInverseOperatorParameters)
        self.labelLoose.setObjectName(_fromUtf8("labelLoose"))
        self.horizontalLayout_2.addWidget(self.labelLoose)
        self.doubleSpinBoxLoose = QtGui.QDoubleSpinBox(self.groupBoxInverseOperatorParameters)
        self.doubleSpinBoxLoose.setMaximum(1.0)
        self.doubleSpinBoxLoose.setSingleStep(0.05)
        self.doubleSpinBoxLoose.setProperty("value", 0.2)
        self.doubleSpinBoxLoose.setObjectName(_fromUtf8("doubleSpinBoxLoose"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxLoose)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelDepth = QtGui.QLabel(self.groupBoxInverseOperatorParameters)
        self.labelDepth.setObjectName(_fromUtf8("labelDepth"))
        self.horizontalLayout_3.addWidget(self.labelDepth)
        self.doubleSpinBoxDepth = QtGui.QDoubleSpinBox(self.groupBoxInverseOperatorParameters)
        self.doubleSpinBoxDepth.setMaximum(1.0)
        self.doubleSpinBoxDepth.setSingleStep(0.05)
        self.doubleSpinBoxDepth.setProperty("value", 0.8)
        self.doubleSpinBoxDepth.setObjectName(_fromUtf8("doubleSpinBoxDepth"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxDepth)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBoxInverseOperatorParameters)
        self.buttonBox = QtGui.QDialogButtonBox(inverseOperatorDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.SpanningRole, self.buttonBox)

        self.retranslateUi(inverseOperatorDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), inverseOperatorDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), inverseOperatorDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(inverseOperatorDialog)

    def retranslateUi(self, inverseOperatorDialog):
        inverseOperatorDialog.setWindowTitle(_translate("inverseOperatorDialog", "Create new inverse operator", None))
        self.labelInverseOperatorName.setText(_translate("inverseOperatorDialog", "Inverse operator name:     ", None))
        self.labelIBasedOn.setText(_translate("inverseOperatorDialog", "Based on forward solution:", None))
        self.groupBoxInverseOperatorParameters.setTitle(_translate("inverseOperatorDialog", "Inverse operator parameters:", None))
        self.labelLoose.setText(_translate("inverseOperatorDialog", "Loose:", None))
        self.labelDepth.setText(_translate("inverseOperatorDialog", "Depth:", None))

