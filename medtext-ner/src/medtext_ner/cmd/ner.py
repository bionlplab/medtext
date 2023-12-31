"""
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
"""
import subprocess
import sys
from pathlib import Path
import bioc
import docopt
import spacy

from medtext_commons.cmd_utils import process_options, process_file
from medtext_commons.download_utils import request_medtext
from medtext_ner.models.ner_regex import NerRegExExtractor, BioCNerRegex, load_yml
from medtext_ner.models.ner_spacy import NerSpacyExtractor, BioCNerSpacy
from medtext_ner.models.radlex import RadLex4

DEFAULT_PHRASES = Path.home() / '.medtext/resources/cxr14_phrases_v2.yml'
DEFAULT_RADLEX = Path.home() / '.medtext/resources/Radlex4.1.xlsx'


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['download']:
        request_medtext(DEFAULT_PHRASES)
        request_medtext(DEFAULT_RADLEX)
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', argv['--spacy-model']])
    elif argv['spacy']:
        nlp = spacy.load(argv['--spacy-model'], exclude=['ner', 'parser', 'senter'])
        radlex = RadLex4(argv['--radlex'])
        matchers = radlex.get_spacy_matchers(nlp)
        extractor = NerSpacyExtractor(nlp, matchers)
        processor = BioCNerSpacy(extractor, 'RadLex')
        process_file(argv['-i'], argv['-o'], processor, bioc.PASSAGE)
    elif argv['regex']:
        patterns = load_yml(argv['--phrases'])
        extractor = NerRegExExtractor(patterns)
        processor = BioCNerRegex(extractor, name=Path(argv['--phrases']).stem)
        process_file(argv['-i'], argv['-o'], processor, bioc.PASSAGE)
    else:
        raise KeyError


if __name__ == '__main__':
    main()
