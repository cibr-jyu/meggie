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
        covarianceRawDialog.resize(496, 337)
        self.gridLayout_7 = QtGui.QGridLayout(covarianceRawDialog)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.buttonBox = QtGui.QDialogButtonBox(covarianceRawDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_7.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.groupBoxName = QtGui.QGroupBox(covarianceRawDialog)
        self.groupBoxName.setObjectName(_fromUtf8("groupBoxName"))
        self.gridLayout = QtGui.QGridLayout(self.groupBoxName)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelName = QtGui.QLabel(self.groupBoxName)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_4.addWidget(self.labelName)
        self.lineEditName = QtGui.QLineEdit(self.groupBoxName)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_4.addWidget(self.lineEditName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.gridLayout.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxName, 0, 0, 1, 1)
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
        self.horizontalLayout_5.addWidget(self.radioButtonCurrentSubject)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.radioButtonElsewhere = QtGui.QRadioButton(self.groupBoxSource)
        self.radioButtonElsewhere.setObjectName(_fromUtf8("radioButtonElsewhere"))
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
        self.gridLayout_7.addWidget(self.groupBoxSource, 1, 0, 1, 1)
        self.groupBoxStartEnd = QtGui.QGroupBox(covarianceRawDialog)
        self.groupBoxStartEnd.setObjectName(_fromUtf8("groupBoxStartEnd"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxStartEnd)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelBeginTime = QtGui.QLabel(self.groupBoxStartEnd)
        self.labelBeginTime.setObjectName(_fromUtf8("labelBeginTime"))
        self.horizontalLayout_3.addWidget(self.labelBeginTime)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.doubleSpinBoxStartTime = QtGui.QDoubleSpinBox(self.groupBoxStartEnd)
        self.doubleSpinBoxStartTime.setPrefix(_fromUtf8(""))
        self.doubleSpinBoxStartTime.setObjectName(_fromUtf8("doubleSpinBoxStartTime"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBoxStartTime)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelEndTime = QtGui.QLabel(self.groupBoxStartEnd)
        self.labelEndTime.setObjectName(_fromUtf8("labelEndTime"))
        self.horizontalLayout_2.addWidget(self.labelEndTime)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.doubleSpinBoxEndTime = QtGui.QDoubleSpinBox(self.groupBoxStartEnd)
        self.doubleSpinBoxEndTime.setObjectName(_fromUtf8("doubleSpinBoxEndTime"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBoxEndTime)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_4.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_7.addWidget(self.groupBoxStartEnd, 2, 0, 1, 1)

        self.retranslateUi(covarianceRawDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), covarianceRawDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), covarianceRawDialog.reject)
        QtCore.QObject.connect(self.radioButtonElsewhere, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.lineEditRawFile.setEnabled)
        QtCore.QObject.connect(self.radioButtonElsewhere, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.pushButtonBrowse.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(covarianceRawDialog)

    def retranslateUi(self, covarianceRawDialog):
        covarianceRawDialog.setWindowTitle(_translate("covarianceRawDialog", "Compute covariance from raw file", None))
        self.groupBoxName.setTitle(_translate("covarianceRawDialog", "General:", None))
        self.labelName.setText(_translate("covarianceRawDialog", "Name:", None))
        self.groupBoxSource.setTitle(_translate("covarianceRawDialog", "Use raw file from:", None))
        self.radioButtonCurrentSubject.setText(_translate("covarianceRawDialog", "Current subject", None))
        self.radioButtonElsewhere.setText(_translate("covarianceRawDialog", "Elsewhere:", None))
        self.pushButtonBrowse.setText(_translate("covarianceRawDialog", "Browse...", None))
        self.groupBoxStartEnd.setTitle(_translate("covarianceRawDialog", "Time interval:", None))
        self.labelBeginTime.setText(_translate("covarianceRawDialog", "Beginning of time interval (seconds from start):", None))
        self.doubleSpinBoxStartTime.setSuffix(_translate("covarianceRawDialog", " s", None))
        self.labelEndTime.setText(_translate("covarianceRawDialog", "End of time interval (seconds from start):", None))
        self.doubleSpinBoxEndTime.setSuffix(_translate("covarianceRawDialog", " s", None))

