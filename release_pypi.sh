#!/usr/bin/env bash

# Before, remember to:
# 1) Update pyproject.toml
# 2) Update CHANGES.rst
# 3) Add a tag

if [[ -z "${INTERP}" ]]; then
  INTERP=python
fi

echo "Removing previous build artifacts"
rm -f dist/*

echo "Building source distribution.."
$INTERP -m build

echo "Uploading to PyPi.."
$INTERP -m twine upload dist/*

echo "Finished."
