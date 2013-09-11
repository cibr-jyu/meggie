'''
Created on Sep 4, 2013

@author: atmiraut
'''
import sys

from PyQt4 import QtCore, QtGui

import mne

from evokedStatsDialogUi import Ui_EvokedStatsDialog
from statistic import Statistic

class EvokedStatsDialog(QtGui.QDialog):
    
    """A Window for displaying statistical information of averaged epochs.
    """
    
    def __init__(self, evoked=None):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_EvokedStatsDialog()
        self.ui.setupUi(self)
        self.evoked = evoked
        if evoked is None: return
        self.ui.doubleSpinBoxStart.setValue(evoked.times[0])
        self.ui.doubleSpinBoxStop.setValue(evoked.times[len(evoked.times)-1])
        for channel in evoked.ch_names:
            item = QtGui.QListWidgetItem(channel)
            self.ui.listWidgetChannels.addItem(item)
            
        self.selected_items = []
        
        self.ui.checkBoxLFrontal.stateChanged.connect(self.
                                                      checkBox_state_changed)
        self.ui.checkBoxLOcci.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxLParietal.stateChanged.connect(self.
                                                       checkBox_state_changed)
        self.ui.checkBoxLTemp.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxRFrontal.stateChanged.connect(self.
                                                      checkBox_state_changed)
        self.ui.checkBoxROcci.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxRParietal.stateChanged.connect(self.
                                                       checkBox_state_changed)
        self.ui.checkBoxRTemp.stateChanged.connect(self.
                                                   checkBox_state_changed)
        self.ui.checkBoxVertex.stateChanged.connect(self.
                                                    checkBox_state_changed)
        
        self.statUpdater = Statistic()
        
        #Multiselection: Do some cool average thing for the channels.
        #Save CSV: Create a CSV file of the key values displayed on the right side
        
    def checkBox_state_changed(self):
        """Select or unselect channels based on the checkbox.
        
        If the checkbox is unchecked, all related channels are unselected.
        If the checkbox is checked, all related channels are selected.
        
        Keyword arguments:
        
        state -- Integer stating whether the checkbox is checked or unchecked.
        """
        
        channels = mne.selection.read_selection(str(self.sender().text()))
        for channel in channels:
            for i in range(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                if str(item.text()) == channel:
                    item.setSelected(self.sender().isChecked())
                    break
        
    def on_pushButtonClearSelections_clicked(self):
        """Reset the values in the dialog's spinboxes.
        """
        self.ui.checkBoxLFrontal.setChecked(False)
        self.ui.checkBoxLOcci.setChecked(False)
        self.ui.checkBoxLParietal.setChecked(False)
        self.ui.checkBoxLTemp.setChecked(False)
        self.ui.checkBoxRFrontal.setChecked(False)
        self.ui.checkBoxROcci.setChecked(False)
        self.ui.checkBoxRParietal.setChecked(False)
        self.ui.checkBoxRTemp.setChecked(False)
        self.ui.checkBoxVertex.setChecked(False)
        self.ui.labelSelectedChannel.setText('No Channels selected.')
        self.resetSpinBoxes()
        
    def on_pushButtonSetSelected_clicked(self):
        """Update the information widgets based on selected channels.
        
        If only one channel is selected, it's information is shown. If multiple
        channels are selected, their averages are shown.
        """
        if len(self.ui.listWidgetChannels.selectedItems()) == 0: return
        self.ui.listWidgetChannels.setCurrentItem(self.ui.
                                                  listWidgetChannels.
                                                  selectedItems()[0])
        self.update_info()
        
    def resetSpinBoxes(self):
        """Reset the values in the dialog's spinboxes.
        """
        self.ui.doubleSpinBoxDuration.setValue(0)
        self.ui.doubleSpinBoxHalfMaxAfter.setValue(0)
        self.ui.doubleSpinBoxHalfMaxAmplitude.setValue(0)
        self.ui.doubleSpinBoxHalfMaxBefore.setValue(0)
        self.ui.doubleSpinBoxIntegral.setValue(0)
        self.ui.doubleSpinBoxMaxAmplitude.setValue(0)
        self.ui.doubleSpinBoxMaxTime.setValue(0)
        self.ui.doubleSpinBoxMinAmplitude.setValue(0)
        self.ui.doubleSpinBoxMinTime.setValue(0)
        
    def update_info(self):
        """Update the info widgets with data based on the selected items.
        """
        data = self.evoked.data
        ch_index = self.evoked.ch_names.index(self.ui.listWidgetChannels.\
                                              currentItem().text())
        #First collect all the necessary bits of information
        
        min, time_min_i = self.statUpdater.find_minimum(data[ch_index])
        max, time_max_i = self.statUpdater.find_maximum(data[ch_index])
        half_max, time_before_i, time_after_i = (self.statUpdater.
                                             find_half_maximum(data[ch_index]))
        
        #time_min_i, time_max_i, time_before_i and time_after_i are actually
        #index values fetch the actual times from evoked.times.
        time_min = self.evoked.times[time_min_i]
        time_max = self.evoked.times[time_max_i]
        time_before = self.evoked.times[time_before_i]
        time_after = self.evoked.times[time_after_i]
        
        duration = time_after - time_before
        integral = self.statUpdater.integrate(data[ch_index], time_before_i,
                                              time_after_i)
        
        #Amplitudes are displayed in microteslas
        #so scale the values accordingly.
        min = min * 1e12
        max = max * 1e12
        half_max = half_max * 1e12
        integral = integral * 1e12
        
        #Then update the appropriate fields in the dialog.
        self.ui.doubleSpinBoxDuration.setValue(duration)
        self.ui.doubleSpinBoxHalfMaxAfter.setValue(time_after)
        self.ui.doubleSpinBoxHalfMaxAmplitude.setValue(half_max)
        self.ui.doubleSpinBoxHalfMaxBefore.setValue(time_before)
        self.ui.doubleSpinBoxIntegral.setValue(integral)
        self.ui.doubleSpinBoxMaxAmplitude.setValue(max)
        self.ui.doubleSpinBoxMaxTime.setValue(time_max)
        self.ui.doubleSpinBoxMinAmplitude.setValue(min)
        self.ui.doubleSpinBoxMinTime.setValue(time_min)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    
    epochs = mne.read_epochs('/space/atmiraut/meggieWorkspace/Boris/jn/epochs/Epochs.fif')
    evoked = epochs.average()
    
    window = EvokedStatsDialog(evoked)
    
    window.show()
    
    sys.exit(app.exec_())