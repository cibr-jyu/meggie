#!/bin/bash

# Before, remember to:
# 1) Update setup.py
# 2) Update CHANGES.rst
# 3) Add a tag

if [[ -z "${INTERP}" ]]; then
  INTERP=python
fi

echo "Removing previous build artifacts"
rm -f dist/*

echo "Building source distribution.."
$INTERP setup.py sdist
echo "Building wheel.."
$INTERP setup.py bdist_wheel
echo "Uploading to pypi.."
$INTERP -m twine upload dist/*
echo "Finished."
