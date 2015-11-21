# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/talli/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/addSubjectDialog.ui'
#
# Created: Fri Dec 19 13:07:28 2014
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
        self.gridLayout = QtGui.QGridLayout(AddSubject)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(AddSubject)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.listWidgetFileNames = QtGui.QListWidget(AddSubject)
        self.listWidgetFileNames.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetFileNames.setObjectName(_fromUtf8("listWidgetFileNames"))
        self.horizontalLayout.addWidget(self.listWidgetFileNames)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonBrowse = QtGui.QPushButton(AddSubject)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonBrowse.sizePolicy().hasHeightForWidth())
        self.pushButtonBrowse.setSizePolicy(sizePolicy)
        self.pushButtonBrowse.setObjectName(_fromUtf8("pushButtonBrowse"))
        self.verticalLayout.addWidget(self.pushButtonBrowse)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 3)
        self.pushButtonShowFileInfo = QtGui.QPushButton(AddSubject)
        self.pushButtonShowFileInfo.setObjectName(_fromUtf8("pushButtonShowFileInfo"))
        self.gridLayout.addWidget(self.pushButtonShowFileInfo, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(AddSubject)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 2, 1, 1)
        self.pushButtonRemove = QtGui.QPushButton(AddSubject)
        self.pushButtonRemove.setEnabled(False)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.gridLayout.addWidget(self.pushButtonRemove, 2, 1, 1, 1)

        self.retranslateUi(AddSubject)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AddSubject.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AddSubject.reject)
        QtCore.QMetaObject.connectSlotsByName(AddSubject)

    def retranslateUi(self, AddSubject):
        AddSubject.setWindowTitle(_translate("AddSubject", "Meggie - Add subject", None))
        self.label.setText(_translate("AddSubject", "Add subject file to the experiment:", None))
        self.pushButtonBrowse.setText(_translate("AddSubject", "Browse...", None))
        self.pushButtonShowFileInfo.setText(_translate("AddSubject", "Show file info", None))
        self.pushButtonRemove.setText(_translate("AddSubject", "Remove", None))

