# Section Split

This module splits the report into sections. 
We provide two options for section split.

```shell
Usage:
    medtext-secsplit regex [--section-titles FILE --overwrite] -i FILE -o FILE
    medtext-secsplit medspacy [--overwrite] -i FILE -o FILE
    medtext-secsplit download [--section-titles FILE]

Options:
    -o FILE                 Input file
    -i FILE                 Output file
    --overwrite             Overwrite the existing file
    --section-titles FILE   List of section titles [default: ~/.medtext/resources/medspacy_section_titles.txt]
```

## regex

This **rule-based** module uses a list of section titles to split the notes.

```python
from medtext_secsplit.models.section_split_regex import BioCSectionSplitterRegex, combine_patterns

with open(argv['--section-titles']) as fp:
    section_titles = [line.strip() for line in fp]
pattern = combine_patterns(section_titles)
processor = BioCSectionSplitterRegex(regex_pattern=pattern)
```

We provide two sets of section titles
* `medspacy_section_titles`: rules from [medspacy](https://github.com/medspacy/medspacy/blob/master/resources/section_patterns.json), 
    which are adapted from [SecTag](https://www.vumc.org/cpm/cpm-blog/sectag-tagging-clinical-note-section-headers) and expanded through practice
* `cxr_section_titles`: rules from the analysis of radiology reports in MIMIC-CXR

## medspacy

[**MedSpaCy**](https://github.com/medspacy/medspacy) is a spaCy tool for performing
clinical NLP and text processing tasks.
It includes an implementation of clinical section detection based on rule-based
matching of the section titles with default rules adapted from
[SecTag](https://pubmed.ncbi.nlm.nih.gov/18999303/) and
expanded through practice.

```python
import medspacy
from medtext_secsplit.models.section_split_medspacy import BioCSectionSplitterMedSpacy
nlp = medspacy.load()
nlp.add_pipe("medspacy_sectionizer")
processor = BioCSectionSplitterMedSpacy(nlp)
```
