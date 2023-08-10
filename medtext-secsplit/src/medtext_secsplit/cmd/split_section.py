"""
Usage:
    split_section regex [--section-titles FILE | --overwrite] -i FILE -o FILE
    split_section medspacy [--overwrite] -i FILE -o FILE
    split_section download [--section-titles FILE]

Options:
    --section-titles FILE   List of section titles [default: ~/.medtext/resources/section_titles.txt]
    -o FILE
    -i FILE
    --overwrite
"""
import os.path

import bioc
import docopt

from medtext_commons.cmd_utils import process_options
from medtext_commons.download_utils import request_medtext
from medtext_secsplit.models.section_split_regex import BioCSectionSplitterRegex, combine_patterns


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)
    if argv['download']:
        request_medtext(os.path.expanduser(argv['--section-titles']))
        return
    if argv['regex']:
        with open(os.path.expanduser(argv['--section-titles'])) as fp:
            section_titles = [line.strip() for line in fp]
        pattern = combine_patterns(section_titles)
        processor = BioCSectionSplitterRegex(regex_pattern=pattern)
    elif argv['medspacy']:
        import medspacy
        from medtext_secsplit.models.section_split_medspacy import BioCSectionSplitterMedSpacy
        nlp = medspacy.load()
        nlp.add_pipe("medspacy_sectionizer")
        processor = BioCSectionSplitterMedSpacy(nlp)
    else:
        raise KeyError

    with open(argv['-i']) as fp:
        collection = bioc.load(fp)

    processor.process_collection(collection)

    with open(argv['-o'], 'w') as fp:
        bioc.dump(collection, fp, bioc.BioCVersion.V1)


if __name__ == '__main__':
    main()
