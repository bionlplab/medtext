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

from medtext_commons.download_utils import request_medtext, MEDTEXT_RESOURCES_GITHUB
from medtext_commons.core import BioCPipeline


import docopt
from medtext_commons.cmd_utils import process_options, process_file
from medtext_neg.models.rules.match_ngrex import NegGrexPatterns
from medtext_neg.models.rules.neg import NegRegexPatterns
from medtext_neg.models.neg_cleanup import NegCleanUp
from medtext_neg.models.rules.neg import BioCNeg


# DEFAULT_RADLEX = Path.home() / '.medtext/resources/Radlex4.1.xlsx'
'''
    --regex-negation FILE               [default: ~/.medtext/resources/patterns/regex_negation.yml]
    --regex-uncertainty-pre-neg FILE    [default: ~/.medtext/resources/patterns/regex_uncertainty_pre_negation.yml]
    --regex-uncertainty-post-neg FILE   [default: ~/.medtext/resources/patterns/regex_uncertainty_post_negation.yml]
    --regex-double-neg FILE             [default: ~/.medtext/resources/patterns/regex_double_negation.yml]
    --ngrex-negation FILE               [default: ~/.medtext/resources/patterns/ngrex_negation.yml]
    --ngrex-uncertainty-pre-neg FILE    [default: ~/.medtext/resources/patterns/ngrex_uncertainty_pre_negation.yml]
    --ngrex-uncertainty-post-neg FILE   [default: ~/.medtext/resources/patterns/ngrex_uncertainty_post_negation.yml]
    --ngrex-double-neg FILE             [default: ~/.medtext/resources/patterns/ngrex_double_negation.yml]
'''


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['neg']:
        regex_actor = NegRegexPatterns()
        regex_actor.load_yml2(os.path.expanduser(argv['--regex-patterns']))
        ngrex_actor = NegGrexPatterns()
        ngrex_actor.load_yml2(os.path.expanduser(argv['--ngrex-patterns']))

        neg_actor = BioCNeg(regex_actor=regex_actor, ngrex_actor=ngrex_actor)
        cleanup_actor = NegCleanUp(argv['--sort-anns'])
        pipeline = BioCPipeline()
        pipeline.processors = [neg_actor, cleanup_actor]

        process_file(argv['-i'], argv['-o'], pipeline, bioc.PASSAGE)
    elif argv['download']:
        request_medtext(os.path.expanduser(argv['--regex-patterns']),
                        src=MEDTEXT_RESOURCES_GITHUB + '/patterns/regex_patterns.yml')
        request_medtext(os.path.expanduser(argv['--ngrex-patterns']),
                        src=MEDTEXT_RESOURCES_GITHUB + '/patterns/ngrex_patterns.yml')
    else:
        raise KeyError


if __name__ == '__main__':
    main()
