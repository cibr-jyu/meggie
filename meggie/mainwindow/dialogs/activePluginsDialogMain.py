""" Contains a logic for setting active plugins.
"""

import logging
import pkg_resources
import json

from PyQt5 import QtWidgets

from meggie.mainwindow.dynamic import find_all_plugins
from meggie.mainwindow.dynamic import find_all_package_specs

from meggie.mainwindow.dialogs.activePluginsDialogUi import Ui_activePluginsDialog


class ActivePluginsDialog(QtWidgets.QDialog):
    """ Contains logic for active plugins dialog.
    """

    def __init__(self, active_plugins, parent, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_activePluginsDialog()
        self.ui.setupUi(self)

        self.handler = handler

        plugins = find_all_plugins()
        package_specs = find_all_package_specs()


        plugin_info = []
        for source, package_spec in package_specs.items():
            if source not in plugins:
                continue

            id_ = package_spec['id']
            name = package_spec['name']
            author = package_spec['author']

            plugin_info.append((id_, name, author))
        self.plugin_info = plugin_info

        for id_, name, author in plugin_info:
            text = name + ' - ' + author
            item = QtWidgets.QListWidgetItem(text)
            self.ui.listWidgetPlugins.addItem(item)
            if id_ in active_plugins:
                item.setSelected(True)

    def accept(self):
        idxs = [elem.row() for elem in self.ui.listWidgetPlugins.selectedIndexes()]
        active_plugins = [self.plugin_info[idx][0] for idx in idxs]
        self.handler(active_plugins)
        self.close()
