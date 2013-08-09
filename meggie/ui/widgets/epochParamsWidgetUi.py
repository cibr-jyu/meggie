# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'epochParamsWidget.ui'
#
# Created: Fri Aug  9 10:49:44 2013
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
        Form.resize(447, 238)
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(9, 9, 421, 221))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 160, 391, 21))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelGradReject_3 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.labelGradReject_3.setObjectName(_fromUtf8("labelGradReject_3"))
        self.horizontalLayout_2.addWidget(self.labelGradReject_3)
        self.labelMagReject_3 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.labelMagReject_3.setObjectName(_fromUtf8("labelMagReject_3"))
        self.horizontalLayout_2.addWidget(self.labelMagReject_3)
        self.labelEvents = QtGui.QLabel(self.groupBox)
        self.labelEvents.setGeometry(QtCore.QRect(17, 25, 61, 21))
        self.labelEvents.setScaledContents(True)
        self.labelEvents.setWordWrap(True)
        self.labelEvents.setObjectName(_fromUtf8("labelEvents"))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(self.groupBox)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 190, 391, 21))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelEegReject_3 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.labelEegReject_3.setObjectName(_fromUtf8("labelEegReject_3"))
        self.horizontalLayout_3.addWidget(self.labelEegReject_3)
        self.labelEogReject_3 = QtGui.QLabel(self.horizontalLayoutWidget_2)
        self.labelEogReject_3.setObjectName(_fromUtf8("labelEogReject_3"))
        self.horizontalLayout_3.addWidget(self.labelEogReject_3)
        self.textBrowserEvents = QtGui.QTextBrowser(self.groupBox)
        self.textBrowserEvents.setGeometry(QtCore.QRect(70, 30, 341, 91))
        self.textBrowserEvents.setObjectName(_fromUtf8("textBrowserEvents"))
        self.widget = QtGui.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(20, 130, 391, 23))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.widget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        self.labelTmax = QtGui.QLabel(self.widget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout.addWidget(self.labelTmax)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.groupBox.setTitle(_translate("Form", "Epoch parameters:", None))
        self.labelGradReject_3.setText(_translate("Form", "Grad:", None))
        self.labelMagReject_3.setText(_translate("Form", "Mag:", None))
        self.labelEvents.setText(_translate("Form", "Events:", None))
        self.labelEegReject_3.setText(_translate("Form", "EEG:", None))
        self.labelEogReject_3.setText(_translate("Form", "EOG:", None))
        self.labelTmin.setText(_translate("Form", "Start time:", None))
        self.labelTmax.setText(_translate("Form", "End time:", None))

