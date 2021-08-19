#!/bin/bash

INTERP=/usr/bin/python

echo "Building source distribution.."
$INTERP -m build --sdist
echo "Building wheel.."
$INTERP -m build --wheel
echo "Uploading to pypi.."
$INTERP -m twine upload dist/*
echo "Finished."
