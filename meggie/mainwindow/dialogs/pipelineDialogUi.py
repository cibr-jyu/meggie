# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pipelineDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_pipelineDialog(object):
    def setupUi(self, pipelineDialog):
        pipelineDialog.setObjectName("pipelineDialog")
        pipelineDialog.resize(406, 195)
        self.gridLayout = QtWidgets.QGridLayout(pipelineDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(pipelineDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 386, 144))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.groupBoxPipeline = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxPipeline.setObjectName("groupBoxPipeline")
        self.gridLayoutPipeline = QtWidgets.QGridLayout(self.groupBoxPipeline)
        self.gridLayoutPipeline.setObjectName("gridLayoutPipeline")
        self.gridLayout_2.addWidget(self.groupBoxPipeline, 0, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(pipelineDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(pipelineDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(pipelineDialog)
        self.pushButtonCancel.clicked.connect(pipelineDialog.reject)
        self.pushButtonApply.clicked.connect(pipelineDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(pipelineDialog)

    def retranslateUi(self, pipelineDialog):
        _translate = QtCore.QCoreApplication.translate
        pipelineDialog.setWindowTitle(_translate("pipelineDialog", "Meggie - Select pipeline"))
        self.groupBoxPipeline.setTitle(_translate("pipelineDialog", "Select pipeline:"))
        self.pushButtonCancel.setText(_translate("pipelineDialog", "Cancel"))
        self.pushButtonApply.setText(_translate("pipelineDialog", "Apply"))
