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
import validator

import messageBox

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
        Pitäisi:
        (0. Previewin pitäisi laskea xfit-tyylinen käppyrä)
        - Kiskoa datataulukko raw-filestä (vaatii sampleraten lukemista)
        - Lukea parametrit UI:sta ja päättää, mitä kaikki metodeja kutsutaan
        - Käyttää filterimetodeita dataan (järjestyksellä ei väliä)
        - Kopioida data takaisin ja muuttaa ao. infokenttiä
        
        """
        
        # Plot the filtered channels with mne.fiff.raw.plot (which is based
        # on pylab, therefore needing manual cleaning of pyplot state
        # environment.
        
        self.filterParameterDictionary = self.get_filter_parameters()
        self.previewFile = self.parent.caller.\
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
        
        if self.ui.checkBoxLowpass.isChecked() == True:
            dictionary['lowpass'] = True
            
            dictionary['low_cutoff_freq'] = self.ui.\
                                       doubleSpinBoxLowpassCutoff.value()
            dictionary['low_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxLowpassTransBandwidth.value()
            dictionary['low_length'] = str(self.ui.\
                                    doubleSpinBoxLowpassFilterLength.value())
        else:
            dictionary['lowpass'] = True
        
        if self.ui.checkBoxHighpass.isChecked() == True:
            dictionary['highpass'] = True
            
            dictionary['high_cutoff_freq'] = self.ui.\
                                        doubleSpinBoxHighpassCutoff.value()
            dictionary['high_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxHighpassTransBandwidth.value()
            dictionary['high_length'] = str(self.ui.\
                                    doubleSpinBoxHighpassFilterLength.value())
        else:
            dictionary['lowpass'] = True
        
        if self.ui.checkBoxBandstop1.isChecked() == True:
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
                                    doubleSpinBoxBandstopFilterLength1.value())
        else:
            dictionary['bandstop1'] = False
        
        if self.ui.checkBoxBandstop2.isChecked() == True:
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
                                    doubleSpinBoxBandstopFilterLength2.value())
        else:
            dictionary['bandstop2'] = False
            
        if self.ui.checkBoxBandstop3.isChecked() == True:
            dictionary['bandstop3'] = True
            
            dictionary['bandstop3_l_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq3.value() - \
                self.ui.doubleSpinBoxBandstopWidth3/2
            
            dictionary['bandstop3_h_freq'] = \
                self.ui.doubleSpinBoxBandstopFreq3.value() + \
                self.ui.doubleSpinBoxBandstopWidth3/2
            
            dictionary['bandstop3_length'] = str(self.ui.\
                                    doubleSpinBoxBandstopFilterLength3.value())
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
        
        self.dataToFilter = self.parent.experiment.working_file._data
        samplerate = self.parent.experiment.working_file.info['sfreq']
        filteredData = self.parent.caller.filter(self.dataToFilter, 
                                                 samplerate, paramDict)
        
        # Replace the data in the working file with the filtered data
        self.parent.experiment.working_file._data = filteredData
        
        # Update the working file info fields with the new values
        if paramDict['lowpass'] == True:
            self.parent.experiment.working_file.info['lowpass'] = \
                paramDict['low_cutoff_freq']
        
        if paramDict['highpass'] == True:
            self.parent.experiment.working_file.info['highpass'] = \
                paramDict['high_cutoff_freq']
                
        self.close()
    
    def reject(self):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        self.close()
      
    def closeEvent(self, event):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        event.accept()