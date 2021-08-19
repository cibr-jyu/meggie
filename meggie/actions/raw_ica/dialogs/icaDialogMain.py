""" Contains a class for logic of ica dialog.
"""

import logging

from PyQt5 import QtWidgets

from meggie.actions.raw_ica.dialogs.icaDialogUi import Ui_Dialog

from meggie.actions.raw_ica.controller.ica import plot_topographies
from meggie.actions.raw_ica.controller.ica import plot_sources
from meggie.actions.raw_ica.controller.ica import plot_properties
from meggie.actions.raw_ica.controller.ica import plot_changes
from meggie.actions.raw_ica.controller.ica import compute_ica

from meggie.utilities.threading import threaded
from meggie.utilities.messaging import exc_messagebox


class ICADialog(QtWidgets.QDialog):
    """ Contains logic for ICA dialog.
    """

    def __init__(self, parent, experiment, random_state, on_apply=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.parent = parent
        self.experiment = experiment
        self.on_apply = on_apply
        self.random_state = random_state

        # change normal list widgets to multiselect widgets
        self.ui.listWidgetNotRemoved.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.ui.listWidgetRemoved.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)

        self._reset()

    def _reset(self):
        self.ica = None
        self.ui.listWidgetNotRemoved.clear()
        self.ui.listWidgetRemoved.clear()
        self.not_removed = []
        self.removed = []
        self.component_info = {}
        self.params = {}

    def on_pushButtonCompute_clicked(self, checked=None):
        if checked is None:
            return

        # start by clearing out the previous things
        self._reset()

        n_components = self.ui.doubleSpinBoxNComponents.value()
        method = 'fastica'
        max_iter = self.ui.spinBoxMaxIter.value()

        raw = self.experiment.active_subject.get_raw()

        @threaded
        def _compute_ica():
            return compute_ica(raw, n_components, method, max_iter, self.random_state)

        try:
            self.ica = _compute_ica(do_meanwhile=self.parent.update_ui)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.params['n_components'] = n_components
        self.params['method'] = method
        self.params['max_iter'] = max_iter
        self.params['random_state'] = self.random_state

        for idx in range(self.ica.n_components_):
            label = 'Component ' + str(idx)
            self.ui.listWidgetNotRemoved.addItem(label)
            self.component_info[label] = idx
            self.not_removed.append(label)

        logging.getLogger('ui_logger').info('Computing ICA model finished.')

    def on_pushButtonTransfer_clicked(self, checked=None):
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
        # Enforce only one list have a selected item
        widget = self.ui.listWidgetRemoved
        for i in range(widget.count()):
            widget.item(i).setSelected(False)

    def on_listWidgetRemoved_clicked(self):
        # Enforce only one list have a selected item
        widget = self.ui.listWidgetNotRemoved
        for i in range(widget.count()):
            widget.item(i).setSelected(False)

    def on_pushButtonPlotTopographies_clicked(self, checked=None):
        if checked is None:
            return

        raw = self.experiment.active_subject.get_raw()

        try:
            plot_topographies(self.ica, len(self.component_info))
        except Exception as exc:
            exc_messagebox(self, exc)
            return

    def on_pushButtonPlotSources_clicked(self, checked=None):
        if checked is None:
            return

        raw = self.experiment.active_subject.get_raw()

        try:
            plot_sources(raw, self.ica)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

    def on_pushButtonPlotProperties_clicked(self, checked=None):
        if checked is None:
            return

        picks = self._get_picks()

        if not picks:
            return

        raw = self.experiment.active_subject.get_raw()

        try:
            plot_properties(raw, self.ica, picks)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

    def on_pushButtonPlotChanges_clicked(self, checked=None):
        if checked is None:
            return

        raw = self.experiment.active_subject.get_raw()

        indices = [self.component_info[name] for name in self.removed]

        try:
            plot_changes(raw, self.ica, indices)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

    def _get_picks(self):
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
        if not self.ica:
            return

        raw = self.experiment.active_subject.get_raw()

        indices = [self.component_info[name] for name in self.removed]

        try:
            @threaded
            def apply_ica_wrapper():
                self.ica.apply(raw, exclude=indices)

            apply_ica_wrapper(do_meanwhile=self.parent.update_ui)

            self.experiment.active_subject.save()
            self.experiment.active_subject.ica_applied = True
            self.experiment.save_experiment_settings()
     
        except Exception as exc:
            exc_messagebox(self, exc)
            return

        self.parent.initialize_ui()

        # for logging purposes, call the handler
        if self.on_apply:
            self.params['exclude'] = indices
            self.on_apply(self.experiment.active_subject, self.params)

        self._reset()
        self.close()
