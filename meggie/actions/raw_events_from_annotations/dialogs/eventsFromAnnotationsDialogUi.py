# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'eventsFromAnnotationsDialogUi.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets


class Ui_EventsFromAnnotationsDialog(object):
    def setupUi(self, EventsFromAnnotationsDialog):
        EventsFromAnnotationsDialog.setObjectName("EventsFromAnnotationsDialog")
        EventsFromAnnotationsDialog.resize(406, 540)
        self.gridLayout = QtWidgets.QGridLayout(EventsFromAnnotationsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(EventsFromAnnotationsDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 372, 655))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxConfiguration = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxConfiguration.setObjectName("groupBoxConfiguration")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxConfiguration)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelAnnotation = QtWidgets.QLabel(self.groupBoxConfiguration)
        self.labelAnnotation.setObjectName("labelAnnotation")
        self.gridLayout_3.addWidget(self.labelAnnotation, 0, 0, 1, 1)
        self.labelLocation = QtWidgets.QLabel(self.groupBoxConfiguration)
        self.labelLocation.setObjectName("labelLocation")
        self.gridLayout_3.addWidget(self.labelLocation, 1, 0, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(self.groupBoxConfiguration)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout_3.addWidget(self.pushButtonAdd, 8, 0, 1, 2)
        self.radioButtonEnd = QtWidgets.QRadioButton(self.groupBoxConfiguration)
        self.radioButtonEnd.setObjectName("radioButtonEnd")
        self.gridLayout_3.addWidget(self.radioButtonEnd, 2, 1, 1, 1)
        self.radioButtonStart = QtWidgets.QRadioButton(self.groupBoxConfiguration)
        self.radioButtonStart.setChecked(True)
        self.radioButtonStart.setObjectName("radioButtonStart")
        self.gridLayout_3.addWidget(self.radioButtonStart, 1, 1, 1, 1)
        self.comboBoxAnnotation = QtWidgets.QComboBox(self.groupBoxConfiguration)
        self.comboBoxAnnotation.setObjectName("comboBoxAnnotation")
        self.gridLayout_3.addWidget(self.comboBoxAnnotation, 0, 1, 1, 1)
        self.labelEventID = QtWidgets.QLabel(self.groupBoxConfiguration)
        self.labelEventID.setObjectName("labelEventID")
        self.gridLayout_3.addWidget(self.labelEventID, 3, 0, 1, 1)
        self.spinBoxEventID = QtWidgets.QSpinBox(self.groupBoxConfiguration)
        self.spinBoxEventID.setMinimum(1)
        self.spinBoxEventID.setMaximum(1000000)
        self.spinBoxEventID.setObjectName("spinBoxEventID")
        self.gridLayout_3.addWidget(self.spinBoxEventID, 3, 1, 1, 1)
        self.listWidgetItems = QtWidgets.QListWidget(self.groupBoxConfiguration)
        self.listWidgetItems.setObjectName("listWidgetItems")
        self.gridLayout_3.addWidget(self.listWidgetItems, 10, 0, 1, 2)
        self.pushButtonClear = QtWidgets.QPushButton(self.groupBoxConfiguration)
        self.pushButtonClear.setObjectName("pushButtonClear")
        self.gridLayout_3.addWidget(self.pushButtonClear, 11, 0, 1, 2)
        self.gridLayout_2.addWidget(self.groupBoxConfiguration, 0, 0, 1, 1)
        self.groupBoxBatching = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBoxBatching.setObjectName("groupBoxBatching")
        self.gridLayoutBatching = QtWidgets.QGridLayout(self.groupBoxBatching)
        self.gridLayoutBatching.setObjectName("gridLayoutBatching")
        self.batchingWidgetPlaceholder = QtWidgets.QWidget(self.groupBoxBatching)
        self.batchingWidgetPlaceholder.setMinimumSize(QtCore.QSize(300, 300))
        self.batchingWidgetPlaceholder.setObjectName("batchingWidgetPlaceholder")
        self.gridLayoutBatching.addWidget(self.batchingWidgetPlaceholder, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxBatching, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding
        )
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(EventsFromAnnotationsDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonBatch = QtWidgets.QPushButton(EventsFromAnnotationsDialog)
        self.pushButtonBatch.setObjectName("pushButtonBatch")
        self.horizontalLayout.addWidget(self.pushButtonBatch)
        self.pushButtonApply = QtWidgets.QPushButton(EventsFromAnnotationsDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(EventsFromAnnotationsDialog)
        self.pushButtonCancel.clicked.connect(EventsFromAnnotationsDialog.reject)
        self.pushButtonApply.clicked.connect(EventsFromAnnotationsDialog.accept)
        self.pushButtonBatch.clicked.connect(EventsFromAnnotationsDialog.acceptBatch)
        QtCore.QMetaObject.connectSlotsByName(EventsFromAnnotationsDialog)

    def retranslateUi(self, EventsFromAnnotationsDialog):
        _translate = QtCore.QCoreApplication.translate
        EventsFromAnnotationsDialog.setWindowTitle(
            _translate(
                "EventsFromAnnotationsDialog", "Meggie - Events from annotations"
            )
        )
        self.groupBoxConfiguration.setTitle(
            _translate("EventsFromAnnotationsDialog", "Configuration:")
        )
        self.labelAnnotation.setText(
            _translate("EventsFromAnnotationsDialog", "Annotation:")
        )
        self.labelLocation.setText(_translate("EventsFromAnnotationsDialog", "Use:"))
        self.pushButtonAdd.setText(
            _translate("EventsFromAnnotationsDialog", "Add to list")
        )
        self.radioButtonEnd.setText(_translate("EventsFromAnnotationsDialog", "End"))
        self.radioButtonStart.setText(
            _translate("EventsFromAnnotationsDialog", "Start")
        )
        self.labelEventID.setText(
            _translate("EventsFromAnnotationsDialog", "Event id:")
        )
        self.pushButtonClear.setText(_translate("EventsFromAnnotationsDialog", "Clear"))
        self.groupBoxBatching.setTitle(
            _translate("EventsFromAnnotationsDialog", "Batching:")
        )
        self.pushButtonCancel.setText(
            _translate("EventsFromAnnotationsDialog", "Cancel")
        )
        self.pushButtonBatch.setText(_translate("EventsFromAnnotationsDialog", "Batch"))
        self.pushButtonApply.setText(_translate("EventsFromAnnotationsDialog", "Apply"))
