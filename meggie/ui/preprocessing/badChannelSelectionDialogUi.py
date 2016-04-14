# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'badChannelSelectionDialogUi.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(611, 740)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.scrollArea = QtGui.QScrollArea(Dialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 591, 681))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayoutWidget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 261, 631))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelChannels = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelChannels.setObjectName(_fromUtf8("labelChannels"))
        self.verticalLayout.addWidget(self.labelChannels)
        self.listWidgetChannels = QtGui.QListWidget(self.verticalLayoutWidget)
        self.listWidgetChannels.setMinimumSize(QtCore.QSize(0, 400))
        self.listWidgetChannels.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetChannels.setObjectName(_fromUtf8("listWidgetChannels"))
        self.verticalLayout.addWidget(self.listWidgetChannels)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonSelectAll = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtonSelectAll.setObjectName(_fromUtf8("pushButtonSelectAll"))
        self.horizontalLayout.addWidget(self.pushButtonSelectAll)
        self.pushButtonInvertSelection = QtGui.QPushButton(self.verticalLayoutWidget)
        self.pushButtonInvertSelection.setObjectName(_fromUtf8("pushButtonInvertSelection"))
        self.horizontalLayout.addWidget(self.pushButtonInvertSelection)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.widget = QtGui.QWidget(self.scrollAreaWidgetContents)
        self.widget.setGeometry(QtCore.QRect(280, 230, 301, 371))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.pushButtonCancel = QtGui.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.pushButtonComputeBatch = QtGui.QPushButton(Dialog)
        self.pushButtonComputeBatch.setObjectName(_fromUtf8("pushButtonComputeBatch"))
        self.horizontalLayout_2.addWidget(self.pushButtonComputeBatch)
        self.pushButtonCompute = QtGui.QPushButton(Dialog)
        self.pushButtonCompute.setObjectName(_fromUtf8("pushButtonCompute"))
        self.horizontalLayout_2.addWidget(self.pushButtonCompute)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.reject)
        QtCore.QObject.connect(self.pushButtonCompute, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.accept)
        QtCore.QObject.connect(self.pushButtonComputeBatch, QtCore.SIGNAL(_fromUtf8("clicked()")), Dialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.labelChannels.setText(_translate("Dialog", "Channels:", None))
        self.pushButtonSelectAll.setText(_translate("Dialog", "Select All", None))
        self.pushButtonInvertSelection.setText(_translate("Dialog", "Invert", None))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel", None))
        self.pushButtonComputeBatch.setText(_translate("Dialog", "Compute Batch", None))
        self.pushButtonCompute.setText(_translate("Dialog", "Compute", None))

