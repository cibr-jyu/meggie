# coding: utf-8

"""
"""

import logging

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.utilities.dynamic import find_all_tab_specs

from meggie.utilities.dialogs.customTabsDialogUi import Ui_customTabsDialog


class CustomTabsDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, enabled_tabs):
        """
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_customTabsDialog()
        self.ui.setupUi(self)

        all_tabs = find_all_tab_specs()

        tablist = []
        if enabled_tabs:
            for tab_id in enabled_tabs:
                if tab_id in all_tabs:
                    tablist.append(tab_id)

        for tab_id in all_tabs:
            if tab_id not in enabled_tabs:
                tablist.append(tab_id)
        for tab_id in tablist:
            item = QtWidgets.QListWidgetItem(tab_id)
            self.ui.listWidgetTabs.addItem(item)
            if str(item.text()) in enabled_tabs:
                item.setSelected(True)

    def accept(self):
        self.enabled_tabs = [str(item.text()) for item in 
                             self.ui.listWidgetTabs.selectedItems()]
        self.close()
