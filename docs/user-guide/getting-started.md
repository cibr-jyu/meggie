# Installation

Meggie does not have standalone installers, but it can be easily installed on Windows, macOS, or Linux systems with Python 3.9 or higher using either of the following methods:

## Using conda

### Installing miniconda

If conda is not already installed on your system, follow these steps:

1. Visit the Miniconda download page: [https://docs.conda.io/projects/conda](https://docs.conda.io/projects/conda)

2. Download the appropriate installer for your operating system:

    - **Windows**: Miniconda3-latest-Windows-x86_64.exe
    - **Linux**: Miniconda3-latest-Linux-x86_64.sh
    - **macOS**: Miniconda3-latest-MacOSX-x86_64.pkg

3. Run the downloaded installer and follow the on-screen instructions to complete the installation.

### Opening the Anaconda Prompt

- **Windows**: After installation, you can access the Anaconda Prompt from the Start Menu. This opens a terminal window with conda commands available.

- **Linux/macOS**: During installation, Miniconda updates the `.zshrc` or `.bashrc` file (depending on your default shell). Use the standard terminal application, and you may need to open a new terminal window to access the conda commands. The prompt should display “(base)” to indicate that conda is active.

### Installing Meggie

Install Meggie in a conda environment:
```bash
$ conda create -n meggie-env -c conda-forge --solver libmamba meggie=={{VERSION}}
```

## Using pip:

Alternatively, if you have a standard python installation, you can directly use venv and pip to install Meggie in a virtual environment.

Create a virtual environment folder:
```bash
$ python -m venv meggie-env
```
Activate the environment:
```bash
$ source meggie-env/bin/activate
```
Install Meggie:
```bash
pip install meggie=={{VERSION}}
```

# Starting Meggie for the first time
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
