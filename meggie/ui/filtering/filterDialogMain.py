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
        self.previewFile = None
        self.previewFigure = None
        
    def on_pushButtonPreview_clicked(self, checked=None):
        """
        Draws the preview.
        """
        if checked is None: return
        self.drawPreview()      
        
    def drawPreview(self):
        """
        Draws the preview into the preview window with with raw.plot()
        """
        
        # Clear the previous figure to keep the pyplot state environment clean
        # and save memory. 
        if self.previewFigure != None:
            plt.close(self.previewFigure)
   
        
        """
        Pitäisi:
        1. Ottaa working filen data
        2. Lukea filteriparametrit
        3. Soveltaa filteröintiä working filen dataan
        4. Laittaa filteröity data previewfileen
        5. Plotata previewfile 
        6. Jos sitten painetaan OK-nappia, tehdä tuosta previewfilestä working file
        (esim. nimellä "entinenworkingfilennimi"+ filtered.fif
        7. Cancel-napin tapauksessa hävittää se previewfile 
        8. Jos taas painaa OK:ta ennen preview-nappia, pitää vain filteröidä
        working fileä suoraan (tähän on erillinen metodi)
        """
        
        # Plot the filtered channels with mne.fiff.raw.plot (which is based
        # on pylab, therefore needing manual cleaning of pyplot state
        # environment.
        
        filterParameterDictionary = self.get_filter_parameters()
        self.previewFile = caller.filter(filterParameterDictionary, False)
        
        self.previewFigure = self.previewFile.plot(show=False, n_channels=10)
        
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
        working file as the filterin target file.
        """
        checkedButton = self.ui.buttonGroupFilterTypes.checkedButton() 
        checkedButtonName = checkedButton.objectName()
        
        filterType = self.get_filter_type_string(checkedbuttonName)
        
        raw = parent.experiment.working_file
        dictionary = { 'i' : raw }
        
        if checkedButtonName == 'radioButtonLowpass':
            
            dictionary['l_freq'] = self.ui.doubleSpinBoxLowpassCutoff.value()
            dictionary['l_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxLowpassTransBandwidth.value()
            dictionary['method'] = self.ui.buttonGroupLowpassMethod.\
                                    checkedButton().text
            return dictionary
        
        if checkedButtonName == 'radioButtonHighpass':
            dictionary['h_freq'] = self.ui.doubleSpinBoxHighpassCutoff.value()
            dictionary['h_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxHighpassTransBandwidth.value()
            dictionary['method'] = self.ui.buttonGroupHighpassMethod.\
                                    checkedButton().text
            return dictionary
            
        if checkedButtonName == 'radioButtonBandpass':
            dictionary['l_freq'] = self.ui.doubleSpinBoxLowpassCutoff.value()
            dictionary['l_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxLowpassTransBandwidth.value()
            dictionary['h_freq'] = self.ui.doubleSpinBoxHighpassCutoff.value()
            dictionary['h_trans_bandwidth'] = self.ui.\
                        doubleSpinBoxHighpassTransBandwidth.value()
                        
            dictionary['method'] = self.ui.buttonGroupBandpassMethod.\
                                    checkedButton().text
            return dictionary    
    
    def accept(self):
        """
        Collects the parameters and passes them
        to the caller class.
        """
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        
        if self.previewFile == None:
            caller.filter(filterParameterDictionary, True)
        else:
            parent.experiment.working_file = self.previewFile
        
        self.close()
    
    def reject(self):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        self.close()
      
    def closeEvent(self, event):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        event.accept()