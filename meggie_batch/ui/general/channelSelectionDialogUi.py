# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'channelSelectionDialog.ui'
#
# Created: Tue Jan 13 02:57:04 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_ChannelSelectionDialog(object):
    def setupUi(self, ChannelSelectionDialog):
        ChannelSelectionDialog.setObjectName(_fromUtf8("ChannelSelectionDialog"))
        ChannelSelectionDialog.resize(289, 358)
        self.gridLayout = QtGui.QGridLayout(ChannelSelectionDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.listWidgetChannels = QtGui.QListWidget(ChannelSelectionDialog)
        self.listWidgetChannels.setSelectionMode(QtGui.QAbstractItemView.MultiSelection)
        self.listWidgetChannels.setObjectName(_fromUtf8("listWidgetChannels"))
        self.gridLayout.addWidget(self.listWidgetChannels, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(ChannelSelectionDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 3, 0, 1, 1)
        self.label = QtGui.QLabel(ChannelSelectionDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)

        self.retranslateUi(ChannelSelectionDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ChannelSelectionDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ChannelSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ChannelSelectionDialog)

    def retranslateUi(self, ChannelSelectionDialog):
        ChannelSelectionDialog.setWindowTitle(_translate("ChannelSelectionDialog", "Edit channels.", None))
        self.label.setText(_translate("ChannelSelectionDialog", "Select the channels.", None))

