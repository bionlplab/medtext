This module splits the report into sentences. 

## Quickstart

```shell
$ medtext-ssplit -i /path/to/input.xml -o /path/to/output.xml
```

```python
from medtext.models.sentence_split_nltk import BioCSSplitterNLTK
processor = BioCSSplitterNLTK(newline=argv['--newline'])
```

## Links

* [Documentation](https://radtext.readthedocs.io/en/latest/index.html)
* [MedText homepage](https://github.com/bionlplab/radtext)

