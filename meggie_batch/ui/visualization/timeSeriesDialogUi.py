# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'timeSeriesDialog.ui'
#
# Created: Wed Sep  9 01:24:14 2015
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
        self.gridLayout_3 = QtGui.QGridLayout(TimeSeriesDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.spinBoxTstart = QtGui.QSpinBox(TimeSeriesDialog)
        self.spinBoxTstart.setSuffix(_fromUtf8(""))
        self.spinBoxTstart.setObjectName(_fromUtf8("spinBoxTstart"))
        self.gridLayout.addWidget(self.spinBoxTstart, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(TimeSeriesDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.line_3 = QtGui.QFrame(TimeSeriesDialog)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.gridLayout.addWidget(self.line_3, 0, 4, 2, 1)
        self.labelChannels = QtGui.QLabel(TimeSeriesDialog)
        self.labelChannels.setObjectName(_fromUtf8("labelChannels"))
        self.gridLayout.addWidget(self.labelChannels, 0, 5, 1, 1)
        self.spinBoxTend = QtGui.QSpinBox(TimeSeriesDialog)
        self.spinBoxTend.setSuffix(_fromUtf8(""))
        self.spinBoxTend.setObjectName(_fromUtf8("spinBoxTend"))
        self.gridLayout.addWidget(self.spinBoxTend, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(TimeSeriesDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.comboBoxChannels = QtGui.QComboBox(TimeSeriesDialog)
        self.comboBoxChannels.setObjectName(_fromUtf8("comboBoxChannels"))
        self.gridLayout.addWidget(self.comboBoxChannels, 0, 6, 1, 1)
        self.labelMask = QtGui.QLabel(TimeSeriesDialog)
        self.labelMask.setObjectName(_fromUtf8("labelMask"))
        self.gridLayout.addWidget(self.labelMask, 1, 5, 1, 1)
        self.spinBoxMask = QtGui.QSpinBox(TimeSeriesDialog)
        self.spinBoxMask.setObjectName(_fromUtf8("spinBoxMask"))
        self.gridLayout.addWidget(self.spinBoxMask, 1, 6, 1, 1)
        self.pushButtonFind = QtGui.QPushButton(TimeSeriesDialog)
        self.pushButtonFind.setObjectName(_fromUtf8("pushButtonFind"))
        self.gridLayout.addWidget(self.pushButtonFind, 1, 9, 1, 1)
        self.label_4 = QtGui.QLabel(TimeSeriesDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_5 = QtGui.QLabel(TimeSeriesDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.scrollArea = QtGui.QScrollArea(TimeSeriesDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 868, 334))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout_2 = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayoutConditions = QtGui.QVBoxLayout()
        self.verticalLayoutConditions.setObjectName(_fromUtf8("verticalLayoutConditions"))
        self.gridLayout_2.addLayout(self.verticalLayoutConditions, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem1, 2, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(TimeSeriesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 3, 0, 1, 1)

        self.retranslateUi(TimeSeriesDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TimeSeriesDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TimeSeriesDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(TimeSeriesDialog)

    def retranslateUi(self, TimeSeriesDialog):
        TimeSeriesDialog.setWindowTitle(_translate("TimeSeriesDialog", "Time series from triggers", None))
        self.label_3.setText(_translate("TimeSeriesDialog", "Start", None))
        self.labelChannels.setText(_translate("TimeSeriesDialog", "Select the trigger channel", None))
        self.label_2.setText(_translate("TimeSeriesDialog", "End", None))
        self.labelMask.setText(_translate("TimeSeriesDialog", "Mask", None))
        self.pushButtonFind.setText(_translate("TimeSeriesDialog", "Find events", None))
        self.label_4.setText(_translate("TimeSeriesDialog", "seconds after the event.", None))
        self.label_5.setText(_translate("TimeSeriesDialog", "seconds before the event.", None))

