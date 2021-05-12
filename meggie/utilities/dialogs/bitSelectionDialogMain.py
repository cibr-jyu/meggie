""" Contains a class for logic of the bit selection dialog.
"""
from PyQt5 import QtWidgets
from PyQt5.Qt import QPushButton, pyqtSlot

from meggie.utilities.dialogs.bitSelectionDialogUi import Ui_Dialog


class BitSelectionDialog(QtWidgets.QDialog):
    """ Contains the logic for bit selection dialog.
    """

    def __init__(self, parent, target_mask, target_id):
        QtWidgets.QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.intervals = []
        self.button_count = 16

        self.parent = parent
        self.target_mask = target_mask
        self.target_id = target_id

        self.ui.labelID.setText('0')
        # 2^0 + 2^1 + ... + 2^(button_count - 1)
        self.ui.labelMask.setText(str(pow(2, self.button_count) - 1))

        for i in range(1, self.button_count + 1):
            getattr(self.ui, "pushButton" + str(i)).setText(" ")
            (lambda x: getattr(self.ui, "pushButton" + str(x)).clicked.connect(
                lambda: self._bit_clicked(getattr(self.ui,
                                                 "pushButton" + str(x)))))(i)

    @pyqtSlot(QPushButton)
    def _bit_clicked(self, button):
        id_operation, mask_operation = None, None

        if button.text() == ' ':
            button.setText('0')
            mask_operation = '-'
        elif button.text() == '0':
            button.setText('1')
            id_operation = '+'
        elif button.text() == '1':
            button.setText(' ')
            mask_operation = '+'
            id_operation = '-'

        current_id = int(self.ui.labelID.text())
        current_mask = int(self.ui.labelMask.text())
        current_button_number = int(button.objectName()[len("pushButton"):])

        new_id, new_mask = current_id, current_mask

        if id_operation == '+':
            new_id = current_id + pow(2, current_button_number - 1)
        elif id_operation == '-':
            new_id = current_id - pow(2, current_button_number - 1)

        if mask_operation == '+':
            new_mask = current_mask + pow(2, current_button_number - 1)
        elif mask_operation == '-':
            new_mask = current_mask - pow(2, current_button_number - 1)

        self.ui.labelID.setText(str(new_id))
        self.ui.labelMask.setText(str(new_mask))

    def accept(self):
        self.target_id.setValue(int(self.ui.labelID.text()))
        self.target_mask.setValue(int(self.ui.labelMask.text()))
        self.close()
