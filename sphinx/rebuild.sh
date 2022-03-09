#!/bin/bash

# remove existing sources
rm source/*meggie*.rst

# generate sources from docstrings
sphinx-apidoc -f -o source ../meggie \
                           ../meggie/actions/* \
                           ../meggie/mainwindow/* \
                           ../meggie/mainWindowUi.py \
                           ../meggie/utilities/widgets/*Ui.py \
                           ../meggie/utilities/dialogs/*Ui.py

# build the html
make html
