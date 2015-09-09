'''
Created on 26.2.2015

@author: Jaakko Leppakangas
'''

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignal

from powerSpectrumWidgetUi import Ui_PowerSpectrumWidget
from ui.general.channelSelectionDialogMain import ChannelSelectionDialog
from PyQt4.Qt import QPoint, QMenu


class PowerSpectrumWidget(QtGui.QWidget):
    removeWidget = pyqtSignal(int)
    channelCopy = pyqtSignal(int)

    def __init__(self, tmax, parent=None):
        super(PowerSpectrumWidget, self).__init__(parent)
        self.ui = Ui_PowerSpectrumWidget()
        self.ui.setupUi(self)
        self.installEventFilters()
        self._index = None
        self.ui.spinBoxTmin.setMaximum(tmax)
        self.ui.spinBoxTmax.setMaximum(tmax)
        self.ui.spinBoxTmin.setValue(5)
        self.ui.spinBoxTmax.setValue(tmax-5)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.ui.listWidgetChannels.customContextMenuRequested.connect
        (self.openMenu)

    @property
    def index(self):
        """Getter for index."""
        return self._index

    @index.setter
    def index(self, value):
        """Setter for index."""
        if value == 0:
            self.ui.pushButtonRemove.setVisible(False)
        self._index = value

    def setMaxTime(self, tmax):
        """Method for setting max time for spinboxes."""
        self.ui.spinBoxTmin.setMaximum(tmax)
        self.ui.spinBoxTmax.setMaximum(tmax)
        if self.ui.spinBoxTmin.value() > tmax:
            self.ui.spinBoxTmin.setValue(5)
        if self.ui.spinBoxTmax.value() > tmax:
            self.ui.spinBoxTmax.setValue(tmax-5)

    def getStartTime(self):
        """Method for getting the starting time of condition."""
        return self.ui.spinBoxTmin.value()

    def setStartTime(self, tmin):
        """Method for setting starting time."""
        self.ui.spinBoxTmin.setValue(tmin)

    def getEndTime(self):
        """Method for getting the ending time of condition."""
        return self.ui.spinBoxTmax.value()

    def setEndTime(self, tmax):
        """Setter for end time."""
        self.ui.spinBoxTmax.setValue(tmax)

    def getColor(self):
        """Method for getting the default color."""
        return str(self.ui.comboBoxColor.currentText())

    def setColor(self, color):
        """Setter for default color."""
        index = self.ui.comboBoxColor.findText(color)
        self.ui.comboBoxColor.setCurrentIndex(index)

    def getChannelColor(self):
        """Method for getting color for selected channels."""
        return str(self.ui.comboBoxChannelColor.currentText())

    def setChannelColor(self, color):
        """Setter for channel specific color."""
        index = self.ui.comboBoxChannelColor.findText(color)
        self.ui.comboBoxChannelColor.setCurrentIndex(index)

    def getChannels(self):
        """Method for getting the selected channels."""
        channels = []
        for i in xrange(self.ui.listWidgetChannels.count()):
            channels.append(str(self.ui.listWidgetChannels.item(i).text()))
        return channels

    def on_pushButtonRemove_clicked(self, checked=None):
        """
        Called when remove-button is clicked.
        Emits a signal for deleting this widget.
        """
        if checked is None:
            return
        self.removeWidget.emit(self.index)

    def on_pushButtonModify_clicked(self, checked=None):
        """
        Called when modify-button is clicked.
        Opens a dialog for modifying channels on the list.
        """
        if checked is None:
            return
        channels = []
        for i in xrange(self.ui.listWidgetChannels.count()):
            channels.append(self.ui.listWidgetChannels.item(i).text())
        channelDialog = ChannelSelectionDialog(channels)
        channelDialog.channelsChanged.connect(self.on_ChannelsChanged)
        channelDialog.exec_()

    def disableSpinBoxes(self, disable):
        """A method for setting read-only mode for the time spinboxes."""
        self.ui.spinBoxTmin.setReadOnly(disable)
        self.ui.spinBoxTmax.setReadOnly(disable)

    @QtCore.pyqtSlot(list)
    def on_ChannelsChanged(self, channels):
        """
        Called when channels are selected by hand.
        Parameters:
        channels - A list of selected channels
        """
        self.ui.listWidgetChannels.clear()
        if channels == []:
            self.ui.comboBoxChannelColor.setEnabled(False)
        else:
            self.ui.listWidgetChannels.addItems(channels)
            self.ui.comboBoxChannelColor.setEnabled(True)

    @QtCore.pyqtSlot(QPoint)
    def openMenu(self, position):
        """
        Method that handles actions from context menu.
        Parameters:
        position - Position of the action on screen (right click).
        """
        menu = QMenu()
        copyChannels = menu.addAction("Copy channels to all time series")
        clearChannels = menu.addAction("Clear")
        action = menu.exec_(self.ui.listWidgetChannels.mapToGlobal(position))
        if action == copyChannels:
            self.channelCopy.emit(self.index)
        elif action == clearChannels:
            self.ui.listWidgetChannels.clear()

    def installEventFilters(self):
        """Helper method for disabling wheel events on all widgets."""
        self.ui.spinBoxTmin.installEventFilter(self)
        self.ui.spinBoxTmax.installEventFilter(self)
        self.ui.comboBoxColor.installEventFilter(self)
        self.ui.comboBoxChannelColor.installEventFilter(self)

    def eventFilter(self, source, event):
        """Event filter for disabling wheel events on spin boxes and such."""
        if event.type() == QtCore.QEvent.Wheel:
            return True
        return QtGui.QWidget.eventFilter(self, source, event)
