"""
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
"""
import subprocess
import sys

import bioc
import docopt
import spacy
import stanza

from medtext_commons.cmd_utils import process_options, process_file
from medtext_preprocess.models.preprocess_spacy import BioCSpacy
from medtext_preprocess.models.preprocess_stanza import BioCStanza


def download(argv):
    if argv['spacy']:
        print('Downloading: space %s' % argv['--spacy-model'])
        subprocess.check_call([sys.executable, '-m', 'spacy', 'download', argv['--spacy-model']])
    elif argv['stanza']:
        print('Downloading: Stanza en')
        stanza.download('en')
    else:
        raise KeyError


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['download']:
        download(argv)
        exit(1)
    elif argv['stanza']:
        try:
            nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
        except FileNotFoundError:
            print('Install spacy model using \'python -m spacy download en_core_web_sm\'')
            return
        processor = BioCStanza(nlp)
        process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)
    elif argv['spacy']:
        try:
            nlp = spacy.load(argv['--spacy-model'])
        except IOError:
            print('Install spacy model using \'python -m spacy download en_core_web_sm\'')
            return
        processor = BioCSpacy(nlp)
        process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)
    else:
        raise KeyError


if __name__ == '__main__':
    main()
