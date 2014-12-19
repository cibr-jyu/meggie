'''
Created on 19.12.2014

@author: Kari Aliranta
'''


from PyQt4 import QtGui

from forwardSolutionDialogUi import Ui_DialogCreateFSolution
import messageBoxes

import multiprocessing


class ForwardSolutionDialog(QtGui.QDialog):
    
    
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogCreateFSolution()
        self.ui.setupUi(self) 
        
        cores = multiprocessing.cpu_count()
        self.ui.spinBoxNJobs.setMaximum = cores
        self.ui.spinBoxNJobs.setValue(cores - 1)
        
        
    def accept(self):
        """
        Gets the arguments from the gui and passes them to the caller for 
        forward solution creation.
        """
        
        paramdict = {}
        
        paramdict['includeMEG'] = self.ui.checkBoxIncludeMEG.isChecked()
        paramdict['includeEEG'] = self.ui.checkBoxIncludeEEG.isChecked()
        paramdict['mindist'] = self.ui.doubleSpinBoxMinDist.value()
        
        if self.ui.buttonGroupIgnoreRef.checkedButton() == \
        self.ui.radioButtonIgnoreYes:    
            paramdict['ignoreref'] = True
        else:
            paramdict['ignoreref'] = False
            
        paramdict['njobs'] = self.ui.spinBoxNJobs.value()
    
        