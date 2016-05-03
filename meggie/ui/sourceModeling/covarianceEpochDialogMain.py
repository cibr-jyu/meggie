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
    parameters computing the noise covariance for a raw file.
    """
    caller = Caller.Instance()

    def __init__(self, parent):
        QtGui.QDialog.__init__(self)
        self.parent = parent
        self.ui = Ui_covarianceEpochDialog()
        self.ui.setupUi(self)
        
        epochs = self.caller.experiment.active_subject.epochs

        for collection_name in epochs:
            self.ui.listWidgetEpochs.addItem(collection_name)
           
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
        
        if self.ui.doubleSpinBoxTmin.value == 0.00:
            params['tmin'] = None
        else:
            params['tmin'] = self.ui.doubleSpinBoxTmin.value
        
        if self.ui.doubleSpinBoxTmax.value == 0.00:
            params['tmax'] = None
        else:
            params['tmax'] = self.ui.doubleSpinBoxTmax.value
        
        projections = []
        
        for item in self.ui.listWidgetProjections.selectedItems():
            projections.append(str(item.text()))
        
        if len(projections) == 0:
            params['projs'] = None
        else:
            params['projs'] = projections
        
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
        
        #TODO: which projections to show if multiple epochs selected
        epoch = self.caller.experiment.active_subject.epochs.get(str(item.text()))
        raw = epoch.raw
        projs = raw.info['projs']

        for proj in projs:
            self.ui.listWidgetEpochs.addItem(str(proj))
        