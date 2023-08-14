# Developer Guide

## Development Installation

These are development setup. If you are a contributor to medtext, it might be
a good idea to follow these guidelines as well.

To follow these instructions you will need a Unix/Linux system, or 
[Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/). 
Other operating systems are not supported.

```{warning} 
We do not recommend following this guide to deploy an instance of Read the Docs
for production usage. Take into account that this setup is only useful for
developing purposes.
```

### Set up your environment

* Python >=3.6, <3.9
* Linux
* Java

Install system-level dependencies via `apt`

```shell
$ sudo apt install python3 python3-dev build-essential default-java
```

#### Windows (experimental)

* python >=3.6, <3.9
* Java
* Microsoft Visual C++ >=14.0

When working on Microsoft Windows OS, some packages requires Microsoft Visual
C++ 14.0 or greater. You can get it with [Microsoft C++ Build
Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools)

After install Microsoft Build Tools for Visual Studio, select: Workloads →
Desktop development with C++, then for Individual Components, select only:

*  Windows SDK 
*  C++ x64/x86 build tools

The build tools allow using MSVC "cl.exe" C / C++ compiler from the command line.

More information can be found at <https://www.scivision.dev/python-windows-visual-c-14-required/>

### Compile from source

medtext is actively developed on [GitHub repository](https://github.com/bionlplab/medtext).
The other way to install medtext is to clone its GitHub repository.

```shell
# Checkout repository
$ git clone https://github.com/bionlplab/medtext.git
$ cd medtext

# Set up Python environment
$ python -m venv venv
$ source venv/bin/activate

# Install dependencies
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt

# Install packages
$ python -m spacy download en_core_web_sm
$ python medtext/cmd/download.py all
```

## Create this documentation

We use Sphinx and MyST to generate documentation.

```shell
$ pip install sphinx sphinx_rtd_theme myst-parser
$ cd docs
$ make html
```

## Publish MedText to PyPI and TestPyPI

You need two more packages to publish the software to pypi.

```shell
$ pip install build twine
```

First, you need a PyPI user account. You can create an account using the
form on the PyPI/TestPyPI website.

Now you’ll create a PyPI/TestPyPI API token so you will be able to
securely upload your project.

Go to <https://pypi.org/manage/account/#api-tokens> and create a new API
token; don’t limit its scope to a particular project, since you are
creating a new project.

```shell
$ python -m build
```

Using local package with pip

```shell
$ pip install -e .
```

Using TestPyPI with pip

```shell
$ twine upload --repository testpypi dist/*
$ pip install --index-url https://test.pypi.org/simple/ medtext
```

### Validate MedText

```shell
$ bash tests/validate.sh
```

### Test

Install `pytest` and `pytest-cov`. Then, for each module, run

```shell
$ pytest --cov=. --cov-report=html
```