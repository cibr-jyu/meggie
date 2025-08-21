# Getting Started

Meggie can be installed on Windows, macOS, or Linux (Python 3.10+).
Follow one of the three methods below.

---

## 1. Installing via uv

### Installation

Meggie can be installed via [uv](https://github.com/astral-sh/uv) with:

```bash
$ uv tool install meggie=={{VERSION}}
```

### Running Meggie

Simply run:

```bash
meggie
```

---

## 2. Installing via pip

### Installation
Create a virtual environment and install Meggie:

```bash
python -m venv meggie-env
source meggie-env/bin/activate
pip install meggie=={{VERSION}}
```

### Running Meggie

With the venv activated, run:

```bash
meggie
```

---

## 3. Installing via conda

### Installation

If conda is not already installed on your system, follow these steps:

1. Visit the Miniconda download page: [https://docs.conda.io/projects/conda](https://docs.conda.io/projects/conda)

2. Download the appropriate installer for your operating system:

    - **Windows**: Miniconda3-latest-Windows-x86_64.exe
    - **Linux**: Miniconda3-latest-Linux-x86_64.sh
    - **macOS**: Miniconda3-latest-MacOSX-x86_64.pkg

3. Run the downloaded installer and follow the on-screen instructions to complete the installation.

#### Installing Meggie

Create a new conda environment and install Meggie:

```bash
conda create -n meggie-env -c conda-forge --solver libmamba meggie=={{VERSION}}
conda activate meggie-env
```

### Running Meggie

With the conda environment activated, run:

```bash
meggie
```
