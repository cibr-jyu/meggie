# coding: latin1
'''
Created on Aug 20, 2013

@author: kpaliran
'''
import os

import mne
from PyQt4 import QtCore,QtGui
from filterDialogUi import Ui_DialogFilter
from mplWidget import MplWidget, MplCanvas

from code_meggie.general.caller import Caller
from measurementInfo import MeasurementInfo
from matplotlib import pyplot as plt

import messageBoxes
from copy import deepcopy

class FilterDialog(QtGui.QDialog):
    """
    Class containing the logic for filterDialog. It collects the parameters
    needed for filtering and shows the preview for the filter if required.
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogFilter()
        self.ui.setupUi(self)
        self.filterParameterDictionary = None
        self.dataToFilter = None
        self.caller = Caller.Instance()
        
    def on_pushButtonPreview_clicked(self, checked=None):
        """
        Draws the preview.
        """
        if checked is None: return
        
        paramDict = self.get_filter_parameters()
        if paramDict.get('isEmpty') == True:
                message = 'Please select filter(s) to preview'
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                return    
        
        self.drawPreview()      
    
        
    def drawPreview(self):
        """
        Shows the data (mne.raw.plot()) filtered with the given filters, but
        does not actually modify it. Also asks whether the previewed file
        should be saved over the working file, and saves if the user answers
        yes.
        """
        
        paramDict = self.get_filter_parameters()
        self.dataToFilter = self.caller.experiment.active_subject.\
                            _working_file._data
        info = self.caller.experiment.active_subject.\
                            _working_file.info
                            
        samplerate = self.caller.experiment.active_subject._working_file.info['sfreq']
        
        # Check if the filter frequency values are sane or not.
        if (self._validateFilterFreq(paramDict, samplerate) == False) or \
        (self._validateFilterLength(paramDict) == False):
            return
        
        try: 
            filteredData = self.caller.filter(self.dataToFilter, info, samplerate,
                                              paramDict)
        except ValueError as e:
            message = 'There was problem with filtering. MNE-Python error ' + \
            'message was: \n\n' + str(e)
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            return
        
        raw = self.caller.experiment.active_subject._working_file
        previewRaw = deepcopy(raw)
        previewRaw._data = filteredData
        
        # This should really block, but doesn't.
        previewRaw.plot(block=True)                       
        
        reply = QtGui.QMessageBox.question(self, 'Apply filters?', 
                    'Apply the previewed filters to the working file?', 
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                    QtGui.QMessageBox.Yes)  
           
        if reply == QtGui.QMessageBox.Yes:
            fname = previewRaw.info.get('filename')
            # This actually saves the file over current working file,
            # because the previewRaw filename is the same as that of raw
            # file it is copied from. 
            
            # Update the data file with new filter values.
            if 'lowpass' in paramDict and paramDict['lowpass'] == True:
                previewRaw.info['lowpass'] = paramDict['low_cutoff_freq']
        
            if ( 'highpass' in paramDict and paramDict['highpass'] == True ):
                previewRaw.info['highpass'] = paramDict['high_cutoff_freq']
    
            previewRaw.save(fname, overwrite=True)
            raw = mne.io.Raw(fname, preload=True)
            self.caller.update_experiment_working_file(fname, raw)
            
            
            
            self.parent._initialize_ui()
        else: return
        
        
    def get_filter_parameters(self):
        """
        Gets the filtering parameters from the UI fields and performs
        rudimentary sanity checks on them.
        """
        
        dictionary = {}
        dictionary['isEmpty'] = True
        
        if self.ui.checkBoxLowpass.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['lowpass'] = True
            
            dictionary['low_cutoff_freq'] = self.ui.\
                                       doubleSpinBoxLowpassCutoff.value()
            dictionary['low_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxLowpassTransBandwidth.value()
            dictionary['low_length'] = str(self.ui.lineEditLowpassLength.\
                                           text())
        else:
            dictionary['lowpass'] = False
        
        if self.ui.checkBoxHighpass.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['highpass'] = True
            
            dictionary['high_cutoff_freq'] = self.ui.\
                                        doubleSpinBoxHighpassCutoff.value()
            dictionary['high_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxHighpassTransBandwidth.value()
            dictionary['high_length'] = str(self.ui.lineEditHighpassLength.\
                                            text())
        else:
            dictionary['highpass'] = False
        
        if self.ui.checkBoxBandstop.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['bandstop1'] = True
            
            dictionary['bandstop1_l_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq.value() - \
                self.ui.doubleSpinBoxBandstopWidth.value()/2
                
            dictionary['bandstop1_h_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq.value() + \
                self.ui.doubleSpinBoxBandstopWidth.value()/2
                        
            dictionary['bandstop1_trans_bandwidth'] = self.ui.\
            doubleSpinBoxBandstopWidth.value()
            
            dictionary['bandstop1_length'] = str(self.ui.\
                                             lineEditBandstopLength.text())
        else:
            dictionary['bandstop1'] = False
        
        if self.ui.checkBoxBandstop2.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['bandstop2'] = True
            
            dictionary['bandstop2_l_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq2.value() - \
                self.ui.doubleSpinBoxBandstopWidth2.value()/2
            
            dictionary['bandstop2_h_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq2.value() + \
                self.ui.doubleSpinBoxBandstopWidth2.value()/2
            
            dictionary['bandstop2_trans_bandwidth'] = self.ui.\
                doubleSpinBoxBandstopWidth2.value()
                                    
            dictionary['bandstop2_length'] = str(self.ui.\
                                             lineEditBandstopLength2.text())
        else:
            dictionary['bandstop2'] = False
            
        if dictionary.get('isEmpty') == True:
                message = 'Please select filter(s) to apply'
                self.messageBox = messageBoxes.shortMessageBox(message)
                self.messageBox.show()
                return    
            
        return dictionary    
    
    
    def accept(self):
        """
        Get the parameters dictionary and relay it to caller.filter to
        actually do the filtering.
        """
        QtGui.QApplication.setOverrideCursor(QtGui.\
                                             QCursor(QtCore.Qt.WaitCursor))
        paramDict = self.get_filter_parameters()   
        self.dataToFilter = self.caller.experiment.active_subject.\
                            _working_file._data
        samplerate = self.caller.experiment.active_subject.\
        _working_file.info['sfreq']
        info = self.caller.experiment.active_subject.\
                            _working_file.info
        
        # Check if the filter frequency values are sane or not.
        if (self._validateFilterFreq(paramDict, samplerate) == False) or \
                        (self._validateFilterLength(paramDict) == False):
            QtGui.QApplication.restoreOverrideCursor()
            return
        
        try: 
            filteredData = self.caller.filter(self.dataToFilter, info,
                                              samplerate, paramDict)
        except ValueError as e:
            message = 'There was problem with filtering. MNE-Python error ' + \
            'message was: \n\n' + str(e)
            self.messageBox = messageBoxes.shortMessageBox(message)
            self.messageBox.show()
            QtGui.QApplication.restoreOverrideCursor()
            return
        
        raw = self.caller.experiment.active_subject._working_file
        raw._data = filteredData
        fname = raw.info.get('filename')
        
        # Update the data file with new filter values.
        if 'lowpass' in paramDict and paramDict['lowpass'] == True:
            raw.info['lowpass'] = paramDict['low_cutoff_freq']
    
        if ( 'highpass' in paramDict and paramDict['highpass'] == True ):
            raw.info['highpass'] = paramDict['high_cutoff_freq']
        
        raw.save(fname, overwrite=True)
        raw = mne.io.Raw(fname, preload=True)
        self.caller.update_experiment_working_file(fname, raw)

        self.parent._initialize_ui()
        QtGui.QApplication.restoreOverrideCursor()
        self.close()
    
    
    def _validateFilterFreq(self, paramDict, samplerate):
        """
        Checks the validity of filter cutoff frequency values.
        """
        if 'lowpass' in paramDict and paramDict['lowpass'] == True:
            if ( paramDict['low_cutoff_freq'] > samplerate/2 ):
                self._show_filter_freq_error(samplerate)
    
        if ( 'highpass' in paramDict and paramDict['highpass'] == True ):
            if ( paramDict['high_cutoff_freq'] > samplerate/2 ):
                self._show_filter_freq_error(samplerate)
    
    
    def _show_filter_freq_error(self, samplerate):
        message = 'Cutoff frequencies should be lower than samplerate/2 ' + \
                    '(' + 'current samplerate is ' + str(samplerate) + ' Hz)'
        self.messageBox = messageBoxes.shortMessageBox(message)
        self.messageBox.show()
        return
    
    
    def _validateFilterLength(self, paramDict):
        if 'lowpass' in paramDict and paramDict['lowpass'] == True:
            lowLengthString = paramDict['low_length']
            if ( not lowLengthString.endswith('ms') and 
                 not lowLengthString.endswith('s') ):
                self._showLengthError('low pass')
                return False
    
        if 'highpass' in paramDict and paramDict['highpass'] == True:
            highLengthString = paramDict['high_length']
            if ( not highLengthString.endswith('ms') and 
                 not highLengthString.endswith('s') ):
                self._showLengthError('high pass')
                return False
    
    
    def _showLengthError(self, filterSource):
        """
        Show the error for wrong type of filter length string.
        
        Keyword arguments:
        
        filterSource     -- which filter UI box is the source of error.
        """
        message = 'Check filter length for ' + filterSource + \
        '. It should end with \'s\' or \'ms\''
        self.messageBox = messageBoxes.shortMessageBox(message)
        self.messageBox.show()
        