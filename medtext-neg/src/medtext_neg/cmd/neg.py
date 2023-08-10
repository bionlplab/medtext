"""
Usage:
    cmd neg [--regex-patterns FILE --ngrex-patterns FILE --overwrite --sort-anns] -i FILE -o FILE
    cmd download [--regex-patterns FILE --ngrex-patterns FILE]

Options:
    --regex-patterns=FILE    [default: ~/.medtext/resources/patterns/regex_patterns.yml]
    --ngrex-patterns=FILE    [default: ~/.medtext/resources/patterns/ngrex_patterns.yml]
    --overwrite
    --sort-anns
    -o FILE
    -i FILE
"""
import os.path
from pathlib import Path

import bioc

from medtext_commons.download_utils import request_medtext, MEDTEXT_RESOURCES_GITHUB
from medtext_commons.core import BioCPipeline


import docopt
from medtext_commons.cmd_utils import process_options, process_file
from medtext_neg.models.match_ngrex import NegGrexPatterns
from medtext_neg.models.neg import NegRegexPatterns
from medtext_neg.models.neg_cleanup import NegCleanUp
from medtext_neg.models.neg import BioCNeg


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
        cleanup_actor = NegCleanUp(argv['--sort_anns'])
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
