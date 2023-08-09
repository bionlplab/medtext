# Text preprocessing

This module provides sentence split, tokenization, part-of-speech tagging,
lemmatization and dependency parsing. medtext provides two sub-modules for text preprocessing.

## preprocess:spacy

[**spaCy**](https://spacy.io/) is an open-source Python library for Natural Language
Processing.

### Options

| Option name   | Default          | Description              |
|:--------------|:-----------------|:-------------------------|
| --spacy-model | `en_core_web_sm` | The spaCy model          |

### Example Usage

```bash
$ medtext-preprocess spacy -i /path/to/input.xml -o /path/to/output.xml
```

```python
import spacy
from medtext_preprocess.models.preprocess_spacy import BioCSpacy

nlp = spacy.load(argv['--spacy-model'])
processor = BioCSpacy(nlp)
```

## preprocess:stanza

[**Stanza**](https://stanfordnlp.github.io/stanza/) is a collection of efficient
tools for Natural Language Processing.

### Example Usage

```bash
$ medtext-preprocess stanza -i /path/to/input.xml -o /path/to/output.xml
```

```python
import stanza
from medtext_preprocess.models.preprocess_stanza import BioCStanza

nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
processor = BioCStanza(nlp)
```