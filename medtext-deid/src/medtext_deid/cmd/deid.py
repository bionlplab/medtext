"""
Usage:
    medtext-deid philter [options] -i FILE -o FILE
    medtext-deid bert [options] (--collection | --document | --passage) -i FILE -o FILE
    medtext-deid download

Options:
    -i FILE         Input file
    -o FILE         Output file
    --overwrite     Overwrite the existing file
    --repl CHAR     PHI replacement char [default: X]
    --collection    Every document has one passage and that passage has
                    no sentences
    --document      Every document has a list of passages and these passages
                    have no sentences
    --passage       Every passage has a list sentences [default: 0]
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
        if argv['--collection']:
            process_file(argv['-i'], argv['-o'], processor, 0)
        elif argv['--document']:
            process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)
        elif argv['--passage']:
            process_file(argv['-i'], argv['-o'], processor, bioc.PASSAGE)


if __name__ == '__main__':
    main()
