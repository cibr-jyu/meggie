# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/talli/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/addSubjectDialog.ui'
#
# Created: Tue Dec  9 11:39:42 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_AddSubject(object):
    def setupUi(self, AddSubject):
        AddSubject.setObjectName(_fromUtf8("AddSubject"))
        AddSubject.resize(640, 305)
        self.buttonBox = QtGui.QDialogButtonBox(AddSubject)
        self.buttonBox.setGeometry(QtCore.QRect(460, 270, 171, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(AddSubject)
        self.label.setGeometry(QtCore.QRect(10, 20, 251, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.pushButtonBrowse = QtGui.QPushButton(AddSubject)
        self.pushButtonBrowse.setGeometry(QtCore.QRect(540, 40, 81, 31))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonBrowse.setSizePolicy(sizePolicy)
        self.pushButtonBrowse.setObjectName(_fromUtf8("pushButtonBrowse"))
        self.pushButtonShowFileInfo = QtGui.QPushButton(AddSubject)
        self.pushButtonShowFileInfo.setGeometry(QtCore.QRect(10, 200, 107, 31))
        self.pushButtonShowFileInfo.setObjectName(_fromUtf8("pushButtonShowFileInfo"))
        self.listWidgetFileNames = QtGui.QListWidget(AddSubject)
        self.listWidgetFileNames.setGeometry(QtCore.QRect(10, 40, 521, 151))
        self.listWidgetFileNames.setObjectName(_fromUtf8("listWidgetFileNames"))

        self.retranslateUi(AddSubject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddSubject.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddSubject.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSubject)

    def retranslateUi(self, AddSubject):
        AddSubject.setWindowTitle(_translate("AddSubject", "Meggie - Add subject", None))
        self.label.setText(_translate("AddSubject", "Add subject file to the experiment:", None))
        self.pushButtonBrowse.setText(_translate("AddSubject", "Browse...", None))
        self.pushButtonShowFileInfo.setText(_translate("AddSubject", "Show file info", None))

