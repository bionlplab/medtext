"""
Usage:
    preprocess stanza [options] -i FILE -o FILE
    preprocess spacy [--overwrite --spacy-model NAME] -i FILE -o FILE
    preprocess download spacy [--spacy-model]
    preprocess download stanza

Options:
    --overwrite
    --spacy-model NAME   spaCy trained model [default: en_core_web_sm]
    -o FILE
    -i FILE
"""
import subprocess
import sys

import bioc
import docopt
import spacy
import stanza

from medtext_base.cmd.utils import process_options, process_file
from medtext_preprocess.models.preprocess_spacy import BioCSpacy
from medtext_preprocess.models.preprocess_stanza import BioCStanza


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['stanza']:
        try:
            nlp = stanza.Pipeline('en', processors='tokenize,pos,lemma,depparse')
        except FileNotFoundError:
            print('Install spacy model using \'python -m spacy download en_core_web_sm\'')
            return
        processor = BioCStanza(nlp)
    elif argv['spacy']:
        try:
            nlp = spacy.load(argv['--spacy-model'])
        except IOError:
            print('Install spacy model using \'python -m spacy download en_core_web_sm\'')
            return
        processor = BioCSpacy(nlp)
    elif argv['download']:
        if argv['spacy']:
            print('Downloading: space %s' % argv['--spacy-model'])
            subprocess.check_call([sys.executable, '-m', 'spacy', 'download', argv['--spacy-model']])
        elif argv['stanza']:
            print('Downloading: Stanza en')
            stanza.download('en')
        else:
            raise KeyError
    else:
        raise KeyError

    process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)


if __name__ == '__main__':
    main()
