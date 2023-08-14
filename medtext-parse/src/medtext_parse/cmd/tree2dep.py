"""
Usage:
    medtext-tree2dep [options] -i FILE -o FILE

Options:
    -i FILE         Inpput file
    -o FILE         Output file
    --overwrite     Overwrite the existing file
"""
import bioc
import docopt

from medtext_commons.cmd_utils import process_options, process_file
from medtext_parse.models.tree2dep import BioCPtb2DepConverter


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    processor = BioCPtb2DepConverter()
    process_file(argv['-i'], argv['-o'], processor, bioc.SENTENCE)


if __name__ == '__main__':
    main()