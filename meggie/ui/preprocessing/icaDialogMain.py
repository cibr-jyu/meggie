# coding: utf-8
'''
Created on Aug 02, 2017

@author: erpipehe
'''

import logging

from PyQt4 import QtGui

from meggie.ui.preprocessing.icaDialogUi import Ui_Dialog
from meggie.ui.utils.decorators import threaded

from meggie.code_meggie.preprocessing.ica import plot_topographies
from meggie.code_meggie.preprocessing.ica import plot_sources
from meggie.code_meggie.preprocessing.ica import plot_properties
from meggie.code_meggie.preprocessing.ica import plot_changes
from meggie.code_meggie.preprocessing.ica import compute_ica
from meggie.code_meggie.preprocessing.ica import apply_ica

from meggie.ui.utils.messaging import exc_messagebox


class ICADialog(QtGui.QDialog):
    """ Functionality for ICA dialog UI
    """

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        # change normal list widgets to multiselect widgets
        self.ui.listWidgetNotRemoved.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)
        self.ui.listWidgetRemoved.setSelectionMode(
            QtGui.QAbstractItemView.ExtendedSelection)

        self.initialize()

    def initialize(self):
        """ Resets all the storage
        """
        self.ica = None
        self.ui.listWidgetNotRemoved.clear()
        self.ui.listWidgetRemoved.clear()
        self.not_removed = []
        self.removed = []
        self.component_info = {}

    def on_pushButtonCompute_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        # start by clearing out the previous things
        self.initialize()

        n_components = self.ui.doubleSpinBoxNComponents.value()
        method = 'fastica'
        max_iter = self.ui.spinBoxMaxIter.value()

        raw = self.parent.experiment.active_subject.get_working_file()

        @threaded
        def _compute_ica():
            return compute_ica(raw, n_components, method, max_iter)

        try:
            self.ica = _compute_ica()
        except Exception as e:
            exc_messagebox(self, e)
            return

        for idx in range(self.ica.n_components_):
            label = 'Component ' + str(idx+1)
            self.ui.listWidgetNotRemoved.addItem(label)
            self.component_info[label] = idx
            self.not_removed.append(label)

        logging.getLogger('ui_logger').info('ICA finished.')

    def on_pushButtonTransfer_clicked(self, checked=None):
        """ Transfers items from list to another. QListWidgets are the necessary evil
        so the self.removed_items and self.not_removed_items are also kept in sync
        """
        if checked is None:
            return

        # gather contents of the widgets
        not_removed_selected = [item.text() for item in
                                self.ui.listWidgetNotRemoved.selectedItems()]
        removed_selected = [item.text() for item in
                            self.ui.listWidgetRemoved.selectedItems()]

        # update the "backend"
        for item in not_removed_selected:
            self.not_removed.remove(item)
            self.removed.append(item)

        for item in removed_selected:
            self.removed.remove(item)
            self.not_removed.append(item)

        self.not_removed.sort(key=lambda x: self.component_info[x])
        self.removed.sort(key=lambda x: self.component_info[x])

        # clear ui
        self.ui.listWidgetNotRemoved.clear()
        self.ui.listWidgetRemoved.clear()

        # fill again
        for item in self.removed:
            self.ui.listWidgetRemoved.addItem(item)
        for item in self.not_removed:
            self.ui.listWidgetNotRemoved.addItem(item)

    def on_listWidgetNotRemoved_clicked(self):
        """ Enforce only one list have a selected item
        """
        widget = self.ui.listWidgetRemoved
        for i in range(widget.count()):
            widget.item(i).setSelected(False)

    def on_listWidgetRemoved_clicked(self):
        """ Enforce only one list have a selected item
        """
        widget = self.ui.listWidgetNotRemoved
        for i in range(widget.count()):
            widget.item(i).setSelected(False)

    def on_pushButtonPlotTopographies_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        plot_topographies(self.ica, len(self.component_info))

    def on_pushButtonPlotSources_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        raw = self.parent.experiment.active_subject.get_working_file()

        plot_sources(raw, self.ica)


    def on_pushButtonPlotProperties_clicked(self, checked=None):
        """ Plot the property windows for all selected items
        """
        if checked is None:
            return

        picks = self.get_picks()

        raw = self.parent.experiment.active_subject.get_working_file()

        plot_properties(raw, self.ica, picks)

    def on_pushButtonPlotChanges_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        raw = self.parent.experiment.active_subject.get_working_file()

        indices = [self.component_info[name] for name in self.removed]

        plot_changes(raw, self.ica, indices)

    def get_picks(self):
        """ Finds out the indices off all the selected components
        """
        not_removed_selected = [item.text() for item in
                                self.ui.listWidgetNotRemoved.selectedItems()]
        removed_selected = [item.text() for item in
                            self.ui.listWidgetRemoved.selectedItems()]

        picks = [self.component_info[label]
                 for label in not_removed_selected]
        picks.extend([self.component_info[label]
                      for label in removed_selected])

        picks = sorted(picks)
        return picks

    def accept(self):
        """
        Transform and save the data.
        """

        if not self.ica:
            return

        raw = self.parent.experiment.active_subject.get_working_file()

        indices = [self.component_info[name] for name in self.removed]

        apply_ica(raw, self.parent.experiment, self.ica, indices)

        self.initialize()
        self.close()
