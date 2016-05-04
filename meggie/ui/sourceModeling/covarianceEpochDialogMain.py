'''
Created on 3.5.2016

@author: jaolpeso
'''
from PyQt4 import QtGui

from meggie.ui.sourceModeling.covarianceEpochDialogUi import Ui_covarianceEpochDialog

from meggie.code_meggie.general.caller import Caller

from meggie.ui.utils.messaging import exc_messagebox
from meggie.ui.utils.messaging import messagebox

class CovarianceEpochDialog(QtGui.QDialog):
    """
    The class containing the logic for the dialog for collecting the
    parameters computing the noise covariance for epoch collection/s.
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_covarianceEpochDialog()
        self.ui.setupUi(self)
        
        epochs = self.caller.experiment.active_subject.epochs
        name = ''
        item = None
        
        for collection_name in epochs.keys():
            item = QtGui.QListWidgetItem(collection_name)
            self.ui.listWidgetEpochs.addItem(item)
            name = collection_name
            
        self.ui.listWidgetEpochs.setItemSelected(item, True)
        epoch = self.caller.experiment.active_subject.epochs.get(name)
        self.populate_doublespinboxes(epoch)
        
        methods = {
            'empirical': '',
            'diagonal_fixed': '',
            'ledoit_wolf': '',
            'shrunk': '',
            'pca': '',
            'factor_analysis': ''
        }
        
        self.ui.comboBoxMethod.addItems(methods.keys())
        self.ui.comboBoxMethod.setCurrentIndex(methods.keys().index('empirical'))
        
    def accept(self):
        """
        Gets the arguments from the gui and passes them to caller for computing
        the noise covariance matrix.
        """
        params = dict()
        collections = []
        
        if len(self.ui.listWidgetEpochs.selectedItems()) == 0:
            message = ('Select epochs before computation.')
            messagebox(self.parent, message)
            return
        
        for item in self.ui.listWidgetEpochs.selectedItems():
            collections.append(str(item.text()))
        
        params['collection_names'] = collections
        
        if self.ui.checkBoxKeepSampleMean.isChecked():
            params['keep_sample_mean'] = True
        else:
            params['keep_sample_mean'] = False
            
        method = self.ui.comboBoxMethod.currentText()
        
        if method is not 'empirical':
            #only empirical supports False
            params['keep_sample_mean'] = True
        
        #if None, starts at first sample
        params['tmin'] = self.ui.doubleSpinBoxTmin.value()
        #if None, ends at last sample
        params['tmax'] = self.ui.doubleSpinBoxTmax.value()
        params['method'] = method
        
        try:
            #TODO: caller.create_covariance_from_epoch
            self.caller.create_covariance_from_epoch(params)    
        except ValueError as e:
            exc_messagebox(self.parent, e)
            return   
        except IOError as e:
            exc_messagebox(self.parent, e)
            return
        
        self.close()

    def on_listWidgetEpochs_currentItemChanged(self, item):
        
        if not item:
            return

        epoch = self.caller.experiment.active_subject.epochs.get(str(item.text()))
        self.populate_doublespinboxes(epoch)

    def populate_doublespinboxes(self, epoch):
        self.ui.doubleSpinBoxTmin.setMinimum(epoch.params['tmin'])
        self.ui.doubleSpinBoxTmin.setMaximum(epoch.params['tmax'])
        self.ui.doubleSpinBoxTmax.setMinimum(epoch.params['tmin'])
        self.ui.doubleSpinBoxTmax.setMaximum(epoch.params['tmax'])
        self.ui.doubleSpinBoxTmin.setValue(epoch.params['tmin'])
        self.ui.doubleSpinBoxTmax.setValue(epoch.params['tmax'])
        