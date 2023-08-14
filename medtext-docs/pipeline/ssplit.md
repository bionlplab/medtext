# Sentence Split

This module splits the report into sentences using
[NLTK](https://www.nltk.org/api/nltk.tokenize.html).

```shell
Usage:
    medtext-ssplit ssplit [options] -i FILE -o FILE
    medtext-ssplit download

Options:
    --newline       Whether to treat newlines as sentence breaks.
    -o FILE         Output file
    -i FILE         Input file
    --overwrite     Overwrite the existing file
```

```python
from medtext_ssplit.models.sentence_split_nltk import BioCSSplitterNLTK
processor = BioCSSplitterNLTK(newline=argv['--newline'])
```