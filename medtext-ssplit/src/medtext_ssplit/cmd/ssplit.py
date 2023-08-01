"""
Usage:
    ssplit ssplit [options] -i FILE -o FILE
    ssplit download

Options:
    --newline   Whether to treat newlines as sentence breaks.
    -o FILE
    -i FILE
    --overwrite
"""
import bioc
import docopt
import nltk

from medtext_base.cmd.utils import process_options, process_file
from medtext_preprocess.models.sentence_split_nltk import BioCSSplitterNLTK


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)
    if argv['ssplit']:
        processor = BioCSSplitterNLTK(newline=argv['--newline'])
        process_file(argv['-i'], argv['-o'], processor, bioc.PASSAGE)
    elif argv['download']:
        print('Downloading: NLTK punkt')
        nltk.download('punkt')
    else:
        raise KeyError


if __name__ == '__main__':
    main()
