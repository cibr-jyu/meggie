# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizeEpochChannelDialog.ui'
#
# Created: Thu Sep 12 15:50:18 2013
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

class Ui_VisualizeEpochChannelDialog(object):
    def setupUi(self, VisualizeEpochChannelDialog):
        VisualizeEpochChannelDialog.setObjectName(_fromUtf8("VisualizeEpochChannelDialog"))
        VisualizeEpochChannelDialog.resize(559, 287)
        self.listWidgetChannels = QtGui.QListWidget(VisualizeEpochChannelDialog)
        self.listWidgetChannels.setGeometry(QtCore.QRect(20, 30, 211, 171))
        self.listWidgetChannels.setObjectName(_fromUtf8("listWidgetChannels"))
        self.labelChannels = QtGui.QLabel(VisualizeEpochChannelDialog)
        self.labelChannels.setGeometry(QtCore.QRect(20, 10, 91, 21))
        self.labelChannels.setObjectName(_fromUtf8("labelChannels"))
        self.pushButtonVisualizeChannels = QtGui.QPushButton(VisualizeEpochChannelDialog)
        self.pushButtonVisualizeChannels.setGeometry(QtCore.QRect(240, 170, 281, 31))
        self.pushButtonVisualizeChannels.setObjectName(_fromUtf8("pushButtonVisualizeChannels"))
        self.verticalLayoutWidget = QtGui.QWidget(VisualizeEpochChannelDialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(240, 30, 271, 121))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelSigma = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelSigma.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelSigma.setObjectName(_fromUtf8("labelSigma"))
        self.horizontalLayout.addWidget(self.labelSigma)
        self.doubleSpinBoxSigma = QtGui.QDoubleSpinBox(self.verticalLayoutWidget)
        self.doubleSpinBoxSigma.setSingleStep(0.05)
        self.doubleSpinBoxSigma.setProperty("value", 0.5)
        self.doubleSpinBoxSigma.setObjectName(_fromUtf8("doubleSpinBoxSigma"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxSigma)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelVmin = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelVmin.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelVmin.setObjectName(_fromUtf8("labelVmin"))
        self.horizontalLayout_2.addWidget(self.labelVmin)
        self.spinBoxVmin = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.spinBoxVmin.setMinimum(-100000)
        self.spinBoxVmin.setMaximum(100000)
        self.spinBoxVmin.setSingleStep(10)
        self.spinBoxVmin.setProperty("value", -100)
        self.spinBoxVmin.setObjectName(_fromUtf8("spinBoxVmin"))
        self.horizontalLayout_2.addWidget(self.spinBoxVmin)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.labelVmax = QtGui.QLabel(self.verticalLayoutWidget)
        self.labelVmax.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.labelVmax.setObjectName(_fromUtf8("labelVmax"))
        self.horizontalLayout_3.addWidget(self.labelVmax)
        self.spinBoxVmax = QtGui.QSpinBox(self.verticalLayoutWidget)
        self.spinBoxVmax.setMinimum(-100000)
        self.spinBoxVmax.setMaximum(100000)
        self.spinBoxVmax.setProperty("value", 250)
        self.spinBoxVmax.setObjectName(_fromUtf8("spinBoxVmax"))
        self.horizontalLayout_3.addWidget(self.spinBoxVmax)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pushButtonClose = QtGui.QPushButton(VisualizeEpochChannelDialog)
        self.pushButtonClose.setGeometry(QtCore.QRect(410, 250, 111, 31))
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))

        self.retranslateUi(VisualizeEpochChannelDialog)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), VisualizeEpochChannelDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VisualizeEpochChannelDialog)

    def retranslateUi(self, VisualizeEpochChannelDialog):
        VisualizeEpochChannelDialog.setWindowTitle(_translate("VisualizeEpochChannelDialog", "Meggie - Visualize epoch channels", None))
        self.labelChannels.setText(_translate("VisualizeEpochChannelDialog", "Pick channels:", None))
        self.pushButtonVisualizeChannels.setText(_translate("VisualizeEpochChannelDialog", "Visualize selected channels", None))
        self.labelSigma.setText(_translate("VisualizeEpochChannelDialog", "Gaussian smoothing:", None))
        self.labelVmin.setText(_translate("VisualizeEpochChannelDialog", "Min value:", None))
        self.labelVmax.setText(_translate("VisualizeEpochChannelDialog", "Max value:", None))
        self.pushButtonClose.setText(_translate("VisualizeEpochChannelDialog", "Close", None))

