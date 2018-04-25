# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindowTabInducedUi.ui'
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

class Ui_mainWindowTabInduced(object):
    def setupUi(self, mainWindowTabInduced):
        mainWindowTabInduced.setObjectName(_fromUtf8("mainWindowTabInduced"))
        mainWindowTabInduced.resize(1112, 732)
        self.layoutWidget = QtGui.QWidget(mainWindowTabInduced)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 981, 711))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_15 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_15.setObjectName(_fromUtf8("gridLayout_15"))
        self.verticalLayout_23 = QtGui.QVBoxLayout()
        self.verticalLayout_23.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.verticalLayout_23.setObjectName(_fromUtf8("verticalLayout_23"))
        self.groupBoxEpochs = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxEpochs.setTitle(_fromUtf8(""))
        self.groupBoxEpochs.setObjectName(_fromUtf8("groupBoxEpochs"))
        self.verticalLayout_23.addWidget(self.groupBoxEpochs)
        self.groupBoxComputations = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxComputations.setMinimumSize(QtCore.QSize(400, 0))
        self.groupBoxComputations.setObjectName(_fromUtf8("groupBoxComputations"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxComputations)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButtonComputeTFR = QtGui.QPushButton(self.groupBoxComputations)
        self.pushButtonComputeTFR.setObjectName(_fromUtf8("pushButtonComputeTFR"))
        self.gridLayout_2.addWidget(self.pushButtonComputeTFR, 0, 0, 1, 1)
        self.verticalLayout_23.addWidget(self.groupBoxComputations)
        self.gridLayout_15.addLayout(self.verticalLayout_23, 0, 0, 1, 1)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBoxTFR = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxTFR.setMinimumSize(QtCore.QSize(0, 300))
        self.groupBoxTFR.setObjectName(_fromUtf8("groupBoxTFR"))
        self.formLayout = QtGui.QFormLayout(self.groupBoxTFR)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelTFRInfo = QtGui.QLabel(self.groupBoxTFR)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.labelTFRInfo.setFont(font)
        self.labelTFRInfo.setObjectName(_fromUtf8("labelTFRInfo"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelTFRInfo)
        self.listWidgetTFR = QtGui.QListWidget(self.groupBoxTFR)
        self.listWidgetTFR.setObjectName(_fromUtf8("listWidgetTFR"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.listWidgetTFR)
        self.textBrowserTFRInfo = QtGui.QTextBrowser(self.groupBoxTFR)
        self.textBrowserTFRInfo.setObjectName(_fromUtf8("textBrowserTFRInfo"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.textBrowserTFRInfo)
        self.verticalLayout_6.addWidget(self.groupBoxTFR)
        self.groupBoxTFRActions = QtGui.QGroupBox(self.layoutWidget)
        self.groupBoxTFRActions.setObjectName(_fromUtf8("groupBoxTFRActions"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBoxTFRActions)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBoxTFRActions)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_21 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_21.setObjectName(_fromUtf8("gridLayout_21"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pushButtonVisualizeTFR = QtGui.QPushButton(self.groupBox_2)
        self.pushButtonVisualizeTFR.setObjectName(_fromUtf8("pushButtonVisualizeTFR"))
        self.horizontalLayout_2.addWidget(self.pushButtonVisualizeTFR)
        self.gridLayout_21.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButtonDeleteTFR = QtGui.QPushButton(self.groupBoxTFRActions)
        self.pushButtonDeleteTFR.setObjectName(_fromUtf8("pushButtonDeleteTFR"))
        self.gridLayout.addWidget(self.pushButtonDeleteTFR, 1, 0, 1, 1)
        self.pushButtonGroupAverage = QtGui.QPushButton(self.groupBoxTFRActions)
        self.pushButtonGroupAverage.setObjectName(_fromUtf8("pushButtonGroupAverage"))
        self.gridLayout.addWidget(self.pushButtonGroupAverage, 0, 0, 1, 1)
        self.pushButtonGroupDeleteTFR = QtGui.QPushButton(self.groupBoxTFRActions)
        self.pushButtonGroupDeleteTFR.setObjectName(_fromUtf8("pushButtonGroupDeleteTFR"))
        self.gridLayout.addWidget(self.pushButtonGroupDeleteTFR, 2, 0, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(self.groupBoxTFRActions)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_20 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_20.setObjectName(_fromUtf8("gridLayout_20"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.pushButtonSaveTFR = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonSaveTFR.setObjectName(_fromUtf8("pushButtonSaveTFR"))
        self.horizontalLayout_3.addWidget(self.pushButtonSaveTFR)
        self.pushButtonGroupSaveTFR = QtGui.QPushButton(self.groupBox_5)
        self.pushButtonGroupSaveTFR.setObjectName(_fromUtf8("pushButtonGroupSaveTFR"))
        self.horizontalLayout_3.addWidget(self.pushButtonGroupSaveTFR)
        self.gridLayout_20.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_5, 2, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBoxTFRActions)
        self.gridLayout_15.addLayout(self.verticalLayout_6, 0, 1, 1, 1)

        self.retranslateUi(mainWindowTabInduced)
        QtCore.QMetaObject.connectSlotsByName(mainWindowTabInduced)

    def retranslateUi(self, mainWindowTabInduced):
        mainWindowTabInduced.setWindowTitle(_translate("mainWindowTabInduced", "Form", None))
        self.groupBoxComputations.setTitle(_translate("mainWindowTabInduced", "Computations", None))
        self.pushButtonComputeTFR.setText(_translate("mainWindowTabInduced", "Compute TFR...", None))
        self.groupBoxTFR.setTitle(_translate("mainWindowTabInduced", "TFR\'s", None))
        self.labelTFRInfo.setText(_translate("mainWindowTabInduced", "TFR info", None))
        self.groupBoxTFRActions.setTitle(_translate("mainWindowTabInduced", "Available actions for TFR\'s:", None))
        self.groupBox_2.setTitle(_translate("mainWindowTabInduced", "Visualization:", None))
        self.pushButtonVisualizeTFR.setText(_translate("mainWindowTabInduced", "Visualize selected TFR", None))
        self.pushButtonDeleteTFR.setText(_translate("mainWindowTabInduced", "Delete selected TFR", None))
        self.pushButtonGroupAverage.setText(_translate("mainWindowTabInduced", "Group average for all subjects", None))
        self.pushButtonGroupDeleteTFR.setText(_translate("mainWindowTabInduced", "Group delete selected TFR", None))
        self.groupBox_5.setTitle(_translate("mainWindowTabInduced", "Saving:", None))
        self.pushButtonSaveTFR.setText(_translate("mainWindowTabInduced", "Save TFR data", None))
        self.pushButtonGroupSaveTFR.setText(_translate("mainWindowTabInduced", "Group save TFR data", None))

