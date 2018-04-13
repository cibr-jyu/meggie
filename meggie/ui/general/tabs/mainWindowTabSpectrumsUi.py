# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindowTabSpectrumsUi.ui'
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

class Ui_mainWindowTabSpectrums(object):
    def setupUi(self, mainWindowTabSpectrums):
        mainWindowTabSpectrums.setObjectName(_fromUtf8("mainWindowTabSpectrums"))
        mainWindowTabSpectrums.resize(1112, 732)
        self.layoutWidget = QtGui.QWidget(mainWindowTabSpectrums)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 981, 711))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_15 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_15.setObjectName(_fromUtf8("gridLayout_15"))
        self.verticalLayout_23 = QtGui.QVBoxLayout()
        self.verticalLayout_23.setObjectName(_fromUtf8("verticalLayout_23"))
        self.groupBoxEpochs = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxEpochs.setObjectName(_fromUtf8("groupBoxEpochs"))
        self.verticalLayout_23.addWidget(self.groupBoxEpochs)
        self.groupBoxComputations = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxComputations.setMinimumSize(QtCore.QSize(400, 0))
        self.groupBoxComputations.setObjectName(_fromUtf8("groupBoxComputations"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxComputations)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButtonComputeSpectrum = QtGui.QPushButton(self.groupBoxComputations)
        self.pushButtonComputeSpectrum.setObjectName(_fromUtf8("pushButtonComputeSpectrum"))
        self.gridLayout_2.addWidget(self.pushButtonComputeSpectrum, 0, 0, 1, 1)
        self.verticalLayout_23.addWidget(self.groupBoxComputations)
        self.gridLayout_15.addLayout(self.verticalLayout_23, 0, 0, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBoxSpectrums = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxSpectrums.setMinimumSize(QtCore.QSize(0, 300))
        self.groupBoxSpectrums.setObjectName(_fromUtf8("groupBoxSpectrums"))
        self.formLayout = QtGui.QFormLayout(self.groupBoxSpectrums)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelSpectrumInfo = QtGui.QLabel(self.groupBoxSpectrums)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelSpectrumInfo.setFont(font)
        self.labelSpectrumInfo.setObjectName(_fromUtf8("labelSpectrumInfo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelSpectrumInfo)
        self.textBrowserSpectrumInfo = QtGui.QTextBrowser(self.groupBoxSpectrums)
        self.textBrowserSpectrumInfo.setObjectName(_fromUtf8("textBrowserSpectrumInfo"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.textBrowserSpectrumInfo)
        self.listWidgetSpectrums = QtGui.QListWidget(self.groupBoxSpectrums)
        self.listWidgetSpectrums.setObjectName(_fromUtf8("listWidgetSpectrums"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.listWidgetSpectrums)
        self.verticalLayout_6.addWidget(self.groupBoxSpectrums)
        self.groupBoxSpectrumActions = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxSpectrumActions.setObjectName(_fromUtf8("groupBoxSpectrumActions"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxSpectrumActions)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBoxSpectrumActions)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_21 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_21.setObjectName(_fromUtf8("gridLayout_21"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonVisualizeSpectrum = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonVisualizeSpectrum.setObjectName(_fromUtf8("pushButtonVisualizeSpectrum"))
        self.horizontalLayout_2.addWidget(self.pushButtonVisualizeSpectrum)
        self.gridLayout_21.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonDeleteSpectrum = QtGui.QPushButton(self.groupBoxSpectrumActions)
        self.pushButtonDeleteSpectrum.setObjectName(_fromUtf8("pushButtonDeleteSpectrum"))
        self.gridLayout.addWidget(self.pushButtonDeleteSpectrum, 1, 0, 1, 1)
        self.pushButtonGroupDeleteSpectrum = QtGui.QPushButton(self.groupBoxSpectrumActions)
        self.pushButtonGroupDeleteSpectrum.setObjectName(_fromUtf8("pushButtonGroupDeleteSpectrum"))
        self.gridLayout.addWidget(self.pushButtonGroupDeleteSpectrum, 2, 0, 1, 1)
        self.pushButtonGroupAverage = QtGui.QPushButton(self.groupBoxSpectrumActions)
        self.pushButtonGroupAverage.setObjectName(_fromUtf8("pushButtonGroupAverage"))
        self.gridLayout.addWidget(self.pushButtonGroupAverage, 0, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(self.groupBoxSpectrumActions)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_20 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_20.setObjectName(_fromUtf8("gridLayout_20"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonSaveSpectrum = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonSaveSpectrum.setObjectName(_fromUtf8("pushButtonSaveSpectrum"))
        self.horizontalLayout_3.addWidget(self.pushButtonSaveSpectrum)
        self.pushButtonGroupSaveSpectrum = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonGroupSaveSpectrum.setObjectName(_fromUtf8("pushButtonGroupSaveSpectrum"))
        self.horizontalLayout_3.addWidget(self.pushButtonGroupSaveSpectrum)
        self.gridLayout_20.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_5, 2, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBoxSpectrumActions)
        self.gridLayout_15.addLayout(self.verticalLayout_6, 0, 1, 1, 1)

        self.retranslateUi(mainWindowTabSpectrums)
        QtCore.QMetaObject.connectSlotsByName(mainWindowTabSpectrums)

    def retranslateUi(self, mainWindowTabSpectrums):
        mainWindowTabSpectrums.setWindowTitle(_translate("mainWindowTabSpectrums", "Form", None))
        self.groupBoxEpochs.setTitle(_translate("mainWindowTabSpectrums", "Epochs", None))
        self.groupBoxComputations.setTitle(_translate("mainWindowTabSpectrums", "Computations", None))
        self.pushButtonComputeSpectrum.setText(_translate("mainWindowTabSpectrums", "Compute spectrum", None))
        self.groupBoxSpectrums.setTitle(_translate("mainWindowTabSpectrums", "Spectrums", None))
        self.labelSpectrumInfo.setText(_translate("mainWindowTabSpectrums", "Spectrum info", None))
        self.groupBoxSpectrumActions.setTitle(_translate("mainWindowTabSpectrums", "Available actions for spectrums", None))
        self.groupBox_2.setTitle(_translate("mainWindowTabSpectrums", "Visualization:", None))
        self.pushButtonVisualizeSpectrum.setText(_translate("mainWindowTabSpectrums", "Visualize selected spectrum", None))
        self.pushButtonDeleteSpectrum.setText(_translate("mainWindowTabSpectrums", "Delete selected spectrum", None))
        self.pushButtonGroupDeleteSpectrum.setText(_translate("mainWindowTabSpectrums", "Group delete selected spectrum", None))
        self.pushButtonGroupAverage.setText(_translate("mainWindowTabSpectrums", "Group average for all subjects", None))
        self.groupBox_5.setTitle(_translate("mainWindowTabSpectrums", "Saving:", None))
        self.pushButtonSaveSpectrum.setText(_translate("mainWindowTabSpectrums", "Save spectrum data", None))
        self.pushButtonGroupSaveSpectrum.setText(_translate("mainWindowTabSpectrums", "Group save spectrum data", None))

