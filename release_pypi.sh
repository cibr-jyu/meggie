#!/bin/bash

INTERP=python

# Note: remember to run in a environment where there's not PyQt5 installed.

echo "Removing previous build artifacts"
rm -f dist/*

echo "Building source distribution.."
$INTERP setup.py sdist
echo "Building wheel.."
$INTERP setup.py bdist_wheel
echo "Uploading to pypi.."
$INTERP -m twine upload dist/*
echo "Finished."
