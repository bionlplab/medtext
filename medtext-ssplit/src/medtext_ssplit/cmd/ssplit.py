"""
Usage:
    medtext-ssplit ssplit [options] -i FILE -o FILE
    medtext-ssplit download

Options:
    --newline       Whether to treat newlines as sentence breaks.
    -o FILE         Output file
    -i FILE         Input file
    --overwrite     Overwrite the existing file
"""
import bioc
import docopt
import nltk

from medtext_commons.cmd_utils import process_options, process_file
from medtext_ssplit.models.sentence_split_nltk import BioCSSplitterNLTK


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
