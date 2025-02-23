"""Contains a class for logic of action dialog."""

from PyQt5 import QtWidgets
import os
import json
import re
import logging
from pprint import pformat

from meggie.mainwindow.dynamic import find_all_action_specs
from meggie.utilities.messaging import exc_messagebox
from meggie.utilities.messaging import messagebox
from meggie.utilities.filemanager import homepath

from meggie.mainwindow.dialogs.actionDialogUi import Ui_ActionDialog


class ActionDialog(QtWidgets.QDialog):
    """Contains logic for action dialog."""

    def __init__(self, parent, experiment):
        QtWidgets.QDialog.__init__(self, parent)
        self.parent = parent
        self.experiment = experiment
        self.ui = Ui_ActionDialog()
        self.ui.setupUi(self)

        # clear the tree widget
        self.ui.treeWidgetActions.clear()

        try:
            # parse the actions log as a dict
            actions_dict = self._parse_log_as_dict()

            # transform to new dict that includes subject information
            self.data = self._transform_to_subjects(actions_dict)

            # populate the tree widget
            self._populate_tree_widget(self.data)
        except Exception as exc:
            exc_messagebox(self, exc)
            return

    def _parse_log_as_dict(self):
        """Parse actions log file into a dictionary."""
        experiment = self.experiment
        path = os.path.join(experiment.path, "actions.log")
        with open(path, "r") as f:
            lines = f.readlines()

        actions = {}

        for line in lines:
            content = json.loads(line)
            uid = content["uid"]

            if uid not in actions:
                actions[uid] = []

            actions[uid].append(content)

        subject_tree = {}

        for action_uid, action_rows in actions.items():
            action_tree = {}
            id_ = desc = version = data = None
            for row in action_rows:
                if row["type"] == "ACTION_START":
                    id_ = row["id"]
                    desc = row.get("desc")
                    version = row.get("version")
                    data = row.get("data")

                elif row["type"] == "SUBJECT_START":
                    subject_uid = row["subject_uid"]
                    if subject_uid not in action_tree:
                        action_tree[subject_uid] = {}
                    action_tree[subject_uid]["params"] = row["params"]

                elif row["type"] == "SUBJECT_END":
                    subject_uid = row["subject_uid"]
                    if subject_uid not in action_tree:
                        action_tree[subject_uid] = {}
                    action_tree[subject_uid]["finished"] = True
                    action_tree[subject_uid]["timestamp"] = row["timestamp"]

            for subject_uid, branch in action_tree.items():
                if branch.get("finished"):
                    branch["id"] = id_
                    branch["desc"] = desc
                    branch["data"] = data
                    branch["version"] = version
                    if subject_uid not in subject_tree:
                        subject_tree[subject_uid] = []
                    subject_tree[subject_uid].append(branch)

        return subject_tree

    def _transform_to_subjects(self, actions_data):
        """Inject subject data into the dict."""
        experiment = self.experiment

        subject_data = {}
        for subject_name, subject in experiment.subjects.items():
            if subject.uid in actions_data:
                subject_data[subject_name] = actions_data[subject.uid]

        return subject_data

    def _populate_tree_widget(self, data):
        """Populate the tree widget using the internal data representation."""

        action_specs = find_all_action_specs()

        for subject_name, subject_actions in sorted(data.items()):

            subject_item = QtWidgets.QTreeWidgetItem(self.ui.treeWidgetActions)
            subject_item.setText(0, subject_name)

            for action_data in subject_actions:
                action_item = QtWidgets.QTreeWidgetItem(subject_item)

                action_name = action_data["id"]
                if action_data["id"] in action_specs:
                    name_specs = action_specs[action_data["id"]][2]
                    action_name = name_specs.get("name", action_name)

                if action_data["desc"]:
                    action_name += f" ({action_data['desc']})"

                action_item.setText(0, action_name)

                params = action_data.get("params") or {}
                if params:
                    params_item = QtWidgets.QTreeWidgetItem(action_item)
                    params_item.setText(0, "Params")
                    for param_name, param_value in params.items():
                        msg = f"{param_name}: {json.dumps(param_value)}"
                        param_item = QtWidgets.QTreeWidgetItem(params_item)
                        param_item.setText(0, msg)

                data = action_data.get("data") or {}
                if data:
                    data_item = QtWidgets.QTreeWidgetItem(action_item)
                    data_item.setText(0, "Data")
                    for data_name, data_value in data.items():
                        msg = f"{data_name}: {json.dumps(data_value)}"
                        data_row_item = QtWidgets.QTreeWidgetItem(data_item)
                        data_row_item.setText(0, msg)

                timestamp_re = re.compile(
                    r"([0-9]*-[0-9]*-[0-9]*)T([0-9]*:[0-9]*:[0-9]*)\..*"
                )
                elems = timestamp_re.match(action_data["timestamp"])
                if elems:
                    msg = f"Timestamp: {elems[1]} {elems[2]} UTC"
                    timestamp_item = QtWidgets.QTreeWidgetItem(action_item)
                    timestamp_item.setText(0, msg)

    def on_treeWidgetActions_itemDoubleClicked(self, item):
        if item.childCount() == 0:
            # try creating a pretty formatted details dialog
            try:
                match = re.compile("([a-zA-Z0-9_]*): (.*)").match(item.text(0))
                if match:
                    val = match.group(2)
                    try:
                        obj = json.loads(val)
                    except Exception:
                        obj = val
                    messagebox(self, pformat(obj))
            except Exception:
                logging.getLogger("ui_logger").exception("")

    def on_pushButtonExport_clicked(self, checked=None):
        if checked is None:
            return

        default_filename = (
            f"{self.experiment.name.lower().replace(' ', '_')}_actions.json"
        )
        filepath, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export Action Log",
            os.path.join(homepath(), default_filename),
            "JSON Files (*.json);;All Files (*)",
        )

        if filepath:
            try:
                with open(filepath, "w") as file:
                    json.dump(self.data, file, indent=4)
                logging.getLogger("ui_logger").info(
                    "Exported action log successfully to " + filepath
                )
            except Exception as exc:
                exc_messagebox(self, f"Failed to export: {exc}")

        self.close()
