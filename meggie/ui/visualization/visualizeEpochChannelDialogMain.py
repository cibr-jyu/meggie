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
        
        for i in range(304):
            item = QtGui.QListWidgetItem()
            item.setText(self.epochs.ch_names[i])
            self.ui.listWidgetChannels.addItem(item)
        
    def on_pushButtonVisualizeChannels_clicked(self, checked=None):
        
        if checked is None: return
        """
        picks_channel = []
        picks = ['MEG 2443', 'MEG 2113']
        for name in picks:
            if name.startswith('MEG'):
                if name.endswith(('2', '3')):
                    key = name[-4:-1]
                    picks_channel.append(int(key))
        """
        pick = self.epochs.ch_names.index(self.ui.listWidgetChannels.currentItem().text())
        sigma = self.ui.doubleSpinBoxSigma.value()
        vmin = self.ui.spinBoxVmin.value()
        vmax = self.ui.spinBoxVmax.value()
        #epochs = self.epochList.ui.listWidgetEpochs.currentItem().data(32).toPyObject()
        mne.viz.plot_image_epochs(self.epochs, pick, sigma=sigma, vmin=vmin,
                    vmax=vmax, colorbar=True, order=None, show=True)
        
        
        
        
        