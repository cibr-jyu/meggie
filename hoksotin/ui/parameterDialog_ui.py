# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'parameterDialog.ui'
#
# Created: Thu Apr 25 15:49:55 2013
#      by: PyQt4 UI code generator 4.10
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

class Ui_ParameterDialog(object):
    def setupUi(self, ParameterDialog):
        ParameterDialog.setObjectName(_fromUtf8("ParameterDialog"))
        ParameterDialog.setWindowModality(QtCore.Qt.WindowModal)
        ParameterDialog.resize(751, 689)
        self.gridLayout = QtGui.QGridLayout(ParameterDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(ParameterDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.labelStimulus = QtGui.QLabel(self.layoutWidget)
        self.labelStimulus.setObjectName(_fromUtf8("labelStimulus"))
        self.horizontalLayout_2.addWidget(self.labelStimulus)
        self.comboBoxStimulus = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxStimulus.setObjectName(_fromUtf8("comboBoxStimulus"))
        self.horizontalLayout_2.addWidget(self.comboBoxStimulus)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.labelEventID = QtGui.QLabel(self.layoutWidget)
        self.labelEventID.setObjectName(_fromUtf8("labelEventID"))
        self.horizontalLayout_7.addWidget(self.labelEventID)
        self.comboBoxEventID = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxEventID.setObjectName(_fromUtf8("comboBoxEventID"))
        self.horizontalLayout_7.addWidget(self.comboBoxEventID)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.labelTmin = QtGui.QLabel(self.layoutWidget)
        self.labelTmin.setObjectName(_fromUtf8("labelTmin"))
        self.horizontalLayout.addWidget(self.labelTmin)
        self.doubleSpinBoxTmin = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxTmin.setMinimum(-10.0)
        self.doubleSpinBoxTmin.setSingleStep(0.1)
        self.doubleSpinBoxTmin.setProperty("value", -0.2)
        self.doubleSpinBoxTmin.setObjectName(_fromUtf8("doubleSpinBoxTmin"))
        self.horizontalLayout.addWidget(self.doubleSpinBoxTmin)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.labelTmax = QtGui.QLabel(self.layoutWidget)
        self.labelTmax.setObjectName(_fromUtf8("labelTmax"))
        self.horizontalLayout_4.addWidget(self.labelTmax)
        self.doubleSpinBoxTmax = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxTmax.setMaximum(9.9)
        self.doubleSpinBoxTmax.setSingleStep(0.1)
        self.doubleSpinBoxTmax.setProperty("value", 0.5)
        self.doubleSpinBoxTmax.setObjectName(_fromUtf8("doubleSpinBoxTmax"))
        self.horizontalLayout_4.addWidget(self.doubleSpinBoxTmax)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.labelName = QtGui.QLabel(self.layoutWidget)
        self.labelName.setObjectName(_fromUtf8("labelName"))
        self.horizontalLayout_5.addWidget(self.labelName)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.lineEditName = QtGui.QLineEdit(self.layoutWidget)
        self.lineEditName.setObjectName(_fromUtf8("lineEditName"))
        self.horizontalLayout_5.addWidget(self.lineEditName)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelInclude = QtGui.QLabel(self.layoutWidget)
        self.labelInclude.setObjectName(_fromUtf8("labelInclude"))
        self.verticalLayout.addWidget(self.labelInclude)
        self.textEditInclude = QtGui.QTextEdit(self.layoutWidget)
        self.textEditInclude.setObjectName(_fromUtf8("textEditInclude"))
        self.verticalLayout.addWidget(self.textEditInclude)
        self.comboBoxChannelGroup = QtGui.QComboBox(self.layoutWidget)
        self.comboBoxChannelGroup.setObjectName(_fromUtf8("comboBoxChannelGroup"))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.comboBoxChannelGroup.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.comboBoxChannelGroup)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.checkBoxMag = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxMag.setObjectName(_fromUtf8("checkBoxMag"))
        self.horizontalLayout_6.addWidget(self.checkBoxMag)
        self.checkBoxGrad = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxGrad.setObjectName(_fromUtf8("checkBoxGrad"))
        self.horizontalLayout_6.addWidget(self.checkBoxGrad)
        self.checkBoxEeg = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxEeg.setObjectName(_fromUtf8("checkBoxEeg"))
        self.horizontalLayout_6.addWidget(self.checkBoxEeg)
        self.checkBoxStim = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxStim.setObjectName(_fromUtf8("checkBoxStim"))
        self.horizontalLayout_6.addWidget(self.checkBoxStim)
        self.checkBoxEog = QtGui.QCheckBox(self.layoutWidget)
        self.checkBoxEog.setObjectName(_fromUtf8("checkBoxEog"))
        self.horizontalLayout_6.addWidget(self.checkBoxEog)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem1)
        self.labelExclude = QtGui.QLabel(self.layoutWidget)
        self.labelExclude.setObjectName(_fromUtf8("labelExclude"))
        self.verticalLayout_3.addWidget(self.labelExclude)
        self.textEditExclude = QtGui.QTextEdit(self.layoutWidget)
        self.textEditExclude.setObjectName(_fromUtf8("textEditExclude"))
        self.verticalLayout_3.addWidget(self.textEditExclude)
        self.labelRejections = QtGui.QLabel(self.layoutWidget)
        self.labelRejections.setObjectName(_fromUtf8("labelRejections"))
        self.verticalLayout_3.addWidget(self.labelRejections)
        self.horizontalLayout_30 = QtGui.QHBoxLayout()
        self.horizontalLayout_30.setObjectName(_fromUtf8("horizontalLayout_30"))
        self.verticalLayout_7 = QtGui.QVBoxLayout()
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.horizontalLayout_31 = QtGui.QHBoxLayout()
        self.horizontalLayout_31.setObjectName(_fromUtf8("horizontalLayout_31"))
        self.labelGradReject_3 = QtGui.QLabel(self.layoutWidget)
        self.labelGradReject_3.setObjectName(_fromUtf8("labelGradReject_3"))
        self.horizontalLayout_31.addWidget(self.labelGradReject_3)
        self.doubleSpinBoxGradReject_3 = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxGradReject_3.setPrefix(_fromUtf8(""))
        self.doubleSpinBoxGradReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxGradReject_3.setProperty("value", 4000.0)
        self.doubleSpinBoxGradReject_3.setObjectName(_fromUtf8("doubleSpinBoxGradReject_3"))
        self.horizontalLayout_31.addWidget(self.doubleSpinBoxGradReject_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_31)
        self.horizontalLayout_32 = QtGui.QHBoxLayout()
        self.horizontalLayout_32.setObjectName(_fromUtf8("horizontalLayout_32"))
        self.labelEegReject_3 = QtGui.QLabel(self.layoutWidget)
        self.labelEegReject_3.setObjectName(_fromUtf8("labelEegReject_3"))
        self.horizontalLayout_32.addWidget(self.labelEegReject_3)
        self.doubleSpinBoxEEGReject_3 = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxEEGReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxEEGReject_3.setProperty("value", 40.0)
        self.doubleSpinBoxEEGReject_3.setObjectName(_fromUtf8("doubleSpinBoxEEGReject_3"))
        self.horizontalLayout_32.addWidget(self.doubleSpinBoxEEGReject_3)
        self.verticalLayout_7.addLayout(self.horizontalLayout_32)
        self.horizontalLayout_30.addLayout(self.verticalLayout_7)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.horizontalLayout_33 = QtGui.QHBoxLayout()
        self.horizontalLayout_33.setObjectName(_fromUtf8("horizontalLayout_33"))
        self.labelMagReject_3 = QtGui.QLabel(self.layoutWidget)
        self.labelMagReject_3.setObjectName(_fromUtf8("labelMagReject_3"))
        self.horizontalLayout_33.addWidget(self.labelMagReject_3)
        self.doubleSpinBoxMagReject_3 = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxMagReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxMagReject_3.setProperty("value", 4000.0)
        self.doubleSpinBoxMagReject_3.setObjectName(_fromUtf8("doubleSpinBoxMagReject_3"))
        self.horizontalLayout_33.addWidget(self.doubleSpinBoxMagReject_3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_33)
        self.horizontalLayout_34 = QtGui.QHBoxLayout()
        self.horizontalLayout_34.setObjectName(_fromUtf8("horizontalLayout_34"))
        self.labelEogReject_3 = QtGui.QLabel(self.layoutWidget)
        self.labelEogReject_3.setObjectName(_fromUtf8("labelEogReject_3"))
        self.horizontalLayout_34.addWidget(self.labelEogReject_3)
        self.doubleSpinBoxEOGReject_3 = QtGui.QDoubleSpinBox(self.layoutWidget)
        self.doubleSpinBoxEOGReject_3.setMaximum(1000000000.0)
        self.doubleSpinBoxEOGReject_3.setProperty("value", 250.0)
        self.doubleSpinBoxEOGReject_3.setObjectName(_fromUtf8("doubleSpinBoxEOGReject_3"))
        self.horizontalLayout_34.addWidget(self.doubleSpinBoxEOGReject_3)
        self.verticalLayout_8.addLayout(self.horizontalLayout_34)
        self.horizontalLayout_30.addLayout(self.verticalLayout_8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_30)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushButtonAdd = QtGui.QPushButton(self.layoutWidget)
        self.pushButtonAdd.setObjectName(_fromUtf8("pushButtonAdd"))
        self.horizontalLayout_3.addWidget(self.pushButtonAdd)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setMargin(0)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.listWidgetEvents = QtGui.QListWidget(self.layoutWidget1)
        self.listWidgetEvents.setObjectName(_fromUtf8("listWidgetEvents"))
        self.verticalLayout_4.addWidget(self.listWidgetEvents)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.pushButtonRemove = QtGui.QPushButton(self.layoutWidget1)
        self.pushButtonRemove.setEnabled(False)
        self.pushButtonRemove.setObjectName(_fromUtf8("pushButtonRemove"))
        self.horizontalLayout_8.addWidget(self.pushButtonRemove)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem3)
        self.cancelOkButtonBox = QtGui.QDialogButtonBox(self.layoutWidget1)
        self.cancelOkButtonBox.setEnabled(True)
        self.cancelOkButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.cancelOkButtonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cancelOkButtonBox.setObjectName(_fromUtf8("cancelOkButtonBox"))
        self.horizontalLayout_8.addWidget(self.cancelOkButtonBox)
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        self.retranslateUi(ParameterDialog)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ParameterDialog.accept)
        QtCore.QObject.connect(self.cancelOkButtonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ParameterDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ParameterDialog)

    def retranslateUi(self, ParameterDialog):
        ParameterDialog.setWindowTitle(_translate("ParameterDialog", "Give parameters", None))
        self.labelStimulus.setText(_translate("ParameterDialog", "Stimulus channel:", None))
        self.labelEventID.setText(_translate("ParameterDialog", "Event ID:", None))
        self.labelTmin.setText(_translate("ParameterDialog", "Start time:", None))
        self.labelTmax.setText(_translate("ParameterDialog", "End time:", None))
        self.labelName.setText(_translate("ParameterDialog", "Event name:      ", None))
        self.labelInclude.setText(_translate("ParameterDialog", "Include:", None))
        self.comboBoxChannelGroup.setItemText(0, _translate("ParameterDialog", "All", None))
        self.comboBoxChannelGroup.setItemText(1, _translate("ParameterDialog", "Vertex", None))
        self.comboBoxChannelGroup.setItemText(2, _translate("ParameterDialog", "Left-temporal", None))
        self.comboBoxChannelGroup.setItemText(3, _translate("ParameterDialog", "Right-temporal", None))
        self.comboBoxChannelGroup.setItemText(4, _translate("ParameterDialog", "Left-parietal", None))
        self.comboBoxChannelGroup.setItemText(5, _translate("ParameterDialog", "Right-parietal", None))
        self.comboBoxChannelGroup.setItemText(6, _translate("ParameterDialog", "Left-occipital", None))
        self.comboBoxChannelGroup.setItemText(7, _translate("ParameterDialog", "Right-occipital", None))
        self.comboBoxChannelGroup.setItemText(8, _translate("ParameterDialog", "Left-frontal", None))
        self.comboBoxChannelGroup.setItemText(9, _translate("ParameterDialog", "Right-frontal", None))
        self.comboBoxChannelGroup.setItemText(10, _translate("ParameterDialog", "MEG 01-04", None))
        self.comboBoxChannelGroup.setItemText(11, _translate("ParameterDialog", "MEG 05-08", None))
        self.comboBoxChannelGroup.setItemText(12, _translate("ParameterDialog", "MEG 09-12", None))
        self.comboBoxChannelGroup.setItemText(13, _translate("ParameterDialog", "MEG 13-16", None))
        self.comboBoxChannelGroup.setItemText(14, _translate("ParameterDialog", "MEG 17-20", None))
        self.comboBoxChannelGroup.setItemText(15, _translate("ParameterDialog", "MEG 21-24", None))
        self.comboBoxChannelGroup.setItemText(16, _translate("ParameterDialog", "MEG 25-26", None))
        self.checkBoxMag.setText(_translate("ParameterDialog", "mag", None))
        self.checkBoxGrad.setText(_translate("ParameterDialog", "grad", None))
        self.checkBoxEeg.setText(_translate("ParameterDialog", "eeg", None))
        self.checkBoxStim.setText(_translate("ParameterDialog", "stim", None))
        self.checkBoxEog.setText(_translate("ParameterDialog", "eog", None))
        self.labelExclude.setText(_translate("ParameterDialog", "Exclude:", None))
        self.labelRejections.setText(_translate("ParameterDialog", "Rejection parameters", None))
        self.labelGradReject_3.setText(_translate("ParameterDialog", "Grad:", None))
        self.doubleSpinBoxGradReject_3.setSuffix(_translate("ParameterDialog", " fT/cm", None))
        self.labelEegReject_3.setText(_translate("ParameterDialog", "EEG:", None))
        self.doubleSpinBoxEEGReject_3.setSuffix(_translate("ParameterDialog", " uV", None))
        self.labelMagReject_3.setText(_translate("ParameterDialog", "Mag:", None))
        self.doubleSpinBoxMagReject_3.setSuffix(_translate("ParameterDialog", " fT", None))
        self.labelEogReject_3.setText(_translate("ParameterDialog", "EOG:", None))
        self.doubleSpinBoxEOGReject_3.setSuffix(_translate("ParameterDialog", " uV", None))
        self.pushButtonAdd.setText(_translate("ParameterDialog", "Add to list >>", None))
        self.pushButtonRemove.setText(_translate("ParameterDialog", "<< Remove", None))

