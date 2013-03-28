'''
Created on Mar 28, 2013

@author: jaeilepp
'''
from maxFilterDialog import Ui_Dialog
from settings import Settings

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
        settings = Settings()
        x = self.ui.lineEditX0.text()
        y = self.ui.lineEditY0.text()
        z = self.ui.lineEditZ0.text()
        settings.validate_int(x, 0, 1000)
        settings.validate_int(y, 0, 1000)
        settings.validate_int(z, 0, 1000)
        fit = self.ui.checkBoxFit.checkState() == QtCore.Qt.Checked
        order_in = self.ui.lineEditOrderIn.text()
        order_out = self.ui.lineEditOrderOut.text()
        bad_limit = self.ui.lineEditBadLimit.text()
        bads = self.ui.lineEditBad.text()
        skips = ''
        if self.ui.checkBoxSkip_1.checkState() == QtCore.Qt.Checked:
            skips += ' -skip '
            skips += self.ui.lineEditSkipStart_1.text() + ' '
            skips += self.ui.lineEditSkipEnd_1.text() + ' '
            if self.ui.checkBoxSkip_2.checkState() == QtCore.Qt.Checked:
                skips += self.ui.lineEditSkipStart_2.text() + ' '
                skips += self.ui.lineEditSkipEnd_2.text() + ' '
                if self.ui.checkBoxSkip_2.checkState() == QtCore.Qt.Checked:
                    skips += self.ui.lineEditSkipStart_3.text() + ' '
                    skips += self.ui.lineEditSkipEnd_3.text() + ' '
        button = self.ui.buttonGroup.checkedButton()
        format = button.text().split(' ').toLower()
        tSSS = ''
        if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
            tSSS += ' -st ' + self.ui.lineEditDataBufferLength.text()
            tSSS += ' -corr ' + self.ui.lineEditSubspaceCorrelationLimit.text()
        max_move = ''
        if self.ui.checkBoxMaxMove.checkState() == QtCore.Qt.Checked:
            max_move += ' -movecomp ' + '-hpiwin ' + self.ui.lineEditHPI.text()
            max_move += ' -hpistep ' + self.ui.lineEditHPIStep.text()
            
        bs += 'maxfilter -v -f ' + self.raw.info.get('filename')
        """raw.fif -> raw_sss.fif"""
        bs += ' -o '
        bs += self.raw.info.get('filename')[:-4] + '_sss.fif'
        bs += ' -origin ' + x + ' ' + y + ' ' + z + ' '
        if fit: bs += '-origin fit '
        