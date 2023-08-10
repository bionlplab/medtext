"""
Usage:
    deid philter [options] -i FILE -o FILE
    deid download

Options:
    --overwrite
    -o FILE
    -i FILE
    --repl CHAR    PHI replacement char [default: X]
"""
import bioc
import docopt
import nltk

from medtext_commons.cmd_utils import process_options, process_file
from medtext_deid.models.deid_philter import BioCDeidPhilter


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)
    if argv['philter']:
        processor = BioCDeidPhilter(argv['--repl'])
        process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)
    elif argv['download']:
        print('Downloading: NLTK averaged_perceptron_tagger')
        nltk.download('averaged_perceptron_tagger')


if __name__ == '__main__':
    main()
