# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Widget.ui'
#
# Created: Mon Mar 11 15:40:16 2013
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(393, 342)
        self.scrollArea = QtGui.QScrollArea(Form)
        self.scrollArea.setGeometry(QtCore.QRect(30, 10, 341, 321))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 339, 319))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.stimChannelComboBox = QtGui.QComboBox(self.scrollAreaWidgetContents)
        self.stimChannelComboBox.setGeometry(QtCore.QRect(94, 191, 85, 31))
        self.stimChannelComboBox.setObjectName(_fromUtf8("stimChannelComboBox"))
        self.PresetComboBox = QtGui.QComboBox(self.scrollAreaWidgetContents)
        self.PresetComboBox.setGeometry(QtCore.QRect(80, 40, 85, 31))
        self.PresetComboBox.setObjectName(_fromUtf8("PresetComboBox"))
        self.eventMarginalMin = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.eventMarginalMin.setGeometry(QtCore.QRect(60, 100, 51, 31))
        self.eventMarginalMin.setText(_fromUtf8(""))
        self.eventMarginalMin.setObjectName(_fromUtf8("eventMarginalMin"))
        self.eventMarginalMax = QtGui.QLineEdit(self.scrollAreaWidgetContents)
        self.eventMarginalMax.setGeometry(QtCore.QRect(60, 140, 51, 31))
        self.eventMarginalMax.setObjectName(_fromUtf8("eventMarginalMax"))
        self.DrawButton = QtGui.QPushButton(self.scrollAreaWidgetContents)
        self.DrawButton.setGeometry(QtCore.QRect(220, 280, 95, 31))
        self.DrawButton.setObjectName(_fromUtf8("DrawButton"))
        self.label = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label.setGeometry(QtCore.QRect(120, 10, 101, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_2.setGeometry(QtCore.QRect(1, 191, 87, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_3.setGeometry(QtCore.QRect(10, 100, 66, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 41, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setGeometry(QtCore.QRect(10, 40, 66, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setGeometry(QtCore.QRect(220, 30, 66, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.EOGcheckBox = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.EOGcheckBox.setGeometry(QtCore.QRect(210, 60, 93, 26))
        self.EOGcheckBox.setObjectName(_fromUtf8("EOGcheckBox"))
        self.ECGCheckBox = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.ECGCheckBox.setGeometry(QtCore.QRect(210, 90, 93, 26))
        self.ECGCheckBox.setObjectName(_fromUtf8("ECGCheckBox"))
        self.StimChannelCheckBox = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.StimChannelCheckBox.setGeometry(QtCore.QRect(210, 120, 111, 26))
        self.StimChannelCheckBox.setObjectName(_fromUtf8("StimChannelCheckBox"))
        self.BadChannelsCheckBox = QtGui.QCheckBox(self.scrollAreaWidgetContents)
        self.BadChannelsCheckBox.setGeometry(QtCore.QRect(210, 150, 121, 26))
        self.BadChannelsCheckBox.setObjectName(_fromUtf8("BadChannelsCheckBox"))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.DrawButton.setText(_translate("Form", "Draw", None))
        self.label.setText(_translate("Form", "Epoch selector", None))
        self.label_2.setText(_translate("Form", "Stim channel:", None))
        self.label_3.setText(_translate("Form", "tmin", None))
        self.label_4.setText(_translate("Form", "tmax", None))
        self.label_5.setText(_translate("Form", "Preset", None))
        self.label_6.setText(_translate("Form", "Show:", None))
        self.EOGcheckBox.setText(_translate("Form", "EOG", None))
        self.ECGCheckBox.setText(_translate("Form", "ECG", None))
        self.StimChannelCheckBox.setText(_translate("Form", "StimChannel", None))
        self.BadChannelsCheckBox.setText(_translate("Form", "BadChannels", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

