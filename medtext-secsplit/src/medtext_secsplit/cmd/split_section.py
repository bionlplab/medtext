"""
Usage:
    split_section regex [--section-titles FILE | --overwrite] -i FILE -o FILE
    split_section medspacy [--overwrite] -i FILE -o FILE
    split_section download [--section-titles FILE]

Options:
    --section-titles FILE   List of section titles [default: .radtext/resources/section_titles.txt]
    -o FILE
    -i FILE
    --overwrite
"""
import bioc
import docopt

from medtext_base.cmd.utils import process_options
from medtext_base.download_utils import request_medtext
from medtext_secsplit.models.section_split_regex import BioCSectionSplitterRegex, combine_patterns


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    try:
        if argv['regex']:
            with open(argv['--section-titles']) as fp:
                section_titles = [line.strip() for line in fp]
            pattern = combine_patterns(section_titles)
            processor = BioCSectionSplitterRegex(regex_pattern=pattern)
        elif argv['medspacy']:
            import medspacy
            from medtext_secsplit.models.section_split_medspacy import BioCSectionSplitterMedSpacy
            nlp = medspacy.load(enable=["sectionizer"])
            processor = BioCSectionSplitterMedSpacy(nlp)
        elif argv['download']:
            request_medtext(argv['--section-titles'])
            return
        else:
            raise KeyError
    except KeyError as e:
        raise e

    with open(argv['-i']) as fp:
        collection = bioc.load(fp)

    processor.process_collection(collection)

    with open(argv['-o'], 'w') as fp:
        bioc.dump(collection, fp, bioc.BioCVersion.V1)


if __name__ == '__main__':
    main()
