'''
Created on 10.11.2014

@author: Kari Aliranta
'''

from PyQt4 import QtCore, QtGui

from meggie.ui.sourceModeling.holdCoregistrationDialogUi import Ui_DialogHoldCoregistration

from meggie.code_meggie.general import fileManager

import os


class holdCoregistrationDialog(QtGui.QDialog):
    
    
    def __init__(self, parent, activeSubject, selectedFmodelName):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogHoldCoregistration()
        self.ui.setupUi(self)
        
        self.subject = activeSubject
        self.fModelName = selectedFmodelName
        self.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint |
                            QtCore.Qt.WindowCloseButtonHint |
                            QtCore.Qt.WindowStaysOnTopHint)
        self.center()
    
    
    def center(self):
        """
        Center the window on screen.
        """
        screen = QtGui.QDesktopWidget().screenGeometry()
        mysize = self.geometry()
        hpos = ( screen.width() - mysize.width() ) / 2
        vpos = ( screen.height() - mysize.height() ) / 2
        self.move(hpos, vpos)

    
    def on_pushButtonCancel_clicked(self, checked=None):
        if checked is None: return
        self.close()
    
        
    def on_pushButtonCopy_clicked(self, checked=None):
        if checked is None: return
        
        transFilePath = os.path.join(self.subject._subject_path, 
                                     'reconFiles-trans.fif')
        
        if not os.path.isfile(transFilePath):
            self.ui.labelTransFileWarning.setHidden(False)
            return
        
        try:
            fileManager.move_trans_file(self.subject, self.fModelName)
            
            """
            Remove the current fModel from the MVC model and add it back, so
            that the presence of trans file gets noted.
            """
            fModelModel = self.parent.parent.forwardModelModel
            fModelList = fModelModel.fmodelInfoList
            for fm in fModelList:
                if fm[0] == self.fModelName:
                    fModelList.remove(fm)
                    break
            
            fModelModel.layoutAboutToBeChanged.emit()
            fModelModel.layoutChanged.emit()
        
            fmdir = self.subject._forwardModels_directory
            pmlist = fModelModel.create_single_FM_param_list(fmdir,
                                                             self.fModelName)
            fModelModel.fmodelInfoList.append(pmlist)
            
            fModelModel.layoutAboutToBeChanged.emit()
            fModelModel.layoutChanged.emit()
            
            self.close()
        except IOError: 
            message = 'There was an unknown problem copying the trans file. '
            self.ui.labelTransFileWarning.setText(message)
            self.ui.labelTransFileWarning.setHidden(False)
