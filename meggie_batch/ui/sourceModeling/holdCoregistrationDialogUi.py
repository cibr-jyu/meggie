# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/holdCoregistrationDialog.ui'
#
# Created: Wed Nov 12 11:56:42 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_DialogHoldCoregistration(object):
    def setupUi(self, DialogHoldCoregistration):
        DialogHoldCoregistration.setObjectName(_fromUtf8("DialogHoldCoregistration"))
        DialogHoldCoregistration.resize(565, 368)
        self.formLayout = QtGui.QFormLayout(DialogHoldCoregistration)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelCoregInfo = QtGui.QLabel(DialogHoldCoregistration)
        self.labelCoregInfo.setWordWrap(True)
        self.labelCoregInfo.setObjectName(_fromUtf8("labelCoregInfo"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.labelCoregInfo)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonCancel = QtGui.QPushButton(DialogHoldCoregistration)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonCopy = QtGui.QPushButton(DialogHoldCoregistration)
        self.pushButtonCopy.setObjectName(_fromUtf8("pushButtonCopy"))
        self.horizontalLayout.addWidget(self.pushButtonCopy)
        self.formLayout.setLayout(4, QtGui.QFormLayout.SpanningRole, self.horizontalLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(1, QtGui.QFormLayout.LabelRole, spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtGui.QFormLayout.LabelRole, spacerItem1)
        self.labelTransFileWarning = QtGui.QLabel(DialogHoldCoregistration)
        self.labelTransFileWarning.setEnabled(True)
        self.labelTransFileWarning.setWordWrap(True)
        self.labelTransFileWarning.setObjectName(_fromUtf8("labelTransFileWarning"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.labelTransFileWarning)

        self.retranslateUi(DialogHoldCoregistration)
        QtCore.QMetaObject.connectSlotsByName(DialogHoldCoregistration)

    def retranslateUi(self, DialogHoldCoregistration):
        DialogHoldCoregistration.setWindowTitle(_translate("DialogHoldCoregistration", "Coregistering with MNE-Python coregistration gui", None))
        self.labelCoregInfo.setText(_translate("DialogHoldCoregistration", "<html><head/><body><p>An MNE-Python user interface for coregistration has been opened. Please note the following to ensure that everything works smoothly:</p><p>1) &quot;MRI Subject&quot; and &quot;Head Shape Source&quot; files are automatically set to right files by Meggie. You should not mess with them.</p><p>2) If you also want to save the fiducials file elsewhere (&quot;Save as...&quot; in &quot;MRI Fiducials&quot; box), you can do that too, as long as you also save the file to the default location.</p><p>3) The MNE-Python coregistration user interface does not automatically copy the translated coordinate file to the right place for Meggie. To ensure that the file gets copied, please click &quot;Copy coordinate file&quot; button in this dialog AFTER you have finished the coregistration and saved the coordinate file to the default location (the final &quot;Save as...&quot; button in the coregistration tab). You can also save the file elsewhere after that, if you wish.</p></body></html>", None))
        self.pushButtonCancel.setText(_translate("DialogHoldCoregistration", "Cancel", None))
        self.pushButtonCopy.setText(_translate("DialogHoldCoregistration", "Copy coordinate file", None))
        self.labelTransFileWarning.setText(_translate("DialogHoldCoregistration", "<html><head/><body><p><span style=\" color:#ff0000;\">No translation file found. Are you sure you have saved it to the default location provided by the final &quot;Save as...&quot; button?</span></p></body></html>", None))

