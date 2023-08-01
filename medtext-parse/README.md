This module uses the Bllip parser to obtain the parse tree. The Bllip parser was trained on the biomedical text.

## Quickstart

```shell
$ medtext-secsplit medspacy -i /path/to/input.xml -o /path/to/output.xml
```

```python
import medspacy
from medtext_secsplit.models.section_split_medspacy import BioCSectionSplitterMedSpacy

nlp = medspacy.load(enable=["sectionizer"])
processor = BioCSectionSplitterMedSpacy(nlp)
```

## Links

* [Documentation](https://radtext.readthedocs.io/en/latest/index.html)
* [MedText homepage](https://github.com/bionlplab/radtext)

