# Sentence Split

This module splits the report into sentences using
[NLTK](https://www.nltk.org/api/nltk.tokenize.html).

```shell
Usage:
    medtext-ssplit ssplit [options] -i FILE -o FILE
    medtext-ssplit download

Options:
    -i FILE         Input file
    -o FILE         Output file
    --overwrite     Overwrite the existing file
    --newline       Whether to treat newlines as sentence breaks.
```

```python
from medtext_ssplit.models.sentence_split_nltk import BioCSSplitterNLTK
processor = BioCSSplitterNLTK(newline=argv['--newline'])
```