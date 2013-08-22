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
        
        # Give parameters to plot() if you want to preview only the first 10s
        # or so.
        previewFigure = self.parent.experiment.working_file.plot(show=False, n_channels=10)
        
        self.ui.widgetMpl.canvas.figure = previewFigure
        self.ui.widgetMpl.canvas.draw()
        
        # TODO This should scale the preview info to fit the preview frame 
        self.ui.widgetMpl.canvas.updateGeometry()
        previewFigure.clear()
        