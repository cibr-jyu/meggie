""" Contains a class for logic of the single channel plot dialog.
"""
import logging

from PyQt5 import QtWidgets

from meggie.utilities.dialogs.singleChannelDialogUi import Ui_singleChannelDialog


class SingleChannelDialog(QtWidgets.QDialog):
    """ Contains logic for the single channel plot dialog.
    """
    def __init__(self, parent, handler, title, ch_names,
                 scalings, units, ylims, default_legend_names):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_singleChannelDialog()
        self.ui.setupUi(self)
        self.handler = handler
        self.scalings = scalings
        self.units = units
        self.ylims = ylims
        self.default_legend_names = default_legend_names

        # populate channel combobox
        for ch_name in sorted(ch_names):
            self.ui.comboBoxChannel.addItem(ch_name)

        # populate title
        self.ui.lineEditTitle.setText(title)

        # populate legend settings
        for legend_idx, legend_name in enumerate(default_legend_names):

            label_item = QtWidgets.QLabel(self.ui.groupBoxLegend)
            label_item.setText(legend_name)
            self.ui.formLayoutLegend.setWidget(legend_idx,
                QtWidgets.QFormLayout.LabelRole, label_item)

            line_edit_item = QtWidgets.QLineEdit(self.ui.groupBoxLegend)
            setattr(self.ui, 'lineEditItem_' + str(legend_idx),
                line_edit_item)
            line_edit_item.setText(legend_name)
            self.ui.formLayoutLegend.setWidget(legend_idx,
                QtWidgets.QFormLayout.FieldRole, line_edit_item)

    def on_comboBoxChannel_currentTextChanged(self, item):
        self.ui.doubleSpinBoxMin.setSuffix(' ' + self.units[item])
        self.ui.doubleSpinBoxMax.setSuffix(' ' + self.units[item])

        self.ui.doubleSpinBoxMin.setValue(self.ylims[item][0] *
                                          self.scalings[item] * 1.05)
        self.ui.doubleSpinBoxMax.setValue(self.ylims[item][1] *
                                          self.scalings[item] * 1.05)


    def accept(self):
        ymax = self.ui.doubleSpinBoxMax.value()
        ymin = self.ui.doubleSpinBoxMin.value()
        ylim = (ymin, ymax)

        ch_name = self.ui.comboBoxChannel.currentText()
        window_len = self.ui.spinBoxWindowLength.value()
        window = self.ui.comboBoxWindow.currentText()

        title = self.ui.lineEditTitle.text()

        legend = {}
        for idx in range(len(self.default_legend_names)):
            line_edit = getattr(self.ui, 'lineEditItem_' + str(idx))
            legend[self.default_legend_names[idx]] = line_edit.text()

        self.handler(ch_name, title, legend, ylim, window, window_len)

        self.close()
