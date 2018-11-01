"""
"""

from PyQt5 import QtWidgets

from meggie.ui.source_analysis.forwardSolutionDialogUi import Ui_forwardSolutionDialog  # noqa

from meggie.code_meggie.general.source_analysis import create_forward_solution

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox
from meggie.ui.utils.decorators import threaded

class ForwardSolutionDialog(QtWidgets.QDialog):
    """
    """

    def __init__(self, parent, experiment=None, on_close=None):
        QtWidgets.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_forwardSolutionDialog()
        self.ui.setupUi(self)
        self.on_close = on_close
        self.experiment = experiment

    def accept(self):
        """
        """

        # collect parameters
        name = str(self.ui.lineEditForwardSolutionName.text())
        decim = str(self.ui.comboBoxSurfaceDecimMethod.currentText())
        triang_ico = int(self.ui.spinBoxTriangFilesIco.value())

        include_eeg = self.ui.checkBoxIncludeEEG.isChecked()
        include_meg = self.ui.checkBoxIncludeMEG.isChecked()

        if not include_eeg and not include_meg:
            messagebox(self, "You must include either EEG or MEG channels.", exec_=True)
            return

        inner_skull = float(self.ui.doubleSpinBoxBrainConductivity.value())
        outer_skull = float(self.ui.doubleSpinBoxSkullConductivity.value())
        outer_skin = float(self.ui.doubleSpinBoxScalpConductivity.value())

        # if single layer
        if self.ui.comboBoxCompartmentModel.currentIndex() == 0:
            conductivity = (inner_skull,)

        # three layers
        else:
            conductivity = (
                inner_skull,
                outer_skull,
                outer_skin
            )

        subject = self.experiment.active_subject

        @threaded
        def fwd_solution(*args, **kwargs):
            create_forward_solution(*args, **kwargs)

        try:
            update_ui = self.parent.parent.update_ui
            fwd_solution(subject, name, decim, triang_ico, conductivity, 
                         include_eeg, include_meg, do_meanwhile=update_ui)
        except Exception as exc:
            exc_messagebox(self, exc)

        # call close handler
        if self.on_close:
            self.on_close()

        self.close()

