import os
import logging
import shutil

from PyQt4 import QtGui

from meggie.ui.general.tabs.mainWindowTabSpectrumsUi import Ui_mainWindowTabSpectrums  # noqa

from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.decorators import threaded

import meggie.code_meggie.general.fileManager as fileManager
import meggie.code_meggie.general.mne_wrapper as mne


class MainWindowTabSpectrums(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_mainWindowTabSpectrums()
        self.ui.setupUi(self)

        self.initialize_ui()


    def initialize_ui(self):

        if not self.parent.experiment:
            return

        active_subject = self.parent.experiment.active_subject

        if active_subject is None:
            return

        # do something :)

