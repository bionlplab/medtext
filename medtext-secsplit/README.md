This module splits the report into sections. 

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

