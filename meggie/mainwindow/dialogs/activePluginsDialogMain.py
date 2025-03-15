"""Contains a logic for setting active plugins."""

from PyQt5 import QtWidgets, QtCore

from meggie.mainwindow.dynamic import find_all_plugins
from meggie.mainwindow.dynamic import find_all_package_specs

from meggie.mainwindow.dialogs.activePluginsDialogUi import Ui_activePluginsDialog


class ActivePluginsDialog(QtWidgets.QDialog):
    """Contains logic for active plugins dialog."""

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

            id_ = package_spec["id"]
            name = package_spec["name"]
            author = package_spec["author"]

            plugin_info.append((id_, name, author))
        self.plugin_info = plugin_info

        for id_, name, author in plugin_info:
            text = name + " - " + author
            item = QtWidgets.QListWidgetItem(text)
            self.ui.listWidgetPlugins.addItem(item)
            if id_ in active_plugins:
                item.setSelected(True)

        # Create the hyperlink label
        self.link_label = QtWidgets.QLabel(self)
        self.link_label.setTextFormat(QtCore.Qt.RichText)
        self.link_label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.link_label.setOpenExternalLinks(True)

        # Define URL as a variable for reuse
        plugin_url = "https://cibr-jyu.github.io/meggie/user-guide/plugins"

        self.link_label.setText(
            f'Find and install plugins: <a href="{plugin_url}">Documentation</a>'
        )

        # Add tooltip with full URL
        self.link_label.setToolTip(plugin_url)

        # Insert the link label below the plugin list
        self.ui.gridLayout.addWidget(self.link_label, 1, 0)

        # Move buttons to next row
        self.ui.gridLayout.removeItem(self.ui.horizontalLayout)
        self.ui.gridLayout.addLayout(self.ui.horizontalLayout, 2, 0)

    def accept(self):
        idxs = [elem.row() for elem in self.ui.listWidgetPlugins.selectedIndexes()]
        active_plugins = [self.plugin_info[idx][0] for idx in idxs]
        self.handler(active_plugins)
        self.close()
