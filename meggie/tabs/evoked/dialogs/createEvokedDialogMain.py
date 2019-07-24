# coding: utf-8

"""
"""

import logging

from PyQt5 import QtCore
from PyQt5 import QtWidgets

import numpy as np

from meggie.tabs.evoked.dialogs.createEvokedDialogUi import Ui_CreateEvokedDialog

from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget

from meggie.utilities.decorators import threaded
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.validators import validate_name


class CreateEvokedDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, experiment, parent):
        """Initialize the event selection dialog.

        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_CreateEvokedDialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment

        self.batching_widget = BatchingWidget(
            experiment_getter=self.experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry())
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def experiment_getter(self):
        return self.experiment

    def accept(self):
        pass

    def acceptBatch(self):
        pass

