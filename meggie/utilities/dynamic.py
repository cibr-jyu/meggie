# coding: utf-8

import importlib
import logging

from PyQt5 import QtWidgets

from meggie.utilities.messaging import exc_messagebox

"""
"""
def construct_tab(tab_spec, parent):

    class DynamicTab(QtWidgets.QDialog):
        def __init__(self, parent):
            QtWidgets.QDialog.__init__(self)
            self.parent = parent
            self.tab_spec = tab_spec

            # first create basic layout

            self.gridLayoutContainer = QtWidgets.QGridLayout(self)

            self.gridLayoutRoot = QtWidgets.QGridLayout()
            self.gridLayoutContainer.addLayout(self.gridLayoutRoot, 0, 0, 1, 1)

            if tab_spec.get('outputs'):
                self.groupBoxOutputs = QtWidgets.QGroupBox(self)
                self.groupBoxOutputs.setTitle('Outputs')
                self.gridLayoutOutputs = QtWidgets.QGridLayout(self.groupBoxOutputs)

            if tab_spec.get('actions'):
                self.groupBoxActions = QtWidgets.QGroupBox(self)
                self.groupBoxActions.setTitle('Actions')
                self.gridLayoutActions = QtWidgets.QGridLayout(self.groupBoxActions)

            if tab_spec.get('transforms'):
                self.groupBoxTransforms = QtWidgets.QGroupBox(self)
                self.groupBoxTransforms.setTitle('Transforms')
                self.gridLayoutTransforms = QtWidgets.QGridLayout(self.groupBoxTransforms)
                
            if tab_spec.get('inputs'):
                self.groupBoxInputs = QtWidgets.QGroupBox(self)
                self.groupBoxInputs.setTitle('Inputs')
                self.gridLayoutInputs = QtWidgets.QGridLayout(self.groupBoxInputs)


            # then fill the contents

            for idx, input_element in enumerate(tab_spec.get('inputs', [])):
                groupBoxInputElement = QtWidgets.QGroupBox(self.groupBoxInputs)
                groupBoxInputElement.setTitle(input_element.capitalize())
                gridLayoutInputElement = QtWidgets.QGridLayout(groupBoxInputElement)
                listWidgetInputElement = QtWidgets.QListWidget(groupBoxInputElement)

                gridLayoutInputElement.addWidget(listWidgetInputElement, idx, 0, 1, 1)
                self.gridLayoutInputs.addWidget(groupBoxInputElement)

                setattr(self, 'groupBoxInputElement_' + str(idx+1), 
                        groupBoxInputElement)
                setattr(self, 'gridLayoutInputElement_' + str(idx+1), 
                        gridLayoutInputElement)
                setattr(self, 'listWidgetInputElement_' + str(idx+1), 
                        listWidgetInputElement)

            for idx, output_element in enumerate(tab_spec.get('outputs', [])):
                groupBoxOutputElement = QtWidgets.QGroupBox(self.groupBoxOutputs)
                groupBoxOutputElement.setTitle(output_element.capitalize())
                gridLayoutOutputElement = QtWidgets.QGridLayout(groupBoxOutputElement)
                listWidgetOutputElement = QtWidgets.QListWidget(groupBoxOutputElement)

                gridLayoutOutputElement.addWidget(listWidgetOutputElement, idx, 0, 1, 1)
                self.gridLayoutOutputs.addWidget(groupBoxOutputElement)

                setattr(self, 'groupBoxOutputElement_' + str(idx+1), 
                        groupBoxOutputElement)
                setattr(self, 'gridLayoutOutputElement_' + str(idx+1), 
                        gridLayoutOutputElement)
                setattr(self, 'listWidgetOutputElement_' + str(idx+1), 
                        listWidgetOutputElement)

            # connect to handler
            def connect_to_handler(button, element, data_type):
                module_name = tab_spec['id']
                try:
                    module = importlib.import_module(
                        '.'.join(['meggie', 'tabs', module_name, 'ui']))
                    handler = getattr(module, element)

                    def handler_wrapper(checked):
                        experiment = self.parent.experiment
                        if not experiment:
                            return


                        subject = experiment.active_subject
                        if not subject:
                            return

                        data = []
                        for idx, name in enumerate(self.tab_spec.get(data_type, [])):
                            if data_type == 'inputs':
                                ui_element = getattr(self, 'listWidgetInputElement_' + str(idx+1))
                            elif data_type == 'outputs':
                                ui_element = getattr(self, 'listWidgetOutputElement_' + str(idx+1))

                            try:
                                selected_items = [item.text() for item in 
                                                  ui_element.selectedItems()]
                            except:
                                continue

                            data.append((name, selected_items))

                        try:
                            handler(experiment, data, parent)
                        except Exception as e:
                            exc_messagebox(self, e)
                        
                    if handler:
                        button.clicked.connect(handler_wrapper)
                except ModuleNotFoundError:
                    pass
                except AttributeError:
                    pass

            for idx, transform_element in enumerate(tab_spec.get('transforms', [])):
                pushButtonTransformElement = QtWidgets.QPushButton(self.groupBoxTransforms)
                pushButtonTransformElement.setText(transform_element.capitalize())
                self.gridLayoutTransforms.addWidget(pushButtonTransformElement, idx, 0, 1, 1)
                setattr(self, 'pushButtonTransformElement_' + str(idx+1), 
                        pushButtonTransformElement)

                connect_to_handler(pushButtonTransformElement, transform_element, 'inputs')

            for idx, action_element in enumerate(tab_spec.get('actions', [])):
                pushButtonActionElement = QtWidgets.QPushButton(self.groupBoxActions)
                pushButtonActionElement.setText(action_element.capitalize())
                self.gridLayoutActions.addWidget(pushButtonActionElement, idx, 0, 1, 1)
                setattr(self, 'pushButtonActionElement_' + str(idx+1), 
                        pushButtonActionElement)

                connect_to_handler(pushButtonActionElement, action_element, 'outputs')

            if tab_spec.get('inputs') and not tab_spec.get('transforms'):
                self.gridLayoutRoot.addWidget(self.groupBoxInputs, 0, 0, 2, 1)
            elif tab_spec.get('inputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxInputs, 0, 0, 1, 1)

            if tab_spec.get('outputs') and not tab_spec.get('actions'):
                self.gridLayoutRoot.addWidget(self.groupBoxOutputs, 0, 1, 2, 1)
            elif tab_spec.get('outputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxOutputs, 0, 1, 1, 1)

            if tab_spec.get('transforms') and not tab_spec.get('inputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxTransforms, 0, 0, 2, 1)
            elif tab_spec.get('transforms'):
                self.gridLayoutRoot.addWidget(self.groupBoxTransforms, 1, 0, 1, 1)

            if tab_spec.get('actions') and not tab_spec.get('outputs'):
                self.gridLayoutRoot.addWidget(self.groupBoxActions, 0, 1, 2, 1)
            elif tab_spec.get('actions'):
                self.gridLayoutRoot.addWidget(self.groupBoxActions, 1, 1, 1, 1)

            spacerItemVertical = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            self.gridLayoutContainer.addItem(spacerItemVertical, 1, 0, 1, 1)
            spacerItemHorizontal = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            self.gridLayoutContainer.addItem(spacerItemHorizontal, 0, 1, 1, 1)


        def initialize_ui(self):

            experiment = self.parent.experiment
            if not experiment:
                return

            subject = experiment.active_subject
            if not subject:
                return

            for idx, input_name in enumerate(self.tab_spec.get('inputs', [])):
                ui_element = getattr(self, 'listWidgetInputElement_' + str(idx+1))

                data = getattr(subject, input_name, None)
                if not data:
                    logging.getLogger('ui_logger').info(
                        "Data not found for " + str(input_name) + 
                        " in " + self.name + " tab.")
                    continue

                for key in sorted(list(data.keys())):
                    ui_element.addItem(key)

            for idx, output_name in enumerate(self.tab_spec.get('outputs', [])):
                ui_element = getattr(self, 'listWidgetOutputElement_' + str(idx+1))

                data = getattr(subject, output_name, None)
                if not data:
                    logging.getLogger('ui_logger').info(
                        "Data not found for " + str(output_name) + 
                        " in " + self.name + " tab.")
                    continue

                for key in sorted(list(data.keys())):
                    ui_element.addItem(key)

        @property
        def name(self):
            return self.tab_spec['name']

    DynamicTab.__name__ = 'MainWindowTab' + tab_spec['id'].capitalize()

    tab = DynamicTab(parent)

    return tab
