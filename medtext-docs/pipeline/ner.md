# Named entity recognition

The named entity recognition (NER) module recognizes mention spans of a
particular entity type (e.g., abnormal findings) from the reports.
We provide two options for NER.

```shell
Usage:
    medtext-ner spacy [--overwrite --spacy-model NAME --radlex FILE] -i FILE -o FILE
    medtext-ner regex [--overwrite] --phrases FILE -i FILE -o FILE
    medtext-ner download [--spacy-model NAME]

Options:
    -i FILE             Inpput file
    -o FILE             Output file
    --overwrite         Overwrite the existing file
    --phrases FILE      Phrase patterns
    --radlex FILE       The RadLex ontology file [default: .medtext/resources/Radlex4.1.xlsx]
    --spacy-model NAME  spaCy trained model [default: en_core_web_sm]
```

## regex

The rule-based method uses regular expressions that combine information from
terminological resources and characteristics of the entities of interest.
They are manually constructed by domain experts.

```python
from pathlib import Path
from medtext_ner.models.ner_regex import NerRegExExtractor, BioCNerRegex, load_yml

patterns = load_yml(argv['--phrases'])
extractor = NerRegExExtractor(patterns)
processor = BioCNerRegex(extractor, name=Path(argv['--phrases']).stem)
```

## spacy

[**SpaCy's PhraseMatcher**](https://spacy.io/api/phrasematcher) provides another
way to efficiently match large terminology lists. medtext uses PhraseMatcher to
recognize concepts in the [RadLex ontology](http://radlex.org/).

```python
import spacy
from medtext_ner.models.ner_spacy import NerSpacyExtractor, BioCNerSpacy
from medtext_ner.models.radlex import RadLex4

nlp = spacy.load(argv['--spacy-model'], exclude=['ner', 'parser', 'senter'])
radlex = RadLex4(argv['--radlex'])
matchers = radlex.get_spacy_matchers(nlp)
extractor = NerSpacyExtractor(nlp, matchers)
processor = BioCNerSpacy(extractor, 'RadLex')
```

## Phrase patterns

The pattern file is in the [yaml](https://yaml.org/) format. It contains a list of concepts where the key serves as the
preferred name. Each concept should contain three attributes: `concept_id`, `include`, and
`exclude`. 
`include` contains the regular expressions that the concept will match.
`exclude` contains the regular expressions that the concept will not match, even if its substring will match the regular
expressions in the `include`

Using the following example, medtext will recognize "emphysema", but reject "subcutaneous emphysema" though "emphysema"
is part of "subcutaneous emphysema".

```yaml
Emphysema:
  concept_id: RID4799
  include:
    - emphysema
  exclude:
    - subcutaneous emphysema
```