# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterDialog.ui'
#
# Created: Thu May  2 17:55:20 2013
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

class Ui_ParameterDialog(object):
    def setupUi(self, ParameterDialog):
        ParameterDialog.setObjectName(_fromUtf8("ParameterDialog"))
        ParameterDialog.setWindowModality(QtCore.Qt.WindowModal)
        ParameterDialog.resize(779, 617)
        self.gridLayout = QtGui.QGridLayout(ParameterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(ParameterDialog)
        self.cancelOkButtonBox.setEnabled(True)
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.gridLayout.addWidget(self.cancelOkButtonBox, 2, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(ParameterDialog)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 743, 675))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(741, 675))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(310, 0, 131, 71))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.pushButtonAdd = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.verticalLayout.addWidget(self.pushButtonAdd)
        self.pushButtonRemove = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtonRemove.setEnabled(False)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.verticalLayout.addWidget(self.pushButtonRemove)
        self.layoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.layoutWidget.setGeometry(QtCore.QRect(450, 2, 285, 541))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.listWidgetEvents = QtGui.QListWidget(self.layoutWidget)
        self.listWidgetEvents.setObjectName(_fromUtf8("listWidgetEvents"))
        self.verticalLayout_4.addWidget(self.listWidgetEvents)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.pushButtonSaveEvents = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonSaveEvents.setObjectName(_fromUtf8("pushButtonSaveEvents"))
        self.horizontalLayout_8.addWidget(self.pushButtonSaveEvents)
        self.pushButtonReadEvents = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonReadEvents.setObjectName(_fromUtf8("pushButtonReadEvents"))
        self.horizontalLayout_8.addWidget(self.pushButtonReadEvents)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.layoutWidget1 = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.layoutWidget1.setGeometry(QtCore.QRect(0, 0, 301, 74))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelEventID = QtGui.QLabel(self.layoutWidget1)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_7.addWidget(self.labelEventID)
        self.comboBoxEventID = QtGui.QComboBox(self.layoutWidget1)
        self.comboBoxEventID.setObjectName(_fromUtf8("comboBoxEventID"))
        self.horizontalLayout_7.addWidget(self.comboBoxEventID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelName = QtGui.QLabel(self.layoutWidget1)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_5.addWidget(self.labelName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.lineEditName = QtGui.QLineEdit(self.layoutWidget1)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_5.addWidget(self.lineEditName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 1)

        self.retranslateUi(ParameterDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParameterDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParameterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ParameterDialog)

    def retranslateUi(self, ParameterDialog):
        ParameterDialog.setWindowTitle(_translate("ParameterDialog", "Give parameters", None))
        self.pushButtonAdd.setText(_translate("ParameterDialog", "Add to list >>", None))
        self.pushButtonRemove.setText(_translate("ParameterDialog", "<< Remove", None))
        self.pushButtonSaveEvents.setText(_translate("ParameterDialog", "Save events", None))
        self.pushButtonReadEvents.setText(_translate("ParameterDialog", "Read events", None))
        self.labelEventID.setText(_translate("ParameterDialog", "Event ID:", None))
        self.labelName.setText(_translate("ParameterDialog", "Event name:      ", None))
