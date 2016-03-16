# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plotStcDialog.ui'
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

class Ui_PlotStcDialog(object):
    def setupUi(self, PlotStcDialog):
        PlotStcDialog.setObjectName(_fromUtf8("PlotStcDialog"))
        PlotStcDialog.resize(304, 206)
        self.gridLayout = QtGui.QGridLayout(PlotStcDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelHemi = QtGui.QLabel(PlotStcDialog)
        self.labelHemi.setObjectName(_fromUtf8("labelHemi"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelHemi)
        self.comboBoxHemi = QtGui.QComboBox(PlotStcDialog)
        self.comboBoxHemi.setObjectName(_fromUtf8("comboBoxHemi"))
        self.comboBoxHemi.addItem(_fromUtf8(""))
        self.comboBoxHemi.addItem(_fromUtf8(""))
        self.comboBoxHemi.addItem(_fromUtf8(""))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.comboBoxHemi)
        self.labelSurface = QtGui.QLabel(PlotStcDialog)
        self.labelSurface.setObjectName(_fromUtf8("labelSurface"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelSurface)
        self.comboBoxSurface = QtGui.QComboBox(PlotStcDialog)
        self.comboBoxSurface.setObjectName(_fromUtf8("comboBoxSurface"))
        self.comboBoxSurface.addItem(_fromUtf8(""))
        self.comboBoxSurface.addItem(_fromUtf8(""))
        self.comboBoxSurface.addItem(_fromUtf8(""))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.comboBoxSurface)
        self.labelSmooth = QtGui.QLabel(PlotStcDialog)
        self.labelSmooth.setObjectName(_fromUtf8("labelSmooth"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelSmooth)
        self.spinBoxSmooth = QtGui.QSpinBox(PlotStcDialog)
        self.spinBoxSmooth.setProperty("value", 10)
        self.spinBoxSmooth.setObjectName(_fromUtf8("spinBoxSmooth"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.spinBoxSmooth)
        self.labelAlpha = QtGui.QLabel(PlotStcDialog)
        self.labelAlpha.setObjectName(_fromUtf8("labelAlpha"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelAlpha)
        self.doubleSpinBoxAlpha = QtGui.QDoubleSpinBox(PlotStcDialog)
        self.doubleSpinBoxAlpha.setMaximum(1.0)
        self.doubleSpinBoxAlpha.setSingleStep(0.01)
        self.doubleSpinBoxAlpha.setProperty("value", 1.0)
        self.doubleSpinBoxAlpha.setObjectName(_fromUtf8("doubleSpinBoxAlpha"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.doubleSpinBoxAlpha)
        self.gridLayout.addLayout(self.formLayout, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PlotStcDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.labelStc = QtGui.QLabel(PlotStcDialog)
        self.labelStc.setText(_fromUtf8(""))
        self.labelStc.setObjectName(_fromUtf8("labelStc"))
        self.gridLayout.addWidget(self.labelStc, 0, 0, 1, 1)

        self.retranslateUi(PlotStcDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PlotStcDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PlotStcDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PlotStcDialog)

    def retranslateUi(self, PlotStcDialog):
        PlotStcDialog.setWindowTitle(_translate("PlotStcDialog", "Plot source estimate", None))
        self.labelHemi.setText(_translate("PlotStcDialog", "Hemisphere", None))
        self.comboBoxHemi.setItemText(0, _translate("PlotStcDialog", "both", None))
        self.comboBoxHemi.setItemText(1, _translate("PlotStcDialog", "lh", None))
        self.comboBoxHemi.setItemText(2, _translate("PlotStcDialog", "rh", None))
        self.labelSurface.setText(_translate("PlotStcDialog", "Surface", None))
        self.comboBoxSurface.setItemText(0, _translate("PlotStcDialog", "white", None))
        self.comboBoxSurface.setItemText(1, _translate("PlotStcDialog", "inflated", None))
        self.comboBoxSurface.setItemText(2, _translate("PlotStcDialog", "orig", None))
        self.labelSmooth.setText(_translate("PlotStcDialog", "SmoothingSteps", None))
        self.labelAlpha.setText(_translate("PlotStcDialog", "Alpha", None))

