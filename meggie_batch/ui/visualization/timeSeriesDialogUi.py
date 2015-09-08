'''
Created on 8.9.2015

@author: Jaakko Leppakangas
'''
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timeSeriesDialog.ui'
#
# Created: Wed Feb  4 05:52:31 2015
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

class Ui_TimeSeriesDialog(object):
    def setupUi(self, TimeSeriesDialog):
        TimeSeriesDialog.setObjectName(_fromUtf8("TimeSeriesDialog"))
        TimeSeriesDialog.resize(888, 517)
        self.gridLayout = QtGui.QGridLayout(TimeSeriesDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label = QtGui.QLabel(TimeSeriesDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.comboBoxChannels = QtGui.QComboBox(TimeSeriesDialog)
        self.comboBoxChannels.setObjectName(_fromUtf8("comboBoxChannels"))
        self.horizontalLayout.addWidget(self.comboBoxChannels)
        self.pushButtonFind = QtGui.QPushButton(TimeSeriesDialog)
        self.pushButtonFind.setObjectName(_fromUtf8("pushButtonFind"))
        self.horizontalLayout.addWidget(self.pushButtonFind)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TimeSeriesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 7, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 6, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(TimeSeriesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 868, 348))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayoutConditions = QtGui.QVBoxLayout()
        self.verticalLayoutConditions.setObjectName(_fromUtf8("verticalLayoutConditions"))
        self.gridLayout_2.addLayout(self.verticalLayoutConditions, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 5, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(TimeSeriesDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.spinBoxTstart = QtGui.QSpinBox(TimeSeriesDialog)
        self.spinBoxTstart.setSuffix(_fromUtf8(""))
        self.spinBoxTstart.setObjectName(_fromUtf8("spinBoxTstart"))
        self.horizontalLayout_2.addWidget(self.spinBoxTstart)
        self.label_4 = QtGui.QLabel(TimeSeriesDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_2.addWidget(self.label_4)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.label_2 = QtGui.QLabel(TimeSeriesDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.spinBoxTend = QtGui.QSpinBox(TimeSeriesDialog)
        self.spinBoxTend.setSuffix(_fromUtf8(""))
        self.spinBoxTend.setObjectName(_fromUtf8("spinBoxTend"))
        self.horizontalLayout_2.addWidget(self.spinBoxTend)
        self.label_5 = QtGui.QLabel(TimeSeriesDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(TimeSeriesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TimeSeriesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TimeSeriesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TimeSeriesDialog)

    def retranslateUi(self, TimeSeriesDialog):
        TimeSeriesDialog.setWindowTitle(_translate("TimeSeriesDialog", "Time series from triggers", None))
        self.label.setText(_translate("TimeSeriesDialog", "Select the trigger channel", None))
        self.pushButtonFind.setText(_translate("TimeSeriesDialog", "Find events", None))
        self.label_3.setText(_translate("TimeSeriesDialog", "Start time", None))
        self.label_4.setText(_translate("TimeSeriesDialog", "seconds after the event.", None))
        self.label_2.setText(_translate("TimeSeriesDialog", "End time", None))
        self.label_5.setText(_translate("TimeSeriesDialog", "seconds before the event.", None))
