<img src="https://github.com/bionlplab/medtext/blob/main/medtext-icon/medtext.png?raw=true" alt="MedText" width="500"/>

## Purpose

medtext is a high-performance Python Clinical Text Analysis System.

## Prerequisites

* Python >= 3.6, <3.9
* Linux 
* Java

```shell
# Set up environment
$ sudo apt-get install python3-dev build-essential default-java
```

## Quickstart

The latest medtext releases are available over
[pypi](https://pypi.org/project/medtext/).

Using pip, medtext releases are available as source packages and binary wheels.
It is also generally recommended installing packages in a virtual environment to
avoid modifying system state:

```shell
$ git clone https://github.com/bionlplab/medtext.git
$ cd medtext

# create virtual environment
$ python -m venv medtext-venv
$ source medtext-venv/bin/activate
$ pip install -U pip setuptools wheel

# download the packages and install modules
$ pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple medtext
$ cd medtext-neg
$ pip install .
$ cd ../medtext-deid
$ pip install .

# build project
$ cd ../medtext
$ pip install .

# download all models
$ cd ..
$ bash medtext/download_all.sh
```
medtext supports command-line interfaces for specific NLP tasks (e.g.,
de-identification, sentence split, or named entity recognition).

```shell
$ medtext-deid philter --repl=X -i /path/to/input.xml -o /path/to/output.xml
$ medtext-ssplit ssplit -i /path/to/input.xml -o /path/to/output.xml
$ medtext-neg-prompt neg -i /path/to/input.xml -o /path/to/output.xml
```

medtext also supports the Python interactive
interpreter. More details on the medtext's pipeline can be
found at [Pipeline](https://medtext.readthedocs.io/en/latest/pipeline/index.html).

## Documentation

You will find complete documentation at our [Read the Docs
site](https://medtext.readthedocs.io/en/latest/index.html).

## Contributing

You can find information about contributing to medtext at our [Contribution
page](https://medtext.readthedocs.io/en/latest/contribute.html).

## Acknowledgment

This work is supported by the National Library of Medicine under Award No.
4R00LM013001 and the NIH Intramural Research Program, National Library of
Medicine.

You can find Acknowledgment information at our [Acknowledgment
page](https://medtext.readthedocs.io/en/latest/acknowledgments.html).

## License

Copyright BioNLP Lab at Weill Cornell Medicine, 2022.

Distributed under the terms of the [MIT](https://github.com/bionlplab/medtext/blob/master/LICENSE) license, 
medtext is free and open source software.
