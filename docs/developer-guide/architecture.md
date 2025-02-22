# Architecture Overview

This document outlines the core structure of Meggie, offering insights into its construction and how developers can leverage its architecture.

## Main Classes

Meggie is structured around three fundamental classes:

### MainWindow

MainWindow is the central hub of the user interface, built using PyQt. Key components include:

- Left Panel: Displays experiment-specific details.
- Bottom Console: Logs user actions and system messages.
- Right Panel: Hosts tabs for data transformation actions.

### Experiment

The Experiment class serves as the top-level container for all data, handling the saving and loading of experiments, and maintaining a collection of subjects.

### Subject

Subject instances are nested within experiments and are tasked with managing subject-specific data. Their primary roles are to handle the saving and loading of raw data and to hold instances of various datatypes.

## Actions, Pipelines, and Datatypes

Meggie's analytical capabilities are structured into actions, pipelines, and datatypes.

### Datatypes

Datatypes are templates for summarizing raw data into meaningful structures for analysis, such as epochs, evokeds, spectrums, and TFRs. These templates are defined within the datatypes folder and instantiated as needed to store within subjects.

### Actions

Actions represent fundamental analysis steps, like "filter" or "create epochs." Each action, located in its respective folder within the actions directory, comprises metadata in configuration.json and Python code. Actions inherit from the Action class in mainwindow/dynamic.py and can be integrated into pipelines and are automatically logged.

### Pipelines

Pipelines organize actions into a sequence represented as buttons within the GUI tabs. They guide the user through a complete analysis workflow, such as "Sensor-level continuous data analysis." Pipelines are specified in the main configuration.json and rely on actions for implementation, thus containing no Python code themselves.

## Plugins

Creating plugins for Meggie is designed to be straightforward. The system dynamically locates pipelines, datatypes, and actions at runtime, allowing them to be loaded from external Python packages within the Meggie namespace. To create a plugin, one simply needs to develop a Python package named within the Meggie namespace that introduces new pipelines, actions, and/or datatypes.

## API

The core of Meggie, excluding the actions, is intended to be stable and reusable. Plugin developers are encouraged to utilize the API provided by the MainWindow, Subject, and Experiment classes. Additionally, developers have access to the four datatypes in the datatypes folder and various utilities, including functions, dialogs, and widgets, found in the utilities folder.
