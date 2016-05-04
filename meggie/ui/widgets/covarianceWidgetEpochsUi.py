# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'covarianceWidgetEpochsUi.ui'
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(563, 413)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setContentsMargins(9, 0, 9, 0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBoxCovarianceMatrix = QtGui.QGroupBox(Form)
        self.groupBoxCovarianceMatrix.setObjectName(_fromUtf8("groupBoxCovarianceMatrix"))
        self.formLayout = QtGui.QFormLayout(self.groupBoxCovarianceMatrix)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelBasedOn = QtGui.QLabel(self.groupBoxCovarianceMatrix)
        self.labelBasedOn.setObjectName(_fromUtf8("labelBasedOn"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelBasedOn)
        self.listWidgetEpochs = QtGui.QListWidget(self.groupBoxCovarianceMatrix)
        self.listWidgetEpochs.setObjectName(_fromUtf8("listWidgetEpochs"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.listWidgetEpochs)
        self.groupBoxEpochTimes = QtGui.QGroupBox(self.groupBoxCovarianceMatrix)
        self.groupBoxEpochTimes.setObjectName(_fromUtf8("groupBoxEpochTimes"))
        self.formLayout_16 = QtGui.QFormLayout(self.groupBoxEpochTimes)
        self.formLayout_16.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_16.setObjectName(_fromUtf8("formLayout_16"))
        self.labelTminCovariance = QtGui.QLabel(self.groupBoxEpochTimes)
        self.labelTminCovariance.setMinimumSize(QtCore.QSize(80, 0))
        self.labelTminCovariance.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelTminCovariance.setObjectName(_fromUtf8("labelTminCovariance"))
        self.formLayout_16.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelTminCovariance)
        self.textBrowserTmin = QtGui.QTextBrowser(self.groupBoxEpochTimes)
        self.textBrowserTmin.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserTmin.sizePolicy().hasHeightForWidth())
        self.textBrowserTmin.setSizePolicy(sizePolicy)
        self.textBrowserTmin.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserTmin.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowserTmin.setSizeIncrement(QtCore.QSize(0, 31))
        self.textBrowserTmin.setBaseSize(QtCore.QSize(0, 0))
        self.textBrowserTmin.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textBrowserTmin.setObjectName(_fromUtf8("textBrowserTmin"))
        self.formLayout_16.setWidget(1, QtGui.QFormLayout.FieldRole, self.textBrowserTmin)
        self.labelTmaxCovariance = QtGui.QLabel(self.groupBoxEpochTimes)
        self.labelTmaxCovariance.setMinimumSize(QtCore.QSize(80, 0))
        self.labelTmaxCovariance.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelTmaxCovariance.setObjectName(_fromUtf8("labelTmaxCovariance"))
        self.formLayout_16.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelTmaxCovariance)
        self.textBrowserTmax = QtGui.QTextBrowser(self.groupBoxEpochTimes)
        self.textBrowserTmax.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowserTmax.sizePolicy().hasHeightForWidth())
        self.textBrowserTmax.setSizePolicy(sizePolicy)
        self.textBrowserTmax.setMinimumSize(QtCore.QSize(0, 0))
        self.textBrowserTmax.setMaximumSize(QtCore.QSize(16777215, 30))
        self.textBrowserTmax.setSizeIncrement(QtCore.QSize(0, 31))
        self.textBrowserTmax.setObjectName(_fromUtf8("textBrowserTmax"))
        self.formLayout_16.setWidget(2, QtGui.QFormLayout.FieldRole, self.textBrowserTmax)
        self.labelKeepSample = QtGui.QLabel(self.groupBoxEpochTimes)
        self.labelKeepSample.setTextFormat(QtCore.Qt.RichText)
        self.labelKeepSample.setObjectName(_fromUtf8("labelKeepSample"))
        self.formLayout_16.setWidget(5, QtGui.QFormLayout.LabelRole, self.labelKeepSample)
        self.labelKeepSampleValue = QtGui.QLabel(self.groupBoxEpochTimes)
        self.labelKeepSampleValue.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelKeepSampleValue.setObjectName(_fromUtf8("labelKeepSampleValue"))
        self.formLayout_16.setWidget(5, QtGui.QFormLayout.FieldRole, self.labelKeepSampleValue)
        self.labelMethod = QtGui.QLabel(self.groupBoxEpochTimes)
        self.labelMethod.setObjectName(_fromUtf8("labelMethod"))
        self.formLayout_16.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelMethod)
        self.labelMethodValue = QtGui.QLabel(self.groupBoxEpochTimes)
        self.labelMethodValue.setText(_fromUtf8(""))
        self.labelMethodValue.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelMethodValue.setObjectName(_fromUtf8("labelMethodValue"))
        self.formLayout_16.setWidget(4, QtGui.QFormLayout.FieldRole, self.labelMethodValue)
        self.formLayout.setWidget(3, QtGui.QFormLayout.SpanningRole, self.groupBoxEpochTimes)
        self.gridLayout_2.addWidget(self.groupBoxCovarianceMatrix, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBoxCovarianceMatrix.setTitle(_translate("Form", "Current covariance matrix info:", None))
        self.labelBasedOn.setText(_translate("Form", "Based on:", None))
        self.groupBoxEpochTimes.setTitle(_translate("Form", "Time limits:", None))
        self.labelTminCovariance.setText(_translate("Form", "Start time:", None))
        self.labelTmaxCovariance.setText(_translate("Form", "End time:", None))
        self.labelKeepSample.setText(_translate("Form", "Keep sample\n"
"mean:", None))
        self.labelKeepSampleValue.setText(_translate("Form", "False", None))
        self.labelMethod.setText(_translate("Form", "Method:", None))

