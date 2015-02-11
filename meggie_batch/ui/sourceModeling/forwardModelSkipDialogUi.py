# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/kari/Opinnot/gradu/lahdekoodit/lahdekoodit/meggie_batch/ui/qt4Designer_ui_files/forwardModelSkipDialog.ui'
#
# Created: Mon Feb  2 14:17:09 2015
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

class Ui_DialogForwardModelSkip(object):
    def setupUi(self, DialogForwardModelSkip):
        DialogForwardModelSkip.setObjectName(_fromUtf8("DialogForwardModelSkip"))
        DialogForwardModelSkip.resize(542, 591)
        self.formLayout = QtGui.QFormLayout(DialogForwardModelSkip)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        spacerItem = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        self.formLayout.setItem(1, QtGui.QFormLayout.LabelRole, spacerItem)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout.setItem(3, QtGui.QFormLayout.LabelRole, spacerItem1)
        self.frame = QtGui.QFrame(DialogForwardModelSkip)
        self.frame.setMinimumSize(QtCore.QSize(200, 200))
        self.frame.setFrameShape(QtGui.QFrame.NoFrame)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.labelQuestion = QtGui.QLabel(self.frame)
        self.labelQuestion.setMinimumSize(QtCore.QSize(200, 200))
        self.labelQuestion.setWordWrap(True)
        self.labelQuestion.setObjectName(_fromUtf8("labelQuestion"))
        self.gridLayout_4.addWidget(self.labelQuestion, 0, 0, 1, 1)
        self.formLayout.setWidget(0, QtGui.QFormLayout.SpanningRole, self.frame)
        self.groupBox = QtGui.QGroupBox(DialogForwardModelSkip)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBoxSourceSpaceSetup = QtGui.QGroupBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxSourceSpaceSetup.sizePolicy().hasHeightForWidth())
        self.groupBoxSourceSpaceSetup.setSizePolicy(sizePolicy)
        self.groupBoxSourceSpaceSetup.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBoxSourceSpaceSetup.setObjectName(_fromUtf8("groupBoxSourceSpaceSetup"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBoxSourceSpaceSetup)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.labelIco = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelIco.setObjectName(_fromUtf8("labelIco"))
        self.gridLayout_3.addWidget(self.labelIco, 0, 0, 1, 1)
        self.labelIcoValue = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelIcoValue.setEnabled(False)
        self.labelIcoValue.setObjectName(_fromUtf8("labelIcoValue"))
        self.gridLayout_3.addWidget(self.labelIcoValue, 1, 0, 1, 1)
        self.labelCPS = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelCPS.setObjectName(_fromUtf8("labelCPS"))
        self.gridLayout_3.addWidget(self.labelCPS, 6, 0, 1, 1)
        self.labelSpacing = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelSpacing.setEnabled(False)
        self.labelSpacing.setObjectName(_fromUtf8("labelSpacing"))
        self.gridLayout_3.addWidget(self.labelSpacing, 2, 0, 1, 1)
        self.labelSurface = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelSurface.setObjectName(_fromUtf8("labelSurface"))
        self.gridLayout_3.addWidget(self.labelSurface, 4, 0, 1, 1)
        self.labelDecimMethod = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelDecimMethod.setText(_fromUtf8(""))
        self.labelDecimMethod.setObjectName(_fromUtf8("labelDecimMethod"))
        self.gridLayout_3.addWidget(self.labelDecimMethod, 0, 1, 1, 2)
        self.labelSurfaceName = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelSurfaceName.setText(_fromUtf8(""))
        self.labelSurfaceName.setObjectName(_fromUtf8("labelSurfaceName"))
        self.gridLayout_3.addWidget(self.labelSurfaceName, 4, 1, 1, 2)
        self.labelComputePatchStats = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelComputePatchStats.setText(_fromUtf8(""))
        self.labelComputePatchStats.setObjectName(_fromUtf8("labelComputePatchStats"))
        self.gridLayout_3.addWidget(self.labelComputePatchStats, 6, 1, 1, 2)
        self.labelIcoValue_2 = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelIcoValue_2.setEnabled(False)
        self.labelIcoValue_2.setObjectName(_fromUtf8("labelIcoValue_2"))
        self.gridLayout_3.addWidget(self.labelIcoValue_2, 1, 1, 1, 1)
        self.labelSpacing_2 = QtGui.QLabel(self.groupBoxSourceSpaceSetup)
        self.labelSpacing_2.setEnabled(False)
        self.labelSpacing_2.setObjectName(_fromUtf8("labelSpacing_2"))
        self.gridLayout_3.addWidget(self.labelSpacing_2, 2, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBoxSourceSpaceSetup, 0, 0, 1, 1)
        self.groupBoxBemModelMeshes = QtGui.QGroupBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxBemModelMeshes.sizePolicy().hasHeightForWidth())
        self.groupBoxBemModelMeshes.setSizePolicy(sizePolicy)
        self.groupBoxBemModelMeshes.setObjectName(_fromUtf8("groupBoxBemModelMeshes"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBoxBemModelMeshes)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.labelAtlas = QtGui.QLabel(self.groupBoxBemModelMeshes)
        self.labelAtlas.setObjectName(_fromUtf8("labelAtlas"))
        self.gridLayout_2.addWidget(self.labelAtlas, 0, 0, 1, 1)
        self.labelUseAtlas = QtGui.QLabel(self.groupBoxBemModelMeshes)
        self.labelUseAtlas.setText(_fromUtf8(""))
        self.labelUseAtlas.setObjectName(_fromUtf8("labelUseAtlas"))
        self.gridLayout_2.addWidget(self.labelUseAtlas, 0, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBoxBemModelMeshes, 1, 0, 1, 1)
        self.formLayout.setWidget(2, QtGui.QFormLayout.SpanningRole, self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButtonCancel = QtGui.QPushButton(DialogForwardModelSkip)
        self.pushButtonCancel.setObjectName(_fromUtf8("pushButtonCancel"))
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.pushButtonBemOnly = QtGui.QPushButton(DialogForwardModelSkip)
        self.pushButtonBemOnly.setObjectName(_fromUtf8("pushButtonBemOnly"))
        self.horizontalLayout.addWidget(self.pushButtonBemOnly)
        self.pushButtonComputeAll = QtGui.QPushButton(DialogForwardModelSkip)
        self.pushButtonComputeAll.setObjectName(_fromUtf8("pushButtonComputeAll"))
        self.horizontalLayout.addWidget(self.pushButtonComputeAll)
        self.formLayout.setLayout(4, QtGui.QFormLayout.SpanningRole, self.horizontalLayout)

        self.retranslateUi(DialogForwardModelSkip)
        QtCore.QMetaObject.connectSlotsByName(DialogForwardModelSkip)

    def retranslateUi(self, DialogForwardModelSkip):
        DialogForwardModelSkip.setWindowTitle(_translate("DialogForwardModelSkip", "Reuse existing files?", None))
        self.labelQuestion.setText(_translate("DialogForwardModelSkip", "<html><head/><body><p>It seems you already have a setup source space and BEM model meshes created with watershed algorithm. If you don\'t need to create them again, Meggie can reuse them and only setup a new forward model. This will save a considerable amount of time, especially in BEM model meshes creation. You can:<br/></p><p>1) press Cancel to get back to previous dialog to adjust parameters</p><p>2) Press &quot;BEM model setup only&quot; to reuse previously created files for a new forward model (only forward model name and BEM model setup parameters will be used, others are ignored)</p><p>3) Compute all phases again</p></body></html>", None))
        self.groupBox.setTitle(_translate("DialogForwardModelSkip", "Parameters for existing source space and meshes:", None))
        self.groupBoxSourceSpaceSetup.setTitle(_translate("DialogForwardModelSkip", "Source space setup parameters:", None))
        self.labelIco.setText(_translate("DialogForwardModelSkip", "Cortical surface decimation method (ico):", None))
        self.labelIcoValue.setText(_translate("DialogForwardModelSkip", "Ico value:", None))
        self.labelCPS.setText(_translate("DialogForwardModelSkip", "Compute cortical patch statistics:", None))
        self.labelSpacing.setText(_translate("DialogForwardModelSkip", "Spacing:", None))
        self.labelSurface.setText(_translate("DialogForwardModelSkip", "Surface name:", None))
        self.labelIcoValue_2.setText(_translate("DialogForwardModelSkip", "Not used", None))
        self.labelSpacing_2.setText(_translate("DialogForwardModelSkip", "Not used", None))
        self.groupBoxBemModelMeshes.setTitle(_translate("DialogForwardModelSkip", "BEM model meshes (watershed) creation parameters:", None))
        self.labelAtlas.setText(_translate("DialogForwardModelSkip", "Use atlas:", None))
        self.pushButtonCancel.setText(_translate("DialogForwardModelSkip", "Cancel", None))
        self.pushButtonBemOnly.setText(_translate("DialogForwardModelSkip", "Bem model \n"
" setup only", None))
        self.pushButtonComputeAll.setText(_translate("DialogForwardModelSkip", "Compute all \n"
" phases again", None))

