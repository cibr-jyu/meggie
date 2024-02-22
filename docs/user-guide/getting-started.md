# Installation

Meggie does not have standalone installers, but it can be easily installed on Windows, macOS, or Linux systems with Python 3.9 or higher using either of the following methods:

## Using conda

Install meggie to a conda environment:
```bash
$ conda create -n meggie-env -c conda-forge meggie=={{VERSION}}
```

### Using pip:

Create a virtual environment folder:
```bash
$ python -m venv meggie-env
```
Activate the environment:
```bash
$ source meggie-env/bin/activate
```
Install dependencies:
```bash
$ pip install -r https://github.com/cibr-jyu/meggie/blob/{{VERSION}}/requirements.txt
```
Install meggie:
```bash
pip install meggie=={{VERSION}}
```
# Starting meggie for the first time
Activate the environment in which Meggie was installed. For conda:
```bash
conda activate meggie-env
```
Or, for pip:
```bash
source meggie-env/bin/activate
```
Then run Meggie:
```bash
$ meggie
```
