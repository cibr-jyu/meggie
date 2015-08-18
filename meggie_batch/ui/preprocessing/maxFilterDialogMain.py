# coding: latin1

#Copyright (c) <2013>, <Kari Aliranta, Jaakko Lepp�kangas, Janne Pesonen and Atte Rautio>
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met: 
#
#1. Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer. 
#2. Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution. 
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
#ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#The views and conclusions contained in the software and documentation are those
#of the authors and should not be interpreted as representing official policies, 
#either expressed or implied, of the FreeBSD Project.

"""
Created on Mar 28, 2013

@author: Kari Aliranta, Jaakko Leppakangas, Atte Rautio
Contains the MaxFilterDialog-class used for calling MaxFilter.
"""

import os
from threading import Thread

from PyQt4 import QtCore,QtGui

from maxFilterDialogUi import Ui_Dialog
from code_meggie.general.caller import Caller
import messageBoxes

class MaxFilterDialog(QtGui.QDialog):
    """
    Collects the parameter values used for calling MaxFilter.
    """


    def __init__(self, parent):
        """
        Initializes the dialog for collecting parameter values for MaxFilter.

        Keyword arguments:
        parent     --    The class that created this window.
        """
        QtGui.QDialog.__init__(self)

        # Reference to main dialog window
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
        # Standard workaround for file dialog opening twice
        if checked is None: return 
        self.fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                                                       '/home/')     

    def accept(self):
        """
        Reads values from the dialog, saves them in a dictionary and initiates
        a caller to actually call the backend.
        """
        self._show_progressbar(True)

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

        # Check for skips and the sanity of their values. Skip periods should
        # not overlap, and later skip periods should come later than earlier
        # regions
        skips = ''
        if self.ui.checkBoxSkip_1.checkState() == QtCore.Qt.Checked:
            if ( self.ui.spinBoxSkipEnd_1.value()
            <= self.ui.spinBoxSkipStart_1.value() ):
                self.showErrorMessage('First skip ends before it starts.')
                self._show_progressbar(False)
                return
            skips += str(self.ui.spinBoxSkipStart_1.value()) + ' '
            skips += str(self.ui.spinBoxSkipEnd_1.value()) + ' '

        if self.ui.checkBoxSkip_2.checkState() == QtCore.Qt.Checked:
            if ( self.ui.spinBoxSkipEnd_2.value()
                 <= self.ui.spinBoxSkipStart_2.value() ):
                    self.showErrorMessage('Second skip ends ' +
                                           'before it starts.')
                    self._show_progressbar(False)
                    return
            if (self.ui.spinBoxSkipStart_2.value() 
                 < self.ui.spinBoxSkipEnd_1.value() ):
                    self.showErrorMessage('Second skip starts before the ' +
                                          'first skip ends.')
                    self._show_progressbar(False)
                    return
            skips += str(self.ui.spinBoxSkipStart_2.value()) + ' '
            skips += str(self.ui.spinBoxSkipEnd_2.value()) + ' '
        
        if self.ui.checkBoxSkip_3.checkState() == QtCore.Qt.Checked:
            if ( self.ui.spinBoxSkipEnd_3.value() 
                 <= self.ui.spinBoxSkipStart_3.value()):
                    self.showErrorMessage('Third skip ends before it starts.')
                    self._show_progressbar(False)
                    return
            if ( self.ui.spinBoxSkipStart_3.value() 
                 < self.ui.spinBoxSkipEnd_2.value() ):
                    self.showErrorMessage('Third skip starts before the ' + 
                                          'second skip ends.')
                    self._show_progressbar(False)
                    return
            skips += str(self.ui.spinBoxSkipStart_3.value()) + ' '
            skips += str(self.ui.spinBoxSkipEnd_3.value()) + ' '

        if self.ui.checkBoxMaxMove.checkState() == QtCore.Qt.Checked:
            button_position = \
            str(self.ui.buttonGroupMaxMove.checkedButton().objectName())
            if button_position == 'radioButtonPositionDefault':
                dictionary['-trans'] = 'default'
            elif button_position == 'radioButtonPositionFile':
                if self.fname != '':
                    try:
                        if os.path.isfile(str(self.fname)) and \
                                str(self.fname).endswith('fif'):
                            dictionary['-trans'] = self.fname
                        else:
                            self._show_progressbar(False)
                            self.showErrorMessage('Could not open file.')
                            return
                    except Exception, err:
                        self._show_progressbar(False)
                        self.showErrorMessage(err)
                        return
            elif button_position == 'radioButtonPositionAverage':
                self._show_progressbar(False)
                raise NotImplementedError('Average head positioning is not '
                                          'implemented.')

        # TODO Store the head position in a file
        if self.ui.checkBoxStorePosition.checkState()==QtCore.Qt.Checked:
            dictionary['-hp'] = ''

        caller = Caller.Instance()
        raw = caller.experiment.active_subject.working_file
        dictionary['-f'] = raw.info.get('filename')
        print raw.info.get('filename')
        
        #raw.fif -> raw_sss.fif
        if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
            dictionary['-o'] = raw.info.get('filename')[:-4] + '_tsss.fif'
        else:
            dictionary['-o'] = raw.info.get('filename')[:-4] + '_sss.fif'
        
        if fit:
            dictionary['-origin fit'] = ''
        else:
            dictionary['-origin'] = str(x) + ' ' + str(y) + ' ' + str(z)
            if self.ui.radioButtonDevice.isChecked():
                dictionary['-frame'] = 'device'
            elif self.ui.radioButtonHead.isChecked():
                dictionary['-frame'] = 'head'
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

        dictionary['-format'] = 'float'

        if self.ui.checkBoxtSSS.checkState() == QtCore.Qt.Checked:
            dictionary['-st'] = self.ui.spinBoxBufferLength.value()
            dictionary['-corr'] = self.ui.doubleSpinBoxCorr.value()

        # TODO: check what the extensions of the calibration files are.    
        lab = self.setLab()

        if not lab == '':
            dictionary['-site'] = lab

        custom = self.ui.textEditCustom.toPlainText()

        try:
            caller.call_maxfilter(dictionary, custom)
        except Exception, err:
            title = 'MaxFilter error:'
            self.messageBox = messageBoxes.longMessageBox(title, str(err))
            self.messageBox.show()
            self._show_progressbar(False)
            return

        # Checks the MaxFilter box in the preprocessing tab of the mainWindow.
        self.parent.ui.checkBoxMaxFilterComputed.setCheckState(2)
        self.close()

    def populateComboboxLab(self):
        """
        Goes through the lab-specific config files in
        $NEUROMAG_ROOT/databases/sss/ and returns a list of labs found.
        TODO: proper message to the user if NEUROMAG_ROOT isn't set.
        """
        if os.environ.get('NEUROMAG_ROOT') is None:
            os.environ['NEUROMAG_ROOT'] = '/neuro'
        self.root = os.environ.get('NEUROMAG_ROOT')
        files = os.listdir(self.root + '/databases/sss/')

        for fname in files:
            if fname.startswith('sss_cal_'):
                lab = fname.split('sss_cal_')[1][:-4]
                if os.path.isfile(self.root + '/databases/ctc/' + 
                                  'ct_sparse_' + lab + '.fif'): 
                    self.ui.comboBoxLab.addItem(lab)

    def setLab(self):
        """
        Checks if the calibration files for the selected lab exist.
        Returns the selected lab or an empty string if no files are found.
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

    def _show_progressbar(self, visible):
        """
        Shows and starts the progressbar.

        Keyword arguments:
        visible  -- Whether to show or hide progress bar.
        """
        if visible:
            QtGui.QApplication.setOverrideCursor(QtGui.\
                                                 QCursor(QtCore.Qt.WaitCursor))
        else:
            QtGui.QApplication.restoreOverrideCursor()
        self.ui.labelComputeMaxFilter.setVisible(visible)
        self.ui.progressBarComputeMaxFilter.setVisible(visible)
