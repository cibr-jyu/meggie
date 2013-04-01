'''
Created on Mar 28, 2013

@author: jaeilepp
'''
from maxFilterDialog import Ui_Dialog
from settings import Settings
import messageBox

#import preprosessing
import subprocess
from threading import Thread
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
        
    def call_maxfilter(self, bs):
        proc = subprocess.Popen(bs, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        for line in proc.stdout.readlines():
            print line
        retval = proc.wait()
        print "the program return code was %d" % retval
    
    def accept(self):
        """
        """
        settings = Settings()
        try:
            x = self.ui.lineEditX0.text()
            y = self.ui.lineEditY0.text()
            z = self.ui.lineEditZ0.text()
            settings.validate_int(x, 0, 1000)
            settings.validate_int(y, 0, 1000)
            settings.validate_int(z, 0, 1000)
            fit = self.ui.checkBoxFit.checkState() == QtCore.Qt.Checked
            order_in = self.ui.lineEditOrderIn.text()
            order_out = self.ui.lineEditOrderOut.text()
            autobad = self.ui.checkBoxAutobad.checkState() == QtCore.Qt.Checked
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
            button_text = str(self.ui.buttonGroup.checkedButton().text())
            format = button_text.split(' ')[0].lower()
            tSSS = ''
            if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
                tSSS += ' -st ' + self.ui.lineEditDataBufferLength.text()
                tSSS += ' -corr ' + self.ui.lineEditSubspaceCorrelationLimit.text()
            max_move = ''
            if self.ui.checkBoxMaxMove.checkState() == QtCore.Qt.Checked:
                max_move += ' -movecomp ' + '-hpiwin ' + self.ui.lineEditHPI.text()
                max_move += ' -hpistep ' + self.ui.lineEditHPIStep.text()
            bs = 'maxfilter -v -f ' + self.raw.info.get('filename')
            bs += ' -o '
            
            """raw.fif -> raw_sss.fif"""
            bs += self.raw.info.get('filename')[:-4] + '_sss.fif'
            bs += ' -origin ' + x + ' ' + y + ' ' + z
            if fit: bs += ' -origin fit'
            bs += ' -in' + order_in
            bs += ' -out' + order_out
            if autobad: bs += ' -autobad on '
            else:
                bs += ' -autobad off'
                bs += ' -bad ' + bads
            bs += ' -badlimit ' + bad_limit
            bs += skips
            bs += ' -format ' + format
            bs += ' -force -def -maint '
            bs += tSSS
            bs += max_move
            t = Thread(target=self.call_maxfilter, args=(bs,))
            t.start()
            self.close()
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
        