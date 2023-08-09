# Installation instructions

medtext is compatible with Python (3.6-3.8) and runs on Unix/Linux and macOS/OS X. 
The latest medtext releases are available over
[pypi](https://pypi.python.org/pypi/medtext).

Using pip, medtext releases are available as source packages and binary wheels.
It is also generally recommended installing packages in a virtual
environment to avoid modifying system state:

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -U pip setuptools wheel
$ pip install -U medtext
$ python -m spacy download en_core_web_sm
$ medtext-download --all
```
