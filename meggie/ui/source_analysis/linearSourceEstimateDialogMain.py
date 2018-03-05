"""
@author: Erkka Heinila
"""

from PyQt4 import QtGui

from meggie.ui.source_analysis.linearSourceEstimateDialogUi import Ui_linearSourceEstimateDialog  # noqa

from meggie.code_meggie.general.source_analysis import create_linear_source_estimate  # noqa

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.decorators import threaded

class LinearSourceEstimateDialog(QtGui.QDialog):
    """
    """

    def __init__(self, parent, fwd_name, inst_type, inst_name, experiment=None, on_close=None):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_linearSourceEstimateDialog()
        self.ui.setupUi(self)
        self.on_close = on_close
        self.experiment = experiment
        self.fwd_name = fwd_name
        self.inst_type = inst_type
        self.inst_name = inst_name

        self.ui.lineEditBasedOn.setText(fwd_name)

    def accept(self):
        """
        """

        # collect parameters
        name = str(self.ui.lineEditSourceEstimateName.text())
        if not name:
            messagebox(self, "Please give a name for the source estimate")
            return

        based_on = self.based_on

        loose = float(self.ui.doubleSpinBoxLoose.value())
        depth = float(self.ui.doubleSpinBoxDepth.value())

        subject = self.experiment.active_subject

        @threaded
        def linear_stc(*args, **kwargs):
            create_linear_source_estimate(*args, **kwargs)

        try:
            linear_stc(subject, name, based_on, loose, depth)
        except Exception as exc:
            exc_messagebox(self, exc)

        # call close handler
        if self.on_close:
            self.on_close()

        self.close()

