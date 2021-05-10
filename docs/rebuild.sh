#!/bin/bash

# remove existing sources
rm source/*meggie*.rst

# generate sources from docstrings
sphinx-apidoc -f -o source ../meggie

# build the html
make html
