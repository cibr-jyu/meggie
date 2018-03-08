# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stcPlotDialogUi.ui'
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

class Ui_stcPlotDialog(object):
    def setupUi(self, stcPlotDialog):
        stcPlotDialog.setObjectName(_fromUtf8("stcPlotDialog"))
        stcPlotDialog.resize(496, 337)
        self.gridLayout_7 = QtGui.QGridLayout(stcPlotDialog)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.buttonBox = QtGui.QDialogButtonBox(stcPlotDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_7.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.groupBoxSource = QtGui.QGroupBox(stcPlotDialog)
        self.groupBoxSource.setEnabled(False)
        self.groupBoxSource.setObjectName(_fromUtf8("groupBoxSource"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBoxSource)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelSource = QtGui.QLabel(self.groupBoxSource)
        self.labelSource.setObjectName(_fromUtf8("labelSource"))
        self.horizontalLayout.addWidget(self.labelSource)
        self.comboBoxSource = QtGui.QComboBox(self.groupBoxSource)
        self.comboBoxSource.setObjectName(_fromUtf8("comboBoxSource"))
        self.horizontalLayout.addWidget(self.comboBoxSource)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_6.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxSource, 0, 0, 1, 1)
        self.groupBoxTimeParameters = QtGui.QGroupBox(stcPlotDialog)
        self.groupBoxTimeParameters.setObjectName(_fromUtf8("groupBoxTimeParameters"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxTimeParameters)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.radioButtonInitialTime = QtGui.QRadioButton(self.groupBoxTimeParameters)
        self.radioButtonInitialTime.setChecked(True)
        self.radioButtonInitialTime.setObjectName(_fromUtf8("radioButtonInitialTime"))
        self.horizontalLayout_2.addWidget(self.radioButtonInitialTime)
        self.doubleSpinBoxInitialTime = QtGui.QDoubleSpinBox(self.groupBoxTimeParameters)
        self.doubleSpinBoxInitialTime.setObjectName(_fromUtf8("doubleSpinBoxInitialTime"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxInitialTime)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.radioButtonPeak = QtGui.QRadioButton(self.groupBoxTimeParameters)
        self.radioButtonPeak.setObjectName(_fromUtf8("radioButtonPeak"))
        self.horizontalLayout_3.addWidget(self.radioButtonPeak)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxTimeParameters, 1, 0, 1, 1)

        self.retranslateUi(stcPlotDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), stcPlotDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), stcPlotDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(stcPlotDialog)

    def retranslateUi(self, stcPlotDialog):
        stcPlotDialog.setWindowTitle(_translate("stcPlotDialog", "Plot source estimate", None))
        self.groupBoxSource.setTitle(_translate("stcPlotDialog", "Source:", None))
        self.labelSource.setText(_translate("stcPlotDialog", "Source epochs / evoked:", None))
        self.groupBoxTimeParameters.setTitle(_translate("stcPlotDialog", "Time parameters:", None))
        self.radioButtonInitialTime.setText(_translate("stcPlotDialog", "Initial time:", None))
        self.doubleSpinBoxInitialTime.setSuffix(_translate("stcPlotDialog", " s", None))
        self.radioButtonPeak.setText(_translate("stcPlotDialog", "Use the peak value as initial time", None))

