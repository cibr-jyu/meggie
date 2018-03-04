"""
@author: Erkka Heinila
"""

from PyQt4 import QtGui

from meggie.ui.source_analysis.inverseOperatorDialogUi import Ui_inverseOperatorDialog  # noqa

from meggie.code_meggie.general.source_analysis import create_inverse_operator  # noqa

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.decorators import threaded

class InverseOperatorDialog(QtGui.QDialog):
    """
    """

    def __init__(self, parent, based_on, experiment=None, on_close=None):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_inverseOperatorDialog()
        self.ui.setupUi(self)
        self.on_close = on_close
        self.experiment = experiment
        self.based_on = based_on

        self.ui.lineEditBasedOn.setText(based_on)

    def accept(self):
        """
        """

        # collect parameters
        name = str(self.ui.lineEditInverseOperatorName.text())
        if not name:
            messagebox(self, "Please give a name for the inverse operator")
            return

        based_on = self.based_on

        loose = float(self.ui.doubleSpinBoxLoose.value())
        depth = float(self.ui.doubleSpinBoxDepth.value())

        subject = self.experiment.active_subject

        @threaded
        def inverse_operator(*args, **kwargs):
            create_inverse_operator(*args, **kwargs)

        try:
            inverse_operator(subject, name, based_on, loose, depth)
        except Exception as exc:
            exc_messagebox(self, exc)

        # call close handler
        if self.on_close:
            self.on_close()

        self.close()

