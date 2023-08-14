# Text preprocessing

This module provides sentence split, tokenization, part-of-speech tagging,
lemmatization and dependency parsing. 
We provide two options for text preprocessing.

```shell
Usage:
    medtext-preprocess stanza [--overwrite] -i FILE -o FILE
    medtext-preprocess spacy [--overwrite --spacy-model NAME] -i FILE -o FILE
    medtext-preprocess download spacy [--spacy-model=NAME]
    medtext-preprocess download stanza

Options:
    -i FILE             Input file
    -o FILE             Output file
    --overwrite         Overwrite the existing file
    --spacy-model NAME  spaCy trained model [default: en_core_web_sm]
```

## spacy

[**spaCy**](https://spacy.io/) is an open-source Python library for Natural Language
Processing.

```python
import spacy
from medtext_preprocess.models.preprocess_spacy import BioCSpacy

nlp = spacy.load(argv['--spacy-model'])
processor = BioCSpacy(nlp)
```

## stanza

[**Stanza**](https://stanfordnlp.github.io/stanza/) is a collection of efficient
tools for Natural Language Processing.

```python
import stanza
from medtext_preprocess.models.preprocess_stanza import BioCStanza

nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
processor = BioCStanza(nlp)
```