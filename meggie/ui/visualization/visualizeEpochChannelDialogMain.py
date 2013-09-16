'''
Created on Sep 12, 2013

@author: jaolpeso
'''

from PyQt4 import QtCore, QtGui

import mne

from visualizeEpochChannelDialogUi import Ui_VisualizeEpochChannelDialog


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
        for channel in epochs.ch_names:
            item = QtGui.QListWidgetItem()
            item.setText(channel)
            self.ui.listWidgetChannels.addItem(item)
        
    def on_pushButtonVisualizeChannel_clicked(self, checked=None):
        
        if checked is None: return
        pick = self.epochs.ch_names.index(self.ui.listWidgetChannels.currentItem().text())
        sigma = self.ui.doubleSpinBoxSigma.value()
        vmin = self.ui.spinBoxVmin.value()
        vmax = self.ui.spinBoxVmax.value()
        # plot_image_epochs averages the epochs before visualizing. 
        mne.viz.plot_image_epochs(self.epochs, pick, sigma=sigma, vmin=vmin,
                    vmax=vmax, colorbar=True, order=None, show=True)