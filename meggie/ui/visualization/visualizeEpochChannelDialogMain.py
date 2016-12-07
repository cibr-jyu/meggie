'''
Created on Sep 12, 2013

@author: jaolpeso
'''

from PyQt4 import QtCore, QtGui

import mne
import numpy as np

from meggie.ui.visualization.visualizeEpochChannelDialogUi import Ui_VisualizeEpochChannelDialog


class VisualizeEpochChannelDialog(QtGui.QDialog):
    
    """A dialog for visualizing epoch channels with custom parameters
    """
    
    def __init__(self, epochs=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_VisualizeEpochChannelDialog()
        self.ui.setupUi(self)
        self.epochs = epochs
        if epochs is None: return
        # Fills channels list with epoch collection channel names.
        for channel in epochs.raw.ch_names:
            item = QtGui.QListWidgetItem()
            item.setText(channel)
            self.ui.listWidgetChannels.addItem(item)
        
    def on_pushButtonVisualizeChannel_clicked(self, checked=None):
        
        if checked is None: return
        
        # TODO: Add possibility for multiple channel picks if needed
        pick = self.epochs.raw.ch_names.index(
            self.ui.listWidgetChannels.currentItem().text())
        sigma = self.ui.doubleSpinBoxSigma.value()
        # plot_image_epochs averages the epochs before visualizing. 
        fig = mne.viz.plot_epochs_image(self.epochs.raw, pick, sigma=sigma,
                                        colorbar=True,
                                        order=None, show=True)