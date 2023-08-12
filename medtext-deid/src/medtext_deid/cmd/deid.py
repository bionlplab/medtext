"""
Usage:
    clid philter [options] -i FILE -o FILE
    clid bert [options] -i FILE -o FILE
    clid download

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
from medtext_deid.models.deid_robust_deid import BioCRobustDeid


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)
    if argv['philter']:
        processor = BioCDeidPhilter(argv['--repl'])
        process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)
    elif argv['download']:
        print('Downloading: NLTK averaged_perceptron_tagger')
        nltk.download('averaged_perceptron_tagger')
    elif argv['bert']:
        processor = BioCRobustDeid(repl=argv['--repl'])
        process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)


if __name__ == '__main__':
    main()
