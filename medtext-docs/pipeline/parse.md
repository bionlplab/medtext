# Constituency Parsing

medtext uses the [Bllip parser](https://github.com/BLLIP/bllip-parser)
to obtain the parse tree. The Bllip parser was trained on the biomedical text.

```shell
Usage:
    medtext-parse parse [options] -i FILE -o FILE
    medtext-parse download [--bllip-model DIR]

Options:
    -i FILE             Inpput file
    -o FILE             Output file
    --overwrite         Overwrite the existing file
    --bllip-model DIR   Bllip parser model path [default: ~/.medtext/bllipparser/BLLIP-GENIA-PubMed]
    --only-ner          Parse the sentences with NER annotations at the passage level
```

```python
from medtext_parse.models.bllipparser import BioCParserBllip
processor = BioCParserBllip(
    model_dir=os.path.expanduser(argv['--bllip-model']),
    only_ner=argv['--only-ner'])
```