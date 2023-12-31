"""
Usage:
    medtext-parse parse [options] -i FILE -o FILE
    medtext-parse download [--bllip-model DIR]

Options:
    -i FILE             Inpput file
    -o FILE             Output file
    --overwrite         Overwrite the existing file
    --bllip-model DIR   Bllip parser model path [default: ~/.medtext/bllipparser/BLLIP-GENIA-PubMed]
    --only-ner          Parse the sentences with NER annotations at the passage level
"""
import os.path
from pathlib import Path

import docopt

import bioc
from medtext_commons.cmd_utils import process_options, process_file
from medtext_parse.models.bllipparser import BioCParserBllip

BLLIP_MODEL_URL = 'https://nlp.stanford.edu/~mcclosky/models/BLLIP-GENIA-PubMed.tar.bz2'


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['parse']:
        processor = BioCParserBllip(
            model_dir=os.path.expanduser(argv['--bllip-model']),
            only_ner=argv['--only-ner'])
        process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)
    elif argv['download']:
        from bllipparser import ModelFetcher
        model_dir = Path(os.path.expanduser(argv['--bllip-model'])).parent
        print("Downloading: %s from [%s]" % (model_dir, BLLIP_MODEL_URL))
        if not model_dir.exists():
            model_dir.mkdir(parents=True)
        ModelFetcher.download_and_install_model(BLLIP_MODEL_URL, str(model_dir))

        print("Downloading: StanfordDependencies")
        import StanfordDependencies
        StanfordDependencies.StanfordDependencies(download_if_missing=True)
    else:
        raise KeyError


if __name__ == '__main__':
    main()
