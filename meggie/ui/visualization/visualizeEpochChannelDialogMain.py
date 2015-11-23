'''
Created on Sep 12, 2013

@author: jaolpeso
'''

from PyQt4 import QtCore, QtGui

import mne

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
        for channel in epochs.ch_names:
            item = QtGui.QListWidgetItem()
            item.setText(channel)
            self.ui.listWidgetChannels.addItem(item)
        
    def on_pushButtonVisualizeChannel_clicked(self, checked=None):
        
        if checked is None: return
        
        # TODO: Add possibility for multiple channel picks if needed
        # fig -> figs (list of figures), pick -> picks (list of selected items
        # texts).
        #
        # picks = [] # can be list of strings since mne seems to convert
        # for item in self.ui.listWidgetChannels.selectedItems():
        #     picks.append(item.text())
        # for fig in figs:
        #     fig.canvas.set_window_title(title)
        
        pick = self.epochs.ch_names.index(self.ui.listWidgetChannels.currentItem().text())
        sigma = self.ui.doubleSpinBoxSigma.value()
        vmin = self.ui.spinBoxVmin.value()
        vmax = self.ui.spinBoxVmax.value()
        # plot_image_epochs averages the epochs before visualizing. 
        fig = mne.viz.plot_image_epochs(self.epochs, pick, sigma=sigma,
                                        vmin=vmin, vmax=vmax, colorbar=True,
                                        order=None, show=True)
        title = ''
        for event_name in self.epochs.event_id.keys():
            if title == '':
                title += event_name
            else:
                title += ' - ' + event_name
        fig[0].canvas.set_window_title(title)
