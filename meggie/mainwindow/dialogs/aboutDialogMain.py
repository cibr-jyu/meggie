""" Contains a class for logic of about dialog.
"""

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from meggie.mainwindow.dialogs.aboutDialogUi import Ui_Dialog


class AboutDialog(QtWidgets.QDialog):
    """ Contains the main logic for about dialog.
    """

    def __init__(self, parent):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        version = ''
        try:
            import pkg_resources
            version = pkg_resources.get_distribution("meggie").version
        except BaseException:
            pass

        self.ui.lineEditVersion.setText(str(version))

    def on_pushButtonClose_clicked(self, checked=None):
        if checked is None:
            return
        self.close()
