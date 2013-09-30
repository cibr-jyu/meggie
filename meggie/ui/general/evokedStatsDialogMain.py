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
        """Constructor.
        
        Keyword arguments:
        
        evoked = a dictionary containing evoked-objects.
        """
        QtGui.QDialog.__init__(self)
        self.ui = Ui_EvokedStatsDialog()
        self.ui.setupUi(self)
        self.evoked = evoked
        if evoked is None: return
            
        #Selected_items is a dictionary containing all the channels selected
        #across the evoked sets in the comboBoxEvokeds. 
        self.selected_channels = {}
        for key in self.evoked.keys():
            self.selected_channels[key] = []
        
        self.populateComboBoxEvoked()
        
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
        
        self.ui.comboBoxEvoked.currentIndexChanged.connect(self.
                                                           evoked_set_changed)
        self.ui.pushButtonSetSelected.setEnabled(False)
        
        self.evoked_set_changed()
        
        self.ui.listWidgetChannels.itemSelectionChanged.\
        connect(self.selection_changed)
        
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
                
    def evoked_set_changed(self):
        """Updates the channel list with current evoked's channels.
        """
        
        channels = self.evoked[str(self.ui.comboBoxEvoked.
                                   currentText())][0].info['ch_names']
        
        #First clear the channel list.
        for i in range(self.ui.listWidgetChannels.count()):
            self.ui.listWidgetChannels.takeItem(0)
        
        #Then add the new channels to the list.
        #Note: This could actually be useless. The channel names seem to be
        #the same across the data sets. Don't know if this is actually
        #the case though.                           
        for channel in channels:
            item = QtGui.QListWidgetItem(channel)
            self.ui.listWidgetChannels.addItem(item)
            self.ui.listWidgetChannels.sortItems()
            
        #Finally check if there are any channels that need to be set as
        #selected in the new channel list.
        for channel in self.selected_channels[str(self.ui.comboBoxEvoked.
                                                  currentText())]:
            for i in range(self.ui.listWidgetChannels.count()):
                item = self.ui.listWidgetChannels.item(i)
                if str(item.text()) == channel:
                    item.setSelected(True)
                    break
                
        self.ui.pushButtonSetSelected.setEnabled(False)
        
    def on_pushButtonClearSelections_clicked(self):
        """Reset the values in the dialog's spinboxes.
        """
        self.reset_data_values()
        self.ui.pushButtonSetSelected.setEnabled(False)
        
    def on_pushButtonSetSelected_clicked(self):
        """Save selected channels to selected_channels dictionary.
        """
        if len(self.ui.listWidgetChannels.selectedItems()) == 0: return
        for item in self.ui.listWidgetChannels.selectedItems():
            if item not in self.selected_channels[str(self.ui.comboBoxEvoked.
                                                      currentText())]:
                self.selected_channels[str(self.ui.comboBoxEvoked.
                                       currentText())].append(str(item.text()))
                                       
        self.ui.pushButtonSetSelected.setEnabled(False)
        
        #TODO: Update the info widgets. If item_selection has multiple
        #channels, they should be averaged and the result of that should be
        #shown on the info widgets.   
        
    def populateComboBoxEvoked(self):
        """Populate the combo box above the channel list with evoked set names.
        """
        for key in self.evoked.keys():
            self.ui.comboBoxEvoked.addItem(key)
        
    def reset_data_values(self):
        """Reset all the spinboxes and labels displaying data.
        
        Keyword arguments:
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
        
        for key in self.selected_channels.keys():
            self.selected_channels[key] = []
    
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
        
    def selection_changed(self):
        """Enable pushButtonSetSelected.
        """
        if len(self.ui.listWidgetChannels.selectedItems()) > 0:
            self.ui.pushButtonSetSelected.setEnabled(True)
            
        else: self.ui.pushButtonSetSelected.setEnabled(False)
        
    def update_info(self, name):
        """Update the info widgets with data based on item.
        
        Keyword arguments:
        
        name -- Name of the channel whose data is to be displayed.
        """
        data = self.evoked[0].data
        ch_index = self.evoked[0].ch_names.index(name)
        #First collect all the necessary bits of information
        
        min, time_min_i = self.statUpdater.find_minimum(data[ch_index])
        max, time_max_i = self.statUpdater.find_maximum(data[ch_index])
        half_max, time_before_i, time_after_i = (self.statUpdater.
                                             find_half_maximum(data[ch_index]))
        
        #time_min_i, time_max_i, time_before_i and time_after_i are actually
        #index values fetch the actual times from evoked.times.
        time_min = self.evoked[0].times[time_min_i]
        time_max = self.evoked[0].times[time_max_i]
        time_before = self.evoked[0].times[time_before_i]
        time_after = self.evoked[0].times[time_after_i]
        
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
        self.ui.labelSelectedChannel.setText(name)
        self.ui.doubleSpinBoxDuration.setValue(duration)
        self.ui.doubleSpinBoxHalfMaxAfter.setValue(time_after)
        self.ui.doubleSpinBoxHalfMaxAmplitude.setValue(half_max)
        self.ui.doubleSpinBoxHalfMaxBefore.setValue(time_before)
        self.ui.doubleSpinBoxIntegral.setValue(integral)
        self.ui.doubleSpinBoxMaxAmplitude.setValue(max)
        self.ui.doubleSpinBoxMaxTime.setValue(time_max)
        self.ui.doubleSpinBoxMinAmplitude.setValue(min)
        self.ui.doubleSpinBoxMinTime.setValue(time_min)