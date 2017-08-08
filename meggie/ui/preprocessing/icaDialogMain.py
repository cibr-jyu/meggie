# coding: utf-8
'''
Created on Aug 02, 2017

@author: erpipehe
'''
from copy import deepcopy

import mne
import numpy as np

from PyQt4 import QtGui

from meggie.code_meggie.general.caller import Caller
from meggie.ui.preprocessing.icaDialogUi import Ui_Dialog

import meggie.code_meggie.general.fileManager as fileManager

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

        self.caller = Caller.Instance()

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
        max_iter = self.ui.spinBoxMaxIter.value()

        self.ica = mne.preprocessing.ICA(
            n_components=n_components,
            method='fastica',
            max_iter=max_iter)

        raw = self.caller.experiment.active_subject.get_working_file()
        self.ica.fit(raw)

        # TODO: what if ica does not converge?
        # TODO: what happens to different type of channels?

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

        figs = self.ica.plot_components()

        def update_topography_texts():
            """ Little trick to allow clean return out of nested loops """
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
        """ Plot the property windows for all selected items
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

    def on_pushButtonPlotChanges_clicked(self, checked=None):
        """
        """
        if checked is None:
            return

        raw = self.caller.experiment.active_subject.get_working_file()

        raw_removed = raw.copy()
        indices = [self.component_info[name] for name in self.removed]
        self.ica.apply(raw_removed, exclude=indices)

        changes_raw = self.prepare_raw_for_changes(raw_removed, raw)
        changes_raw.plot(color='red', bad_color='blue')

    def prepare_raw_for_changes(self, raw_new, raw_old):
        """ Modifies first raw object in place so that the second raw object is
        interleaved to first one
        """

        new_info = raw_old.info.copy()
        new_info['nchan'] = 2*raw_old.info['nchan']

        ch_names = []
        for ch_name in raw_old.info['ch_names']:
            ch_names.append(ch_name + ' (old)')
            ch_names.append(ch_name + ' (new)')
        new_info['ch_names'] = ch_names

        chs = []
        for idx, ch in enumerate(raw_old.info['chs']):
            ch_1 = deepcopy(ch)
            ch_1['ch_name'] = new_info['ch_names'][idx*2]
            chs.append(ch_1)

            ch_2 = deepcopy(ch)
            ch_2['ch_name'] = new_info['ch_names'][idx*2+1]
            chs.append(ch_2)
        new_info['chs'] = chs

        new_info['bads'] = [name for idx, name in enumerate(new_info['ch_names'])
                            if idx%2 == 0]

        raw_new.info = new_info

        raw_old_data = raw_old._data
        raw_new_data = raw_new._data

        data = np.zeros((raw_old_data.shape[0]*2, raw_old_data.shape[1]))
        data[0::2, :] = raw_old_data
        data[1::2, :] = raw_new_data

        raw_new._data = data

        return raw_new

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

        raw = self.caller.experiment.active_subject.get_working_file()

        indices = [self.component_info[name] for name in self.removed]
        self.ica.apply(raw, exclude=indices)

        fileManager.save_raw(self.caller.experiment, raw,
                             raw.info['filename'], overwrite=True)

        self.initialize()
        self.close()
