# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'icaDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(517, 647)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.bottomLayout = QtWidgets.QHBoxLayout()
        self.bottomLayout.setObjectName("bottomLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.bottomLayout.addItem(spacerItem)
        self.pushButtonCancel = QtWidgets.QPushButton(Dialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.bottomLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.pushButtonApply.sizePolicy().hasHeightForWidth()
        )
        self.pushButtonApply.setSizePolicy(sizePolicy)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.bottomLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.bottomLayout, 1, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 499, 587))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.groupBoxComputation = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxComputation.setObjectName("groupBoxComputation")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxComputation)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.parametersLayout = QtWidgets.QGridLayout()
        self.parametersLayout.setObjectName("parametersLayout")
        self.spinBoxMaxIter = QtWidgets.QSpinBox(self.groupBoxComputation)
        self.spinBoxMaxIter.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxMaxIter.setMinimum(1)
        self.spinBoxMaxIter.setMaximum(10000000)
        self.spinBoxMaxIter.setProperty("value", 2000)
        self.spinBoxMaxIter.setObjectName("spinBoxMaxIter")
        self.parametersLayout.addWidget(self.spinBoxMaxIter, 1, 1, 1, 1)
        self.labelNComponents = QtWidgets.QLabel(self.groupBoxComputation)
        self.labelNComponents.setObjectName("labelNComponents")
        self.parametersLayout.addWidget(self.labelNComponents, 0, 0, 1, 1)
        self.doubleSpinBoxNComponents = QtWidgets.QDoubleSpinBox(
            self.groupBoxComputation
        )
        self.doubleSpinBoxNComponents.setSuffix("")
        self.doubleSpinBoxNComponents.setDecimals(3)
        self.doubleSpinBoxNComponents.setMaximum(1000.0)
        self.doubleSpinBoxNComponents.setSingleStep(0.1)
        self.doubleSpinBoxNComponents.setProperty("value", 0.95)
        self.doubleSpinBoxNComponents.setObjectName("doubleSpinBoxNComponents")
        self.parametersLayout.addWidget(self.doubleSpinBoxNComponents, 0, 1, 1, 1)
        self.labelMaxIter = QtWidgets.QLabel(self.groupBoxComputation)
        self.labelMaxIter.setScaledContents(False)
        self.labelMaxIter.setObjectName("labelMaxIter")
        self.parametersLayout.addWidget(self.labelMaxIter, 1, 0, 1, 1)
        self.gridLayout_4.addLayout(self.parametersLayout, 0, 0, 1, 1)
        self.pushButtonCompute = QtWidgets.QPushButton(self.groupBoxComputation)
        self.pushButtonCompute.setObjectName("pushButtonCompute")
        self.gridLayout_4.addWidget(self.pushButtonCompute, 1, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBoxComputation, 0, 0, 1, 1)
        self.groupBoxComponents = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxComponents.setObjectName("groupBoxComponents")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.groupBoxComponents)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.labelNotRemoved = QtWidgets.QLabel(self.groupBoxComponents)
        self.labelNotRemoved.setObjectName("labelNotRemoved")
        self.gridLayout_2.addWidget(self.labelNotRemoved, 0, 0, 1, 1)
        self.listWidgetNotRemoved = QtWidgets.QListWidget(self.groupBoxComponents)
        self.listWidgetNotRemoved.setObjectName("listWidgetNotRemoved")
        self.gridLayout_2.addWidget(self.listWidgetNotRemoved, 1, 0, 1, 1)
        self.listWidgetRemoved = QtWidgets.QListWidget(self.groupBoxComponents)
        self.listWidgetRemoved.setObjectName("listWidgetRemoved")
        self.gridLayout_2.addWidget(self.listWidgetRemoved, 4, 0, 1, 1)
        self.labelRemoved = QtWidgets.QLabel(self.groupBoxComponents)
        self.labelRemoved.setObjectName("labelRemoved")
        self.gridLayout_2.addWidget(self.labelRemoved, 3, 0, 1, 1)
        self.pushButtonTransfer = QtWidgets.QPushButton(self.groupBoxComponents)
        self.pushButtonTransfer.setObjectName("pushButtonTransfer")
        self.gridLayout_2.addWidget(self.pushButtonTransfer, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonPlotProperties = QtWidgets.QPushButton(self.groupBoxComponents)
        self.pushButtonPlotProperties.setObjectName("pushButtonPlotProperties")
        self.gridLayout_3.addWidget(self.pushButtonPlotProperties, 2, 0, 1, 1)
        self.pushButtonPlotChanges = QtWidgets.QPushButton(self.groupBoxComponents)
        self.pushButtonPlotChanges.setObjectName("pushButtonPlotChanges")
        self.gridLayout_3.addWidget(self.pushButtonPlotChanges, 3, 0, 1, 1)
        self.pushButtonPlotSources = QtWidgets.QPushButton(self.groupBoxComponents)
        self.pushButtonPlotSources.setObjectName("pushButtonPlotSources")
        self.gridLayout_3.addWidget(self.pushButtonPlotSources, 0, 0, 1, 1)
        self.pushButtonPlotTopographies = QtWidgets.QPushButton(self.groupBoxComponents)
        self.pushButtonPlotTopographies.setObjectName("pushButtonPlotTopographies")
        self.gridLayout_3.addWidget(self.pushButtonPlotTopographies, 1, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)
        self.gridLayout_7.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.groupBoxComponents, 1, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.pushButtonCancel.clicked.connect(Dialog.reject)
        self.pushButtonApply.clicked.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Meggie - ICA"))
        self.pushButtonCancel.setText(_translate("Dialog", "Cancel"))
        self.pushButtonApply.setText(_translate("Dialog", "Apply"))
        self.groupBoxComputation.setTitle(_translate("Dialog", "ICA computation"))
        self.labelNComponents.setText(_translate("Dialog", "Explained variance:"))
        self.labelMaxIter.setText(
            _translate("Dialog", "Maximum number of iterations: ")
        )
        self.pushButtonCompute.setText(_translate("Dialog", "Compute"))
        self.groupBoxComponents.setTitle(_translate("Dialog", "ICA components"))
        self.labelNotRemoved.setText(_translate("Dialog", "Not removed"))
        self.labelRemoved.setText(_translate("Dialog", "Removed"))
        self.pushButtonTransfer.setText(_translate("Dialog", "Transfer"))
        self.pushButtonPlotProperties.setText(_translate("Dialog", "Plot properties"))
        self.pushButtonPlotChanges.setText(_translate("Dialog", "Plot changes"))
        self.pushButtonPlotSources.setText(_translate("Dialog", "Plot time courses"))
        self.pushButtonPlotTopographies.setText(
            _translate("Dialog", "Plot topographies")
        )
