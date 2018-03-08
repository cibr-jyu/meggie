# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'covarianceEpochDialogUi.ui'
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

class Ui_covarianceEpochDialog(object):
    def setupUi(self, covarianceEpochDialog):
        covarianceEpochDialog.setObjectName(_fromUtf8("covarianceEpochDialog"))
        covarianceEpochDialog.resize(397, 320)
        self.gridLayout = QtGui.QGridLayout(covarianceEpochDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(covarianceEpochDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBoxName = QtGui.QGroupBox(covarianceEpochDialog)
        self.groupBoxName.setObjectName(_fromUtf8("groupBoxName"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxName)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelName = QtGui.QLabel(self.groupBoxName)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_3.addWidget(self.labelName)
        self.lineEditName = QtGui.QLineEdit(self.groupBoxName)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_3.addWidget(self.lineEditName)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBoxName)
        self.groupBoxEpochs = QtGui.QGroupBox(covarianceEpochDialog)
        self.groupBoxEpochs.setObjectName(_fromUtf8("groupBoxEpochs"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxEpochs)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.listWidgetEpochs = QtGui.QListWidget(self.groupBoxEpochs)
        self.listWidgetEpochs.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetEpochs.setObjectName(_fromUtf8("listWidgetEpochs"))
        self.gridLayout_2.addWidget(self.listWidgetEpochs, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBoxEpochs)
        self.groupBoxParams = QtGui.QGroupBox(covarianceEpochDialog)
        self.groupBoxParams.setObjectName(_fromUtf8("groupBoxParams"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxParams)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.groupBoxParams)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        self.doubleSpinBoxTmin = QtGui.QDoubleSpinBox(self.groupBoxParams)
        self.doubleSpinBoxTmin.setMinimum(-1000000000.0)
        self.doubleSpinBoxTmin.setMaximum(1000000000.0)
        self.doubleSpinBoxTmin.setSingleStep(0.1)
        self.doubleSpinBoxTmin.setObjectName(_fromUtf8("doubleSpinBoxTmin"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxTmin)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelTmax = QtGui.QLabel(self.groupBoxParams)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_2.addWidget(self.labelTmax)
        self.doubleSpinBoxTmax = QtGui.QDoubleSpinBox(self.groupBoxParams)
        self.doubleSpinBoxTmax.setMinimum(-1000000000.0)
        self.doubleSpinBoxTmax.setMaximum(1000000000.0)
        self.doubleSpinBoxTmax.setSingleStep(0.1)
        self.doubleSpinBoxTmax.setObjectName(_fromUtf8("doubleSpinBoxTmax"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxTmax)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.gridLayout_3.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBoxParams)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)

        self.retranslateUi(covarianceEpochDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), covarianceEpochDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), covarianceEpochDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(covarianceEpochDialog)

    def retranslateUi(self, covarianceEpochDialog):
        covarianceEpochDialog.setWindowTitle(_translate("covarianceEpochDialog", "Compute covariance from epoch file", None))
        self.groupBoxName.setTitle(_translate("covarianceEpochDialog", "General:", None))
        self.labelName.setText(_translate("covarianceEpochDialog", "Name:", None))
        self.groupBoxEpochs.setTitle(_translate("covarianceEpochDialog", "Select epochs for computation:", None))
        self.groupBoxParams.setTitle(_translate("covarianceEpochDialog", "Set parameters:", None))
        self.labelTmin.setText(_translate("covarianceEpochDialog", "Start time:", None))
        self.doubleSpinBoxTmin.setSuffix(_translate("covarianceEpochDialog", " s", None))
        self.labelTmax.setText(_translate("covarianceEpochDialog", "End time:", None))
        self.doubleSpinBoxTmax.setSuffix(_translate("covarianceEpochDialog", " s", None))

