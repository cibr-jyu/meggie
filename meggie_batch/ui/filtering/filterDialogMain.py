# coding: latin1
'''
Created on Aug 20, 2013

@author: kpaliran
'''
import os

from PyQt4 import QtCore,QtGui
from filterDialogUi import Ui_DialogFilter
from mplWidget import MplWidget, MplCanvas

from caller import Caller
from measurementInfo import MeasurementInfo
from matplotlib import pyplot as plt

import messageBoxes

class FilterDialog(QtGui.QDialog):
    """
    Class containing the logic for filterDialog. It collects the parameters
    needed for filtering and shows the preview for the filter if required.
    """
    caller = Caller.Instance()


    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_DialogFilter()
        self.ui.setupUi(self)
        self.filterParameterDictionary = None
        self.dataToFilter = None
        self.previewFigure = None
        
    def on_pushButtonPreview_clicked(self, checked=None):
        """
        Draws the preview.
        """
        if checked is None: return
        self.drawPreview()      
        
    def drawPreview(self):
        """
        Draws the frequency and impulse response into the preview window.
        """
        
        # Clear the previous figure to keep the pyplot state environment clean
        # and save memory. 
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        
        """
        Pit�isi:
        (0. Previewin pit�isi laskea xfit-tyylinen k�ppyr�)
        - Kiskoa datataulukko raw-filest� (vaatii sampleraten lukemista)
        - Lukea parametrit UI:sta ja p��tt��, mit� kaikki metodeja kutsutaan
        - K�ytt�� filterimetodeita dataan (j�rjestyksell� ei v�li�)
        - Kopioida data takaisin ja muuttaa ao. infokentti�
        
        """
        
        # Plot the filtered channels with mne.io.RawFIFF.plot (which is based
        # on pylab, therefore needing manual cleaning of pyplot state
        # environment.
        
        self.filterParameterDictionary = self.get_filter_parameters()
        self.previewFile = self.caller.\
                                  filter(self.filterParameterDictionary, False)
        
        # TODO draw the image
        # self.previewFigure = 
        
        #previewFigure.set_canvas(self.ui.widgetMpl.canvas)
        self.ui.widgetMpl.canvas.figure = self.previewFigure
        self.ui.widgetMpl.canvas.draw()
        
        # TODO This should scale the preview figure to fit the preview frame,
        # but doesn't work
        self.ui.widgetMpl.canvas.updateGeometry()
        
        # TODO the preview figure should accept clicks, because of scrollbars
        # etc.
        def onclick(event):
            fig.canvas.mpl_connect('button_press_event', onclick)
        
    def get_filter_parameters(self):
        """
        Gets the filtering parameters from the UI fields. Uses default
        working file as the filtering target file.
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
        
        if self.ui.checkBoxBandstop1.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['bandstop1'] = True
            
            dictionary['bandstop1_l_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq1.value() - \
                self.ui.doubleSpinBoxBandstopWidth1/2
                
            dictionary['bandstop1_h_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq1.value() + \
                self.ui.doubleSpinBoxBandstopWidth1/2
                        
            dictionary['bandstop1_trans_bandwidth'] = self.ui.\
                                    doubleSpinBoxBandstopwidth1.value()
            
            dictionary['bandstop1_length'] = str(self.ui.\
                                             lineEditBandstopLength1.text())
        else:
            dictionary['bandstop1'] = False
        
        if self.ui.checkBoxBandstop2.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['bandstop2'] = True
            
            dictionary['bandstop2_l_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq2.value() - \
                self.ui.doubleSpinBoxBandstopWidth2/2
            
            dictionary['bandstop2_h_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq2.value() + \
                self.ui.doubleSpinBoxBandstopWidth2/2
            
            dictionary['bandstop2_trans_bandwidth'] = self.ui.\
                                    doubleSpinBoxBandstopwidth2.value()
                                    
            dictionary['bandstop2_length'] = str(self.ui.\
                                             lineEditBandstopLength2.text())
        else:
            dictionary['bandstop2'] = False
            
        if self.ui.checkBoxBandstop3.isChecked() == True:
            dictionary['isEmpty'] = False
            dictionary['bandstop3'] = True
            
            dictionary['bandstop3_l_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq3.value() - \
                self.ui.doubleSpinBoxBandstopWidth3/2
            
            dictionary['bandstop3_h_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq3.value() + \
                self.ui.doubleSpinBoxBandstopWidth3/2
            
            dictionary['bandstop3_length'] = str(self.ui.\
                                             lineEditBandstopLength3.text())
        else:
            dictionary['bandstop3'] = False
            
        return dictionary    
    
    def accept(self):
        """
        Get the parameters dictionary and relay it to caller.filter to
        actually do the filtering.
        """
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        
        paramDict = self.get_filter_parameters()
        if paramDict.get('isEmpty') == True:
                self.messageBox = messageBox.AppForm()
                self.messageBox.labelException.setText('Please select ' +
                                                       'filter(s) to apply')
                self.messageBox.show()
                return    
        
        self.dataToFilter = self.parent.experiment.active_subject._working_file._data
        samplerate = self.parent.experiment.active_subject._working_file.info['sfreq']
        
         # Check if the filter frequency values are sane or not.
        # TODO preferably catch a custom exception from caller.filter
        self._validateFilterFreq(paramDict, samplerate)
        self._validateFilterLength(paramDict)
        
        filteredData = self.caller.filter(self.dataToFilter, 
                                                 samplerate, paramDict)
        
        # Replace the data in the working file with the filtered data
        self.parent.experiment.active_subject._working_file._data = filteredData
        
        # Update the working file info fields with the new values
        if 'lowpass' in paramDict and paramDict['lowpass'] == True:
            self.parent.experiment.active_subject._working_file.info['lowpass'] = \
                paramDict['low_cutoff_freq']
        
        if ( 'highpass' in paramDict and paramDict['highpass'] == True ):
            self.parent.experiment.active_subject._working_file.info['highpass'] = \
                paramDict['high_cutoff_freq']
                
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
        self.messageBox = messageBox.AppForm()
        self.messageBox.labelException.setText('Cutoff frequencies ' +
                    'should be lower than samplerate/2 ' +
                    '(' + 'current samplerate is ' + str(samplerate) + ' Hz)')
        self.messageBox.show()
        return
    
    def _validateFilterLength(self, paramDict):
        if 'lowpass' in paramDict and paramDict['lowpass'] == True:
            lowLengthString = paramDict['low_length']
            if ( not lowLengthString.endswith('ms') and 
                 not lowLengthString.endswith('s') ):
                self._showLengthError('low pass')
    
        if 'highpass' in paramDict and paramDict['highpass'] == True:
            highLengthString = paramDict['high_length']
            if ( not highLengthString.endswith('ms') and 
                 not highLengthString.endswith('s') ):
                self._showLengthError('high pass')
    
    def _showLengthError(self, filterSource):
        """
        Show the error for wrong type of filter length string.
        
        Keyword arguments:
        
        filterSource     -- which filter UI box is the source of error.
        """
        self.messageBox = messageBox.AppForm()
        self.messageBox.labelException.setText('Check filter length for ' + \
                        filterSource + '. It should end with \'s\' or \'ms\'')
        self.messageBox.show()
        return
    
    def reject(self):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        self.close()
      
    def closeEvent(self, event):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        event.accept()