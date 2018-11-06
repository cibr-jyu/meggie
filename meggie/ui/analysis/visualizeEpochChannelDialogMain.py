"""
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import numpy as np

import meggie.code_meggie.general.mne_wrapper as mne

from meggie.ui.analysis.visualizeEpochChannelDialogUi import Ui_VisualizeEpochChannelDialog


class VisualizeEpochChannelDialog(QtWidgets.QDialog):
    
    """A dialog for visualizing epoch channels with custom parameters
    """
    
    def __init__(self, epochs=None):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_VisualizeEpochChannelDialog()
        self.ui.setupUi(self)
        self.epochs = epochs

        if epochs is None: 
            return

        # fills channels list with epoch collection channel names.
        for channel in epochs.raw.ch_names:
            item = QtWidgets.QListWidgetItem()
            item.setText(channel)
            self.ui.listWidgetChannels.addItem(item)
        
    def on_pushButtonVisualizeChannel_clicked(self, checked=None):
        
        if checked is None: 
            return
        
        pick = self.epochs.raw.ch_names.index(
            self.ui.listWidgetChannels.currentItem().text())
        sigma = self.ui.doubleSpinBoxSigma.value()

        fig = mne.plot_epochs_image(self.epochs.raw, pick, sigma=sigma,
                                        colorbar=True,
                                        order=None, show=True)

        fig[0].canvas.set_window_title('_'.join(['Viz_channel',
                                       self.epochs.collection_name,
                                       self.epochs.raw.ch_names[pick]]))
