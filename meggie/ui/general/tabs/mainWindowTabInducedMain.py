import os
import logging
import shutil

from PyQt4 import QtGui

from meggie.ui.general.tabs.mainWindowTabInducedUi import Ui_mainWindowTabInduced  # noqa

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabInduced(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabInduced()
        self.ui.setupUi(self)

        self.initialize_ui()


    def initialize_ui(self):

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        # do something :)

 
    def on_pushButtonTFR_clicked(self, checked=None):
        """Open the dialog for plotting TFR from a single channel."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return
        
        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must select epochs before TFR.'
            messagebox(self, message)
            return
        
        selected_items = self.epochList.ui.listWidgetEpochs.selectedItems()
        
        if len(selected_items) == 1:
            collection_name = selected_items[0].text()
        else:
            message = 'Select exactly one epoch collection.'
            messagebox(self, message)
            return
        
        epochs = self.experiment.active_subject.epochs.get(collection_name)

        self.tfr_dialog = TFRDialog(self, epochs)
        self.tfr_dialog.show()
        
    def on_pushButtonTFRTopology_clicked(self, checked=None):
        """Opens the dialog for plotting TFR topology."""
        if checked is None:
            return
        if self.experiment.active_subject is None:
            return

        if self.epochList.ui.listWidgetEpochs.currentItem() is None:
            message = 'You must select epochs for TFR.'
            messagebox(self, message)
            return 
        
        selected_items = self.epochList.ui.listWidgetEpochs.selectedItems()
        
        if len(selected_items) == 1:
            collection_name = selected_items[0].text()
        else:
            message = 'Select exactly one epoch collection.'
            messagebox(self, message)
            return
        
        self.tfrTop_dialog = TFRTopologyDialog(self, collection_name)
        self.tfrTop_dialog.show()



