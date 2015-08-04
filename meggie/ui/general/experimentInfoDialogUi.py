# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kpaliran/Hoksotin/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/experimentInfoDialog.ui'
#
# Created: Wed Apr  9 20:35:06 2014
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
        experimentInfoDialog.resize(584, 530)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(experimentInfoDialog.sizePolicy().hasHeightForWidth())
        experimentInfoDialog.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QtGui.QVBoxLayout(experimentInfoDialog)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBoxExperimentInfo = QtGui.QGroupBox(experimentInfoDialog)
        self.groupBoxExperimentInfo.setObjectName(_fromUtf8("groupBoxExperimentInfo"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxExperimentInfo)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.labelExperiment = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelExperiment.setObjectName(_fromUtf8("labelExperiment"))
        self.gridLayout.addWidget(self.labelExperiment, 0, 0, 1, 1)
        self.lineEditExperimentName = QtGui.QLineEdit(self.groupBoxExperimentInfo)
        self.lineEditExperimentName.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditExperimentName.setReadOnly(True)
        self.lineEditExperimentName.setObjectName(_fromUtf8("lineEditExperimentName"))
        self.gridLayout.addWidget(self.lineEditExperimentName, 0, 1, 1, 1)
        self.labelAuthor = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelAuthor.setObjectName(_fromUtf8("labelAuthor"))
        self.gridLayout.addWidget(self.labelAuthor, 1, 0, 1, 1)
        self.lineEditExperimentAuthor = QtGui.QLineEdit(self.groupBoxExperimentInfo)
        self.lineEditExperimentAuthor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEditExperimentAuthor.setReadOnly(True)
        self.lineEditExperimentAuthor.setObjectName(_fromUtf8("lineEditExperimentAuthor"))
        self.gridLayout.addWidget(self.lineEditExperimentAuthor, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.line = QtGui.QFrame(self.groupBoxExperimentInfo)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_2.addWidget(self.line, 1, 0, 1, 1)
        self.labelDescription = QtGui.QLabel(self.groupBoxExperimentInfo)
        self.labelDescription.setObjectName(_fromUtf8("labelDescription"))
        self.gridLayout_2.addWidget(self.labelDescription, 2, 0, 1, 1)
        self.textBrowserExperimentDescription = QtGui.QTextBrowser(self.groupBoxExperimentInfo)
        self.textBrowserExperimentDescription.setObjectName(_fromUtf8("textBrowserExperimentDescription"))
        self.gridLayout_2.addWidget(self.textBrowserExperimentDescription, 3, 0, 1, 1)
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
        self.labelAuthor.setText(_translate("experimentInfoDialog", "Author:", None))
        self.labelDescription.setText(_translate("experimentInfoDialog", "Description:", None))
        self.ButtonClose.setText(_translate("experimentInfoDialog", "Close", None))

