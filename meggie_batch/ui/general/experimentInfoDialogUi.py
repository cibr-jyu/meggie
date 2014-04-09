# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kpaliran/Hoksotin/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/experimentInfoDialog.ui'
#
# Created: Wed Apr  9 19:41:39 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_experimentInfoDialog(object):
    def setupUi(self, experimentInfoDialog):
        experimentInfoDialog.setObjectName(_fromUtf8("experimentInfoDialog"))
        experimentInfoDialog.resize(359, 530)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(experimentInfoDialog.sizePolicy().hasHeightForWidth())
        experimentInfoDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QtGui.QVBoxLayout(experimentInfoDialog)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBoxExperimentInfo = QtGui.QGroupBox(experimentInfoDialog)
        self.groupBoxExperimentInfo.setObjectName(_fromUtf8("groupBoxExperimentInfo"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBoxExperimentInfo)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.formLayout_4 = QtGui.QFormLayout()
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.labelExperiment = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelExperiment.setObjectName(_fromUtf8("labelExperiment"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelExperiment)
        self.labelExperimentName = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelExperimentName.setObjectName(_fromUtf8("labelExperimentName"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.labelExperimentName)
        self.verticalLayout_4.addLayout(self.formLayout_4)
        self.formLayout_5 = QtGui.QFormLayout()
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.labelAuthor = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelAuthor.setObjectName(_fromUtf8("labelAuthor"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelAuthor)
        self.labelAuthorName = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelAuthorName.setObjectName(_fromUtf8("labelAuthorName"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.labelAuthorName)
        self.verticalLayout_4.addLayout(self.formLayout_5)
        self.gridLayout_5.addLayout(self.verticalLayout_4, 0, 0, 1, 1)
        self.labelDescription = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
        self.gridLayout_5.addWidget(self.labelDescription, 1, 0, 1, 1)
        self.textBrowserExperimentDescription = QtGui.QTextBrowser(self.groupBoxExperimentInfo)
        self.textBrowserExperimentDescription.setObjectName(_fromUtf8("textBrowserExperimentDescription"))
        self.gridLayout_5.addWidget(self.textBrowserExperimentDescription, 2, 0, 1, 1)
        self.verticalLayout_6.addWidget(self.groupBoxExperimentInfo)
        self.ButtonClose = QtGui.QPushButton(experimentInfoDialog)
        self.ButtonClose.setObjectName(_fromUtf8("ButtonClose"))
        self.verticalLayout_6.addWidget(self.ButtonClose)

        self.retranslateUi(experimentInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(experimentInfoDialog)

    def retranslateUi(self, experimentInfoDialog):
        experimentInfoDialog.setWindowTitle(_translate("experimentInfoDialog", "Experiment info", None))
        self.groupBoxExperimentInfo.setTitle(_translate("experimentInfoDialog", "Experiment info", None))
        self.labelExperiment.setText(_translate("experimentInfoDialog", "Name:", None))
        self.labelExperimentName.setText(_translate("experimentInfoDialog", "TextLabel", None))
        self.labelAuthor.setText(_translate("experimentInfoDialog", "Author:", None))
        self.labelAuthorName.setText(_translate("experimentInfoDialog", "TextLabel", None))
        self.labelDescription.setText(_translate("experimentInfoDialog", "Description:", None))
        self.ButtonClose.setText(_translate("experimentInfoDialog", "Close", None))

