# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'covarianceRawDialogUi.ui'
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

class Ui_covarianceRawDialog(object):
    def setupUi(self, covarianceRawDialog):
        covarianceRawDialog.setObjectName(_fromUtf8("covarianceRawDialog"))
        covarianceRawDialog.resize(496, 373)
        self.gridLayout_7 = QtGui.QGridLayout(covarianceRawDialog)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.groupBoxSource = QtGui.QGroupBox(covarianceRawDialog)
        self.groupBoxSource.setObjectName(_fromUtf8("groupBoxSource"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBoxSource)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.radioButtonCurrentSubject = QtGui.QRadioButton(self.groupBoxSource)
        self.radioButtonCurrentSubject.setChecked(True)
        self.radioButtonCurrentSubject.setObjectName(_fromUtf8("radioButtonCurrentSubject"))
        self.buttonGroupRawFile = QtGui.QButtonGroup(covarianceRawDialog)
        self.buttonGroupRawFile.setObjectName(_fromUtf8("buttonGroupRawFile"))
        self.buttonGroupRawFile.addButton(self.radioButtonCurrentSubject)
        self.horizontalLayout_5.addWidget(self.radioButtonCurrentSubject)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButtonElsewhere = QtGui.QRadioButton(self.groupBoxSource)
        self.radioButtonElsewhere.setObjectName(_fromUtf8("radioButtonElsewhere"))
        self.buttonGroupRawFile.addButton(self.radioButtonElsewhere)
        self.horizontalLayout.addWidget(self.radioButtonElsewhere)
        self.lineEditRawFile = QtGui.QLineEdit(self.groupBoxSource)
        self.lineEditRawFile.setEnabled(False)
        self.lineEditRawFile.setObjectName(_fromUtf8("lineEditRawFile"))
        self.horizontalLayout.addWidget(self.lineEditRawFile)
        self.pushButtonBrowse = QtGui.QPushButton(self.groupBoxSource)
        self.pushButtonBrowse.setEnabled(False)
        self.pushButtonBrowse.setObjectName(_fromUtf8("pushButtonBrowse"))
        self.horizontalLayout.addWidget(self.pushButtonBrowse)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout_6.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxSource, 0, 0, 1, 1)
        self.groupBoxStartEnd = QtGui.QGroupBox(covarianceRawDialog)
        self.groupBoxStartEnd.setObjectName(_fromUtf8("groupBoxStartEnd"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxStartEnd)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.labelBeginTime = QtGui.QLabel(self.groupBoxStartEnd)
        self.labelBeginTime.setObjectName(_fromUtf8("labelBeginTime"))
        self.gridLayout_4.addWidget(self.labelBeginTime, 0, 0, 1, 1)
        self.doubleSpinBoxStartTime = QtGui.QDoubleSpinBox(self.groupBoxStartEnd)
        self.doubleSpinBoxStartTime.setPrefix(_fromUtf8(""))
        self.doubleSpinBoxStartTime.setObjectName(_fromUtf8("doubleSpinBoxStartTime"))
        self.gridLayout_4.addWidget(self.doubleSpinBoxStartTime, 0, 1, 1, 1)
        self.labelEndTime = QtGui.QLabel(self.groupBoxStartEnd)
        self.labelEndTime.setObjectName(_fromUtf8("labelEndTime"))
        self.gridLayout_4.addWidget(self.labelEndTime, 1, 0, 1, 1)
        self.doubleSpinBoxEndTime = QtGui.QDoubleSpinBox(self.groupBoxStartEnd)
        self.doubleSpinBoxEndTime.setObjectName(_fromUtf8("doubleSpinBoxEndTime"))
        self.gridLayout_4.addWidget(self.doubleSpinBoxEndTime, 1, 1, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxStartEnd, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(covarianceRawDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_7.addWidget(self.buttonBox, 2, 0, 1, 1)

        self.retranslateUi(covarianceRawDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), covarianceRawDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), covarianceRawDialog.reject)
        QtCore.QObject.connect(self.radioButtonElsewhere, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lineEditRawFile.setEnabled)
        QtCore.QObject.connect(self.radioButtonElsewhere, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.pushButtonBrowse.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(covarianceRawDialog)

    def retranslateUi(self, covarianceRawDialog):
        covarianceRawDialog.setWindowTitle(_translate("covarianceRawDialog", "Compute covariance from raw file", None))
        self.groupBoxSource.setTitle(_translate("covarianceRawDialog", "Use raw file from:", None))
        self.radioButtonCurrentSubject.setText(_translate("covarianceRawDialog", "Current subject", None))
        self.radioButtonElsewhere.setText(_translate("covarianceRawDialog", "Elsewhere:", None))
        self.pushButtonBrowse.setText(_translate("covarianceRawDialog", "Browse...", None))
        self.groupBoxStartEnd.setTitle(_translate("covarianceRawDialog", "Time interval:", None))
        self.labelBeginTime.setText(_translate("covarianceRawDialog", "Beginning of time interval (seconds from start):", None))
        self.doubleSpinBoxStartTime.setSuffix(_translate("covarianceRawDialog", " s", None))
        self.labelEndTime.setText(_translate("covarianceRawDialog", "End of time interval (seconds from start):", None))
        self.doubleSpinBoxEndTime.setSuffix(_translate("covarianceRawDialog", " s", None))

