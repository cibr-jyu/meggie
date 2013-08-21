# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'epochParamsWidget.ui'
#
# Created: Wed Aug 21 11:03:00 2013
#      by: PyQt4 UI code generator 4.9.6
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
        Form.resize(419, 328)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 401, 321))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.labelEvents = QtGui.QLabel(self.groupBox)
        self.labelEvents.setGeometry(QtCore.QRect(10, 60, 61, 21))
        self.labelEvents.setScaledContents(True)
        self.labelEvents.setWordWrap(True)
        self.labelEvents.setObjectName(_fromUtf8("labelEvents"))
        self.textBrowserEvents = QtGui.QTextBrowser(self.groupBox)
        self.textBrowserEvents.setGeometry(QtCore.QRect(70, 70, 331, 91))
        self.textBrowserEvents.setObjectName(_fromUtf8("textBrowserEvents"))
        self.groupBoxRejections = QtGui.QGroupBox(self.groupBox)
        self.groupBoxRejections.setGeometry(QtCore.QRect(10, 160, 411, 121))
        self.groupBoxRejections.setObjectName(_fromUtf8("groupBoxRejections"))
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBoxRejections)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 30, 381, 83))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelGradReject = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelGradReject.setObjectName(_fromUtf8("labelGradReject"))
        self.horizontalLayout_2.addWidget(self.labelGradReject)
        self.labelMagReject = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelMagReject.setObjectName(_fromUtf8("labelMagReject"))
        self.horizontalLayout_2.addWidget(self.labelMagReject)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelEegReject = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelEegReject.setObjectName(_fromUtf8("labelEegReject"))
        self.horizontalLayout_3.addWidget(self.labelEegReject)
        self.labelEogReject = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelEogReject.setObjectName(_fromUtf8("labelEogReject"))
        self.horizontalLayout_3.addWidget(self.labelEogReject)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelStimReject = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelStimReject.setObjectName(_fromUtf8("labelStimReject"))
        self.horizontalLayout_5.addWidget(self.labelStimReject)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 391, 23))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.layoutWidget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        self.labelTmax = QtGui.QLabel(self.layoutWidget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout.addWidget(self.labelTmax)
        self.labelWorkingFile = QtGui.QLabel(self.groupBox)
        self.labelWorkingFile.setGeometry(QtCore.QRect(10, 280, 91, 21))
        self.labelWorkingFile.setObjectName(_fromUtf8("labelWorkingFile"))
        self.textBrowserWorkingFile = QtGui.QTextBrowser(self.groupBox)
        self.textBrowserWorkingFile.setGeometry(QtCore.QRect(80, 280, 321, 31))
        self.textBrowserWorkingFile.setObjectName(_fromUtf8("textBrowserWorkingFile"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Epoch parameters:", None))
        self.labelEvents.setText(_translate("Form", "Events:", None))
        self.groupBoxRejections.setTitle(_translate("Form", "Rejections:", None))
        self.labelGradReject.setText(_translate("Form", "Grad:", None))
        self.labelMagReject.setText(_translate("Form", "Mag:", None))
        self.labelEegReject.setText(_translate("Form", "EEG:", None))
        self.labelEogReject.setText(_translate("Form", "EOG:", None))
        self.labelStimReject.setText(_translate("Form", "Stim:", None))
        self.labelTmin.setText(_translate("Form", "Start time:", None))
        self.labelTmax.setText(_translate("Form", "End time:", None))
        self.labelWorkingFile.setText(_translate("Form", "Filename:", None))

