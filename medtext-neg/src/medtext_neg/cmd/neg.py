"""
Usage:
    neg neg [options] -i FILE -o FILE
    neg download

Options:
    --regex_patterns FILE               [default: .medtext/resources/patterns/regex_patterns.yml]
    --ngrex_patterns FILE               [default: .medtext/resources/patterns/ngrex_patterns.yml]
    --overwrite
    --sort_anns
    -o FILE
    -i FILE
"""
from pathlib import Path

import bioc

from medtext_commons.download_utils import request_medtext
from medtext_commons.core import BioCPipeline

"""
    --regex_negation FILE               [default: .medtext/resources/patterns/regex_negation.yml]
    --regex_uncertainty_pre_neg FILE    [default: .medtext/resources/patterns/regex_uncertainty_pre_negation.yml]
    --regex_uncertainty_post_neg FILE   [default: .medtext/resources/patterns/regex_uncertainty_post_negation.yml]
    --regex_double_neg FILE             [default: .medtext/resources/patterns/regex_double_negation.yml]
    --ngrex_negation FILE               [default: .medtext/resources/patterns/ngrex_negation.yml]
    --ngrex_uncertainty_pre_neg FILE    [default: .medtext/resources/patterns/ngrex_uncertainty_pre_negation.yml]
    --ngrex_uncertainty_post_neg FILE   [default: .medtext/resources/patterns/ngrex_uncertainty_post_negation.yml]
    --ngrex_double_neg FILE             [default: .medtext/resources/patterns/ngrex_double_negation.yml]
"""
import docopt
from medtext_commons.cmd_utils import process_options, process_file
from medtext_neg.models.match_ngrex import NegGrexPatterns
from medtext_neg.models.neg import NegRegexPatterns
from medtext_neg.models.neg_cleanup import NegCleanUp
from medtext_neg.models.neg import BioCNeg


DEFAULT_RADLEX = Path.home() / '.medtext/resources/Radlex4.1.xlsx'


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['neg']:
        regex_actor = NegRegexPatterns()
        regex_actor.load_yml2(argv['--regex_patterns'])
        ngrex_actor = NegGrexPatterns()
        ngrex_actor.load_yml2(argv['--ngrex_patterns'])

        neg_actor = BioCNeg(regex_actor=regex_actor, ngrex_actor=ngrex_actor)
        cleanup_actor = NegCleanUp(argv['--sort_anns'])
        pipeline = BioCPipeline()
        pipeline.processors = [neg_actor, cleanup_actor]

        process_file(argv['-i'], argv['-o'], pipeline, bioc.PASSAGE)
    elif argv['download']:
        request_medtext(argv['--regex_patterns'])
        request_medtext(argv['--ngrex_patterns'])
    else:
        raise KeyError

if __name__ == '__main__':
    main()
