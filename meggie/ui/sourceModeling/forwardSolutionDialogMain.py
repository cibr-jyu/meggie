'''
Created on 19.12.2014

@author: Kari Aliranta
'''


from PyQt4 import QtGui

from code_meggie.general.caller import Caller

from ui.sourceModeling.forwardSolutionDialogUi import Ui_DialogCreateFSolution
from ui.general import messageBoxes

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
        
        tableView = self.parent.ui.tableViewFModelsForSolution
        selectedRowIndexes = tableView.selectedIndexes()
        
        compartModelIndex = self.parent.forwardModelModel.index(
                                            selectedRowIndexes[0].row(), 8)
        compartModel = self.parent.forwardModelModel.data(compartModelIndex)
        
        if compartModel == 'single (usually used with MEG)':
            self.ui.checkBoxIncludeEEG.setChecked(False)
            self.ui.checkBoxIncludeEEG.setEnabled(False)
            self.ui.labelIncludEEG.setEnabled(False)
            self.ui.labelIncludEEG.setToolTip('disabled due to single ' + \
                                           'compartment model in forward model')
        
        
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
        caller = Caller.Instance()
        caller.create_forward_solution(paramdict)   
        self.close()
