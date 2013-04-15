'''
Created on Mar 28, 2013

@author: jaeilepp
'''
from maxFilterDialog import Ui_Dialog
from settings import Settings
import messageBox
from caller import Caller

import os
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
        
    def on_pushButtonBrowsePositionFile_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                       '/home/')
        
    
    def accept(self):
        """
        """
        try:
            dictionary = {'-v': ''}
            x = self.ui.doubleSpinBoxX0.value()
            y = self.ui.doubleSpinBoxY0.value()
            z = self.ui.doubleSpinBoxZ0.value()
            fit = self.ui.checkBoxFit.checkState() == QtCore.Qt.Checked
            order_in = self.ui.spinBoxOrderIn.value()
            order_out = self.ui.spinBoxOrderOut.value()
            autobad = self.ui.checkBoxAutobad.checkState() == \
            QtCore.Qt.Checked
            bad_limit = self.ui.doubleSpinBoxBadLimit.value()
            bads = self.ui.lineEditBad.text()
            skips = ''
            if self.ui.checkBoxSkip_1.checkState() == QtCore.Qt.Checked:
                #skips += ' -skip '
                skips += self.ui.lineEditSkipStart_1.text() + ' '
                skips += self.ui.lineEditSkipEnd_1.text() + ' '
                if self.ui.checkBoxSkip_2.checkState() == QtCore.Qt.Checked:
                    skips += self.ui.lineEditSkipStart_2.text() + ' '
                    skips += self.ui.lineEditSkipEnd_2.text() + ' '
                    if self.ui.checkBoxSkip_2.checkState() == \
                    QtCore.Qt.Checked:
                        skips += self.ui.lineEditSkipStart_3.text() + ' '
                        skips += self.ui.lineEditSkipEnd_3.text() + ' '            
            button_text = str(self.ui.buttonGroup.checkedButton().text())
            format = button_text.split(' ')[0].lower()
            if self.ui.checkBoxMaxMove.checkState() == QtCore.Qt.Checked:
                button_position = \
                str(self.ui.buttonGroupMaxMove.checkedButton().text())
                if button_position == \
                'Transform data into default head position':
                    dictionary['-trans'] = 'default'
                elif button_position == \
                'Transform data to head position in a file:':
                    if self.fname != '':
                        try:
                            if os.path.isfile(str(fname)) and \
                            str(fname).endswith('fif'):
                                dictionary['-trans'] = self.fname
                            else:
                                raise Exception('Could not open file.')
                        except Exception, err:
                            self.messageBox = messageBox.AppForm()
                            self.messageBox.labelException.setText(str(err))
                            self.messageBox.show()
                elif button_position == \
                'Transform data into averaged head position':
                    pass
            if self.ui.checkBoxStorePosition.checkState()==QtCore.Qt.Checked:
                dictionary['-hp'] = ''
            dictionary['-f'] = self.raw.info.get('filename')
            print self.raw.info.get('filename')
            """raw.fif -> raw_sss.fif"""
            if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
                dictionary['-o'] = self.raw.info.get('filename')[:-4] + '_tsss.fif'
            else:
                dictionary['-o'] = self.raw.info.get('filename')[:-4] + '_sss.fif'
            if fit: dictionary['-origin fit'] = ''
            else: dictionary['-origin'] = str(x) + ' ' + str(y) + ' ' + str(z)
            dictionary['-linefreq'] = self.ui.spinBoxLineFreq.value()
            dictionary['-in'] = order_in
            dictionary['-out'] = order_out
            if autobad: dictionary['-autobad'] = 'on' 
            else:
                dictionary['-autobad'] = 'off'
                dictionary['-bad'] = bads
            dictionary['-badlimit'] = bad_limit
            if skips != '':
                dictionary['-skip'] = skips
            dictionary['-format'] = format
            
            if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
                dictionary['-st'] = self.ui.spinBoxBufferLength.value()
                dictionary['-corr'] = self.ui.doubleSpinBoxCorr.value()
            custom = self.ui.textEditCustom.toPlainText()
            caller = Caller()
            t = Thread(target=caller.call_maxfilter,
                       args=(dictionary, custom,))
            t.start()
            self.parent.ui.checkBoxMaxFilter.setCheckState(2)
            self.close()
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
            