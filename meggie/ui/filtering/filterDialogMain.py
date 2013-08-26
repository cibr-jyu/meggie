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
        
        # experiment._working_file.data on se, joka pitäisi ottaa plotattavaksi
        # 
        
        
        # Give parameters to plot() if you want to preview only the first 10s
        # or so.
        self.previewFigure = self.parent.experiment.working_file.plot(show=False,
                                                                 n_channels=10)
        
        #previewFigure.set_canvas(self.ui.widgetMpl.canvas)
        self.ui.widgetMpl.canvas.figure = self.previewFigure
        self.ui.widgetMpl.canvas.draw()
        
        # TODO This should scale the preview figure to fit the preview frame,
        # but doesn't work
        self.ui.widgetMpl.canvas.updateGeometry()
        
        def onclick(event):
            fig.canvas.mpl_connect('button_press_event', onclick)
        
    def accept(self):
        """
        Collects the parameters and passes them
        to the caller class.
        """
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        
        
        
        if self.ui.checkBoxLowpass.isChecked() == True:
            dictionary = {  }
        
        self.close()
    
    def reject(self):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        self.close()
      
    def closeEvent(self, event):
        if self.previewFigure != None:
            plt.close(self.previewFigure)
        event.accept()