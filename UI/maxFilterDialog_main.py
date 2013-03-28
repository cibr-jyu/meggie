'''
Created on Mar 28, 2013

@author: jaeilepp
'''
from maxFilterDialog import Ui_Dialog

#import preprosessing

from PyQt4 import QtCore,QtGui

class MaxFilterDialog(QtGui.QDialog):


    def __init__(self, parent, raw):
        '''
        Constructor
        '''
        QtGui.QDialog.__init__(self)
        """
        Reference to main dialog window
        """       
        self.raw = raw
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in file MaxFilterDialog
        self.ui.setupUi(self)
        
    def accept(self):
        """
        """
        x = self.ui.lineEditX0.text()
        y = self.ui.lineEditY0.text()
        z = self.ui.lineEditZ0.text()
        fit = self.ui.checkBoxFit.checkState() == QtCore.Qt.Checked
        order_in = self.ui.lineEditOrderIn.text()
        order_out = self.ui.lineEditOrderOut.text()
        bad_limit = self.ui.lineEditBadLimit.text()
        bads = self.ui.lineEditBad.text()
        #format = self.ui.rad
        #preprosessing.MaxFilter(raw, )
        button = self.ui.buttonGroup.checkedButton()
        format = button.text().split(' ')            