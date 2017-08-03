# coding: utf-8
'''
Created on Aug 02, 2017

@author: erpipehe
'''

import mne

from PyQt4 import QtCore,QtGui

from meggie.code_meggie.general.caller import Caller
from meggie.ui.preprocessing.icaDialogUi import Ui_Dialog
from meggie.ui.utils.messaging import messagebox

class ICADialog(QtGui.QDialog):
    """
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

        self.caller = Caller.Instance()

    def initialize(self):
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
        max_iter = self.ui.spinBoxMaxIter.value()

        self.ica = mne.preprocessing.ICA(
            n_components=n_components, 
            method='fastica',
            max_iter=max_iter)

        raw = self.caller.experiment.active_subject.get_working_file()
        self.ica.fit(raw)

        # TODO: what if ica does not converge?

        for idx in range(self.ica.n_components_):
            label = 'Component ' + str(idx+1)
            self.ui.listWidgetNotRemoved.addItem(label)
            self.component_info[label] = idx
            self.not_removed.append(label)

        print "ICA finished."

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
        """ enforce only one list have a selected item
        """
        widget = self.ui.listWidgetRemoved
        for i in range(widget.count()):
            widget.item(i).setSelected(False)

    def on_listWidgetRemoved_clicked(self):
        """ enforce only one list have a selected item
        """
        widget = self.ui.listWidgetNotRemoved
        for i in range(widget.count()):
            widget.item(i).setSelected(False)

    def on_pushButtonPlotTopographies_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        figs = self.ica.plot_components()

        def update_topography_texts():
            idx = 1
            for fig in figs:
                for ax in fig.get_axes():
                    if idx > len(self.component_info):
                        return

                    ax.set_title('Component ' + str(idx), fontsize=12)
                    idx += 1

        update_topography_texts()

    def on_pushButtonPlotSources_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        raw = self.caller.experiment.active_subject.get_working_file()
        sources = self.ica.get_sources(raw)

        # alter amplitudes to get better plot, this is heuristic
        for source in sources._data:
            for idx, amplitude in enumerate(source):
                source[idx] = amplitude / 5000.0

        sources.plot()

    def on_pushButtonPlotProperties_clicked(self, checked=None):
        """ plot the property windows for all selected items
        """
        if checked is None:
            return

        picks = self.get_picks()

        raw = self.caller.experiment.active_subject.get_working_file()
        figs = self.ica.plot_properties(raw)

        # fix the names
        idx = 0
        for fig in figs:
            for ax_idx, ax in enumerate(fig.get_axes()):
                if ax_idx == 0:
                    ax.set_title("Component " + str(picks[idx] + 1))
                    idx += 1
                break

    def on_pushButtonPlotOverlay_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        picks = self.get_picks()

        raw = self.caller.experiment.active_subject.get_working_file()

        # TODO: implement overlay, maybe try to utilize the raw plot


    def get_picks(self):
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
        Apply the zeroing.
        """

        print "Miau"

        self.ica = None
        self.close()
