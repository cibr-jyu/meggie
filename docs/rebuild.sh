#!/bin/bash

# remove existing sources
rm source/*meggie*.rst

# generate sources from docstrings
sphinx-apidoc -f -o source ../meggie \
                           ../meggie/tabs/* \
                           ../meggie/mainwindow/* \
                           ../meggie/mainWindow* \
                           ../meggie/utilities/widgets/*Ui.py \
                           ../meggie/utilities/dialogs/*Ui.py

# build the html
make html
