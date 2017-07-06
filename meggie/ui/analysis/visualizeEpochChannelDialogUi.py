# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'visualizeEpochChannelDialogUi.ui'
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

class Ui_VisualizeEpochChannelDialog(object):
    def setupUi(self, VisualizeEpochChannelDialog):
        VisualizeEpochChannelDialog.setObjectName(_fromUtf8("VisualizeEpochChannelDialog"))
        VisualizeEpochChannelDialog.resize(499, 328)
        self.gridLayout_3 = QtGui.QGridLayout(VisualizeEpochChannelDialog)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.scrollArea = QtGui.QScrollArea(VisualizeEpochChannelDialog)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 479, 269))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.gridLayout = QtGui.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelChannels = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.labelChannels.setObjectName(_fromUtf8("labelChannels"))
        self.gridLayout.addWidget(self.labelChannels, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelSigma = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.labelSigma.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.labelSigma.setObjectName(_fromUtf8("labelSigma"))
        self.horizontalLayout.addWidget(self.labelSigma)
        self.doubleSpinBoxSigma = QtGui.QDoubleSpinBox(self.scrollAreaWidgetContents)
        self.doubleSpinBoxSigma.setSingleStep(0.05)
        self.doubleSpinBoxSigma.setProperty("value", 0.5)
        self.doubleSpinBoxSigma.setObjectName(_fromUtf8("doubleSpinBoxSigma"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxSigma)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 1)
        self.listWidgetChannels = QtGui.QListWidget(self.scrollAreaWidgetContents)
        self.listWidgetChannels.setObjectName(_fromUtf8("listWidgetChannels"))
        self.gridLayout.addWidget(self.listWidgetChannels, 1, 0, 1, 1)
        self.pushButtonVisualizeChannel = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.pushButtonVisualizeChannel.setObjectName(_fromUtf8("pushButtonVisualizeChannel"))
        self.gridLayout.addWidget(self.pushButtonVisualizeChannel, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout_3.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonClose = QtGui.QPushButton(VisualizeEpochChannelDialog)
        self.pushButtonClose.setObjectName(_fromUtf8("pushButtonClose"))
        self.horizontalLayout_2.addWidget(self.pushButtonClose)
        self.gridLayout_3.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)

        self.retranslateUi(VisualizeEpochChannelDialog)
        QtCore.QObject.connect(self.pushButtonClose, QtCore.SIGNAL(_fromUtf8("clicked()")), VisualizeEpochChannelDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(VisualizeEpochChannelDialog)

    def retranslateUi(self, VisualizeEpochChannelDialog):
        VisualizeEpochChannelDialog.setWindowTitle(_translate("VisualizeEpochChannelDialog", "Meggie - Visualize epoch channels", None))
        self.labelChannels.setText(_translate("VisualizeEpochChannelDialog", "Pick channel:", None))
        self.labelSigma.setText(_translate("VisualizeEpochChannelDialog", "Gaussian smoothing:", None))
        self.pushButtonVisualizeChannel.setText(_translate("VisualizeEpochChannelDialog", "Visualize selected channel", None))
        self.pushButtonClose.setText(_translate("VisualizeEpochChannelDialog", "Close", None))

