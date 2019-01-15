"""
"""
from PyQt5 import QtWidgets

import meggie.code_meggie.general.mne_wrapper as mne
import meggie.code_meggie.general.fileManager as fileManager

from meggie.ui.epoching.fixedLengthEpochDialogUi import Ui_FixedLengthEpochDialog

class FixedLengthEpochDialog(QtWidgets.QDialog):
    """
    Class containing the logic for FixedLengthEpochDialog. It is used for
    creating fixed length events.
    """

    def __init__(self, parent):
        """Initialize the event selection dialog.

        Keyword arguments:

        parent -- Set the parent of this dialog
        """
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_FixedLengthEpochDialog()
        self.ui.setupUi(self)
        self.parent = parent
        self.experiment = self.parent.parent.experiment
        self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Add events')
        self.raw = (self.experiment.active_subject
                    .get_working_file(temporary=True))
        tmax = int(self.raw.times[-1])
        self.ui.doubleSpinBoxStart.setMaximum(tmax)
        self.ui.doubleSpinBoxEnd.setMaximum(tmax)
        self.ui.doubleSpinBoxEnd.setValue(tmax)

    def accept(self, *args, **kwargs):
        event_params = {
            'tmin': self.ui.doubleSpinBoxStart.value(),
            'tmax': self.ui.doubleSpinBoxEnd.value(),
            'interval': self.ui.doubleSpinBoxInterval.value(),
        }
        subject = self.parent.get_selected_subject()
        working_file = subject.get_working_file(preload=False)
        
        events = mne.make_fixed_length_events(
            working_file, 0, event_params['tmin'],
            event_params['tmax'], event_params['interval']
        )
        if len(events) > 0:
            if event_params not in self.parent.event_data['fixed_length_events']:
                self.parent.event_data['fixed_length_events'].append(event_params)
                self.parent.update_events()
        return QtWidgets.QDialog.accept(self, *args, **kwargs)
