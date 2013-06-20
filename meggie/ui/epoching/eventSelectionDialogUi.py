# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eventSelectionDialog.ui'
#
# Created: Sat Jun  1 13:21:29 2013
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

class Ui_EventSelectionDialog(object):
    def setupUi(self, EventSelectionDialog):
        EventSelectionDialog.setObjectName(_fromUtf8("EventSelectionDialog"))
        EventSelectionDialog.setWindowModality(QtCore.Qt.WindowModal)
        EventSelectionDialog.resize(811, 618)
        self.gridLayout = QtGui.QGridLayout(EventSelectionDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(EventSelectionDialog)
        self.scrollArea.setEnabled(True)
        self.scrollArea.setFrameShape(QtGui.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 778, 675))
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
        self.layoutWidget.setGeometry(QtCore.QRect(450, 2, 313, 541))
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
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(EventSelectionDialog)
        self.cancelOkButtonBox.setEnabled(True)
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.gridLayout.addWidget(self.cancelOkButtonBox, 2, 0, 1, 1)

        self.retranslateUi(EventSelectionDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), EventSelectionDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), EventSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(EventSelectionDialog)

    def retranslateUi(self, EventSelectionDialog):
        EventSelectionDialog.setWindowTitle(_translate("EventSelectionDialog", "Meggie - Event selection", None))
        self.pushButtonAdd.setText(_translate("EventSelectionDialog", "Add to list >>", None))
        self.pushButtonRemove.setText(_translate("EventSelectionDialog", "<< Remove", None))
        self.pushButtonSaveEvents.setText(_translate("EventSelectionDialog", "Save events to file...", None))
        self.pushButtonReadEvents.setText(_translate("EventSelectionDialog", "Read events from file...", None))
        self.labelEventID.setText(_translate("EventSelectionDialog", "Event ID:", None))
        self.labelName.setText(_translate("EventSelectionDialog", "Event name:      ", None))

