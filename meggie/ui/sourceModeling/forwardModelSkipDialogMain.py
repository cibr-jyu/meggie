'''
Created on 30.1.2015

@author: Kari Aliranta
'''

from PyQt4 import QtGui

from ui.sourceModeling.forwardModelSkipDialogUi import Ui_DialogForwardModelSkip


class ForwardModelSkipDialog(QtGui.QDialog):
    
    def __init__(self, parent, sSpaceDict, wshedDict):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogForwardModelSkip()
        self.ui.setupUi(self)
        
        # The value the dialog should "return" when one of the buttons is
        # pressed (defaults to cancel for  
        self.returnValue = 'cancel'
        
        dmethod = sSpaceDict['surfaceDecimMethod']
        sName = sSpaceDict['surfaceName']
        cortStats = sSpaceDict['computeCorticalStats']
        atlas = wshedDict['useAtlas']
        
        self.ui.labelDecimMethod.setText(dmethod)
        if not dmethod == 'traditional (default)':
            self.ui.labelIcoValue.setEnabled(True)
            self.ui.labelIcoValue_2.setEnabled(True)
            self.ui.labelIcoValue_2.setText(str(sSpaceDict['surfaceDecimValue']))
        else:
            self.ui.labelSpacing.setEnabled(True)
            self.ui.labelSpacing_2.setEnabled(True)
            self.ui.labelSpacing_2.setText(str(sSpaceDict['spacing']))
    
        self.ui.labelSurfaceName.setText(sName)
        self.ui.labelComputePatchStats.setText(str(cortStats))
        self.ui.labelAtlas.setText(str(atlas))
        
    
    def get_return_value(self):
        return self.returnValue
    
    
    def on_pushButtonCancel_clicked(self, checked=None):
        if checked is None: return
        self.close()
        
        
    def on_pushButtonBemOnly_clicked(self, checked=None):
        if checked is None: return
        self.returnValue = 'bemOnly'
        self.close()
        
        
    def on_pushButtonComputeAll_clicked(self, checked=None):
        if checked is None: return
        self.returnValue = 'computeAll'
        self.close()
