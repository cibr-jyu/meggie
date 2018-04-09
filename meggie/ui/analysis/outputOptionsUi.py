# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt4Designer_ui_files/outputOptions.ui'
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

class Ui_outputOptions(object):
    def setupUi(self, outputOptions):
        outputOptions.setObjectName(_fromUtf8("outputOptions"))
        outputOptions.resize(313, 175)
        self.formLayout = QtGui.QFormLayout(outputOptions)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBoxRows = QtGui.QGroupBox(outputOptions)
        self.groupBoxRows.setObjectName(_fromUtf8("groupBoxRows"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxRows)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.radioButtonAllChannels = QtGui.QRadioButton(self.groupBoxRows)
        self.radioButtonAllChannels.setChecked(True)
        self.radioButtonAllChannels.setObjectName(_fromUtf8("radioButtonAllChannels"))
        self.gridLayout_2.addWidget(self.radioButtonAllChannels, 0, 0, 1, 1)
        self.radioButtonChannelAverages = QtGui.QRadioButton(self.groupBoxRows)
        self.radioButtonChannelAverages.setObjectName(_fromUtf8("radioButtonChannelAverages"))
        self.gridLayout_2.addWidget(self.radioButtonChannelAverages, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxRows, 0, 0, 1, 1)
        self.groupBoxColumns = QtGui.QGroupBox(outputOptions)
        self.groupBoxColumns.setObjectName(_fromUtf8("groupBoxColumns"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxColumns)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.radioButtonAllData = QtGui.QRadioButton(self.groupBoxColumns)
        self.radioButtonAllData.setChecked(True)
        self.radioButtonAllData.setObjectName(_fromUtf8("radioButtonAllData"))
        self.gridLayout_3.addWidget(self.radioButtonAllData, 0, 0, 1, 1)
        self.radioButtonStatistics = QtGui.QRadioButton(self.groupBoxColumns)
        self.radioButtonStatistics.setObjectName(_fromUtf8("radioButtonStatistics"))
        self.gridLayout_3.addWidget(self.radioButtonStatistics, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxColumns, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonCancel = QtGui.QPushButton(outputOptions)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonAccept = QtGui.QPushButton(outputOptions)
        self.pushButtonAccept.setObjectName(_fromUtf8("pushButtonAccept"))
        self.horizontalLayout.addWidget(self.pushButtonAccept)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout)

        self.retranslateUi(outputOptions)
        QtCore.QObject.connect(self.pushButtonCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), outputOptions.reject)
        QtCore.QObject.connect(self.pushButtonAccept, QtCore.SIGNAL(_fromUtf8("clicked()")), outputOptions.accept)
        QtCore.QMetaObject.connectSlotsByName(outputOptions)

    def retranslateUi(self, outputOptions):
        outputOptions.setWindowTitle(_translate("outputOptions", "Output options", None))
        self.groupBoxRows.setTitle(_translate("outputOptions", "Rows", None))
        self.radioButtonAllChannels.setText(_translate("outputOptions", "All channels", None))
        self.radioButtonChannelAverages.setText(_translate("outputOptions", "Channel averages", None))
        self.groupBoxColumns.setTitle(_translate("outputOptions", "Columns", None))
        self.radioButtonAllData.setText(_translate("outputOptions", "All data", None))
        self.radioButtonStatistics.setText(_translate("outputOptions", "Statistics", None))
        self.pushButtonCancel.setText(_translate("outputOptions", "Cancel", None))
        self.pushButtonAccept.setText(_translate("outputOptions", "Accept", None))

