"""
Usage:
    medtext-neg neg [--regex-patterns FILE --ngrex-patterns FILE --overwrite --sort-anns] -i FILE -o FILE
    medtext-neg download [--regex-patterns FILE --ngrex-patterns FILE]

Options:
    -i FILE                 Inpput file
    -o FILE                 Output file
    --overwrite             Overwrite the existing file
    --regex-patterns FILE   Regular expression patterns [default: ~/.medtext/resources/patterns/regex_patterns.yml]
    --ngrex-patterns FILE   Nregex-based expression patterns [default: ~/.medtext/resources/patterns/ngrex_patterns.yml]
    --sort-anns             Sort annotations by its location
"""
import os.path
import bioc
from medtext_commons.core import BioCPipeline

import docopt
from medtext_commons.cmd_utils import process_options, process_file
from medtext_neg.models.neg_cleanup import NegCleanUp
from medtext_neg.models.neg import BioCNeg

def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['neg']:
        neg_actor = BioCNeg()
        cleanup_actor = NegCleanUp()
        pipeline = BioCPipeline()
        pipeline.processors = [neg_actor, cleanup_actor]
        process_file(argv['-i'], argv['-o'], pipeline, bioc.PASSAGE)
    else:
        raise KeyError

if __name__ == '__main__':
    main()
