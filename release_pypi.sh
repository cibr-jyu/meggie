#!/bin/bash

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
