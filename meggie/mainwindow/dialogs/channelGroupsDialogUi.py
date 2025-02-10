# Form implementation generated from reading ui file './meggie/mainwindow/dialogs/channelGroupsDialogUi.ui'
#
# Created by: PyQt6 UI code generator 6.8.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtWidgets


class Ui_channelGroupsDialog(object):
    def setupUi(self, channelGroupsDialog):
        channelGroupsDialog.setObjectName("channelGroupsDialog")
        channelGroupsDialog.resize(398, 324)
        self.gridLayout = QtWidgets.QGridLayout(channelGroupsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.scrollArea = QtWidgets.QScrollArea(parent=channelGroupsDialog)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scrollArea.setHorizontalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.scrollArea.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 378, 273))
        self.scrollAreaWidgetContents.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBoxChannelGroups = QtWidgets.QGroupBox(
            parent=self.scrollAreaWidgetContents
        )
        self.groupBoxChannelGroups.setObjectName("groupBoxChannelGroups")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxChannelGroups)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.pushButtonSetChannels = QtWidgets.QPushButton(
            parent=self.groupBoxChannelGroups
        )
        self.pushButtonSetChannels.setObjectName("pushButtonSetChannels")
        self.gridLayout_3.addWidget(self.pushButtonSetChannels, 4, 1, 1, 1)
        self.pushButtonAdd = QtWidgets.QPushButton(parent=self.groupBoxChannelGroups)
        self.pushButtonAdd.setObjectName("pushButtonAdd")
        self.gridLayout_3.addWidget(self.pushButtonAdd, 0, 1, 1, 1)
        self.listWidgetChannelGroups = QtWidgets.QListWidget(
            parent=self.groupBoxChannelGroups
        )
        self.listWidgetChannelGroups.setObjectName("listWidgetChannelGroups")
        self.gridLayout_3.addWidget(self.listWidgetChannelGroups, 2, 0, 3, 1)
        self.pushButtonRemove = QtWidgets.QPushButton(parent=self.groupBoxChannelGroups)
        self.pushButtonRemove.setObjectName("pushButtonRemove")
        self.gridLayout_3.addWidget(self.pushButtonRemove, 2, 1, 1, 1)
        self.lineEditAdd = QtWidgets.QLineEdit(parent=self.groupBoxChannelGroups)
        self.lineEditAdd.setObjectName("lineEditAdd")
        self.gridLayout_3.addWidget(self.lineEditAdd, 0, 0, 1, 1)
        self.pushButtonReset = QtWidgets.QPushButton(parent=self.groupBoxChannelGroups)
        self.pushButtonReset.setObjectName("pushButtonReset")
        self.gridLayout_3.addWidget(self.pushButtonReset, 3, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxChannelGroups, 1, 0, 1, 1)
        self.groupBoxChannelType = QtWidgets.QGroupBox(
            parent=self.scrollAreaWidgetContents
        )
        self.groupBoxChannelType.setObjectName("groupBoxChannelType")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.groupBoxChannelType)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.radioButtonMEG = QtWidgets.QRadioButton(parent=self.groupBoxChannelType)
        self.radioButtonMEG.setChecked(True)
        self.radioButtonMEG.setObjectName("radioButtonMEG")
        self.horizontalLayout_2.addWidget(self.radioButtonMEG)
        self.radioButtonEEG = QtWidgets.QRadioButton(parent=self.groupBoxChannelType)
        self.radioButtonEEG.setObjectName("radioButtonEEG")
        self.horizontalLayout_2.addWidget(self.radioButtonEEG)
        self.gridLayout_5.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBoxChannelType, 0, 0, 1, 2)
        spacerItem = QtWidgets.QSpacerItem(
            20,
            40,
            QtWidgets.QSizePolicy.Policy.Minimum,
            QtWidgets.QSizePolicy.Policy.Expanding,
        )
        self.gridLayout_2.addItem(spacerItem, 2, 0, 1, 1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(
            40,
            20,
            QtWidgets.QSizePolicy.Policy.Expanding,
            QtWidgets.QSizePolicy.Policy.Minimum,
        )
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonCancel = QtWidgets.QPushButton(parent=channelGroupsDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonApply = QtWidgets.QPushButton(parent=channelGroupsDialog)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(channelGroupsDialog)
        self.pushButtonCancel.clicked.connect(channelGroupsDialog.reject)  # type: ignore
        self.pushButtonApply.clicked.connect(channelGroupsDialog.accept)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(channelGroupsDialog)
        channelGroupsDialog.setTabOrder(self.pushButtonCancel, self.pushButtonApply)
        channelGroupsDialog.setTabOrder(self.pushButtonApply, self.scrollArea)
        channelGroupsDialog.setTabOrder(self.scrollArea, self.radioButtonMEG)
        channelGroupsDialog.setTabOrder(self.radioButtonMEG, self.radioButtonEEG)
        channelGroupsDialog.setTabOrder(self.radioButtonEEG, self.lineEditAdd)
        channelGroupsDialog.setTabOrder(self.lineEditAdd, self.pushButtonAdd)
        channelGroupsDialog.setTabOrder(
            self.pushButtonAdd, self.listWidgetChannelGroups
        )
        channelGroupsDialog.setTabOrder(
            self.listWidgetChannelGroups, self.pushButtonRemove
        )
        channelGroupsDialog.setTabOrder(self.pushButtonRemove, self.pushButtonReset)
        channelGroupsDialog.setTabOrder(
            self.pushButtonReset, self.pushButtonSetChannels
        )

    def retranslateUi(self, channelGroupsDialog):
        _translate = QtCore.QCoreApplication.translate
        channelGroupsDialog.setWindowTitle(
            _translate("channelGroupsDialog", "Meggie - Channel groups")
        )
        self.groupBoxChannelGroups.setTitle(
            _translate("channelGroupsDialog", "Channel groups:")
        )
        self.pushButtonSetChannels.setText(
            _translate("channelGroupsDialog", "Set channels")
        )
        self.pushButtonAdd.setText(_translate("channelGroupsDialog", "Add"))
        self.pushButtonRemove.setText(
            _translate("channelGroupsDialog", "Remove selected")
        )
        self.pushButtonReset.setText(
            _translate("channelGroupsDialog", "Reset to defaults")
        )
        self.groupBoxChannelType.setTitle(
            _translate("channelGroupsDialog", "Select channel type:")
        )
        self.radioButtonMEG.setText(_translate("channelGroupsDialog", "MEG"))
        self.radioButtonEEG.setText(_translate("channelGroupsDialog", "EEG"))
        self.pushButtonCancel.setText(_translate("channelGroupsDialog", "Cancel"))
        self.pushButtonApply.setText(_translate("channelGroupsDialog", "Apply"))
