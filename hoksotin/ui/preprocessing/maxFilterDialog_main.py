# coding: latin1
'''
Created on Mar 28, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Atte Rautio
'''
from maxFilterDialog_Ui import Ui_Dialog

import glob
import sys
import os
import subprocess
from threading import Thread
from PyQt4 import QtCore,QtGui

import messageBox

class MaxFilterDialog(QtGui.QDialog):


    def __init__(self, parent, raw):
        """
        A dialog for collecting parameter values for MaxFilter.
        
        Keyword arguments:
        
        parent     --    The class that created this window.
        raw        --    The raw data file to be MaxFiltered.
        """
        QtGui.QDialog.__init__(self)
        """
        Reference to main dialog window
        """       
        self.raw = raw
        self.parent = parent
        self.ui = Ui_Dialog() # Refers to class in file MaxFilterDialog
        self.ui.setupUi(self)
        # Hides the label indicating that MaxFilter has been used.
        self.ui.labelComputeMaxFilter.setVisible(False)
        self.ui.progressBarComputeMaxFilter.setVisible(False)
        # Checks which lab-specific calibration files are found and adds those
        # labs to comboBoxLab.
        self.populateComboboxLab()
        
    def on_pushButtonBrowsePositionFile_clicked(self, checked=None):
        if checked is None: return # Standard workaround for file dialog opening twice
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                       '/home/')     
    
    def accept(self):
        """
        Reads values from the dialog, saves them in a dictionary and initiates
        a caller to actually call the backend.
        """
        t = Thread(target=self._show_progressbar)
        t.start()
        
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
        
        try:
            bads = self.ui.lineEditBad.text()
        except InputError, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()           
        """ 
        Check for skips and the sanity of their values. Skip periods should
        not overlap, and later skip periods should come later than earlier
        regions
        """
        
        skips = ''
        if self.ui.checkBoxSkip_1.checkState() == QtCore.Qt.Checked:
            if ( self.ui.spinBoxSkipEnd_1.value() 
            <= self.ui.spinBoxSkipStart_1.value() ):
                self.showErrorMessage('First skip ends before it starts.')
                return 
            skips += str(self.ui.spinBoxSkipStart_1.value()) + ' '
            skips += str(self.ui.spinBoxSkipEnd_1.value()) + ' '
            
        if self.ui.checkBoxSkip_2.checkState() == QtCore.Qt.Checked:
            if ( self.ui.spinBoxSkipEnd_2.value() 
                 <= self.ui.spinBoxSkipStart_2.value() ):
                    self.showErrorMessage('Second skip ends ' +
                                           'before it starts.')
            if (self.ui.spinBoxSkipStart_2.value() 
                 < self.ui.spinBoxSkipEnd_1.value() ):
                    self.showErrorMessage('Second skip starts before the ' +
                                          'first skip ends.')
                    return
            skips += str(self.ui.spinBoxSkipStart_2.value()) + ' '
            skips += str(self.ui.spinBoxSkipEnd_2.value()) + ' '
        
        if self.ui.checkBoxSkip_3.checkState() == QtCore.Qt.Checked:
            if ( self.ui.spinBoxSkipEnd_3.value() 
                 <= self.ui.spinBoxSkipStart_3.value()):
                    self.showErrorMessage('Third skip ends before it starts.')
            if ( self.ui.spinBoxSkipStart_3.value() 
                 < self.ui.spinBoxSkipEnd_2.value() ):
                    self.showErrorMessage('Third skip starts before the ' + 
                                          'second skip ends.')
                    return
            skips += str(self.ui.spinBoxSkipStart_3.value()) + ' '
            skips += str(self.ui.spinBoxSkipEnd_3.value()) + ' '            
        
        """ 
        This code was used for a buttongroup that allowed selection of output
        format of MaxFilter generated files. The format now defaults to 32-bit
        float. MaxFilter allows other formats, but no need to show them
        in the UI.
        """
        # button_text = str(self.ui.buttonGroupFormat.checkedButton().text())
        # format = button_text.split(' ')[0].lower()
            
        if self.ui.checkBoxMaxMove.checkState() == QtCore.Qt.Checked:
            button_position = \
            str(self.ui.buttonGroupMaxMove.checkedButton().objectName())
            if button_position == \
            'radioButtonPositionDefault':
                dictionary['-trans'] = 'default'
            elif button_position == \
            'radioButtonPositionFile':
                if self.fname != '':
                    try:
                        if os.path.isfile(str(self.fname)) and \
                        str(self.fname).endswith('fif'):
                            dictionary['-trans'] = self.fname
                        else:
                            raise Exception('Could not open file.')
                    except Exception, err:
                        self.showErrorMessage(err)
            elif button_position == \
            'radioButtonPositionAverage':
                pass
        
        # TODO Stores the head position in a file 
        if self.ui.checkBoxStorePosition.checkState()==QtCore.Qt.Checked:
            dictionary['-hp'] = ''
        
        dictionary['-f'] = self.raw.info.get('filename')
        print self.raw.info.get('filename')
        
        #raw.fif -> raw_sss.fif
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
        
        dictionary['-format'] = float
        
        if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
            dictionary['-st'] = self.ui.spinBoxBufferLength.value()
            dictionary['-corr'] = self.ui.doubleSpinBoxCorr.value()
        
        # TODO: check what the extensions of the calibration files are.    
        lab = self.setLab()
        
        if not lab == '':
            dictionary['-site'] = lab
            
        custom = self.ui.textEditCustom.toPlainText()
        
        # Uses the caller related to mainwindow
        caller = self.parent.caller
        
        try:
            caller.call_maxfilter(dictionary, custom)
        except Exception, err:
            self.messageBox = messageBox.AppForm()
            self.messageBox.labelException.setText(str(err))
            self.messageBox.show()
        
        """
        Checks the MaxFilter box in the preprocessing tab of the mainWindow
        """ 
        self.parent.ui.checkBoxMaxFilter.setCheckState(2)
        
        self.close()
        
    def populateComboboxLab(self):
        # TODO: fix the paths
        """
        Goes through the lab-specific config files in
        $NEUROMAG_ROOT/databases/sss/ and returns a list of labs found.
        """
        # TODO: change c:\\MyTemp\\testi\\ into the proper env variable.
        if os.environ.get('NEUROMAG_ROOT') is None:
            os.environ['NEUROMAG_ROOT'] = '/neuro'
        self.root = os.environ.get('NEUROMAG_ROOT')
        files = os.listdir(self.root + '/databases/sss/')
        
        for file in files:
            
            if file.startswith('sss_cal_'):
                lab = file.split('sss_cal_')[1][:-4]
                if os.path.isfile(self.root + '/databases/ctc/' + 
                                  'ct_sparse_' + lab + '.fif'): 
                    self.ui.comboBoxLab.addItem(lab)
                
    
    def setLab(self):
        # TODO: Fix the paths.
        """
        Checks if calibration files for the selected lab exist.
        Returns the selected lab or an empty string if files are not found.
        """
        
        lab = str(self.ui.comboBoxLab.currentText())
        
        if not os.path.isfile(self.root + '/databases/sss/sss_cal_' +
                              lab + '.dat'):
            lab = ''
            return lab
        
        if not os.path.isfile(self.root + '/databases/ctc/ct_sparse_' + 
                              lab + '.fif'):
            lab = ''
            return lab
        
        return lab
            
    def _show_progressbar(self):
        """
        Shows and starts the progressbar.
        """
        self.ui.labelComputeMaxFilter.setVisible(True)
        self.ui.progressBarComputeMaxFilter.setVisible(True)
            
    def showErrorMessage(self, message):
        """
        Generic error message to be shown to the user
        """
        self.messageBox = messageBox.AppForm()
        self.messageBox.labelException.setText(str(message))
        self.messageBox.show()
        