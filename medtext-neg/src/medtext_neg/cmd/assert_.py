"""
Usage:
    medtext-neg negbio [--regex-patterns FILE --ngrex-patterns FILE --overwrite --sort-anns] -i FILE -o FILE
    medtext-neg prompt [--model-dir DIR --overwrite] -i FILE -o FILE
    medtext-neg download negbio [--regex-patterns FILE --ngrex-patterns FILE]
    medtext-neg download prompt [--model FILE --model-dir DIR]

Options:
    -i FILE                 Inpput file
    -o FILE                 Output file
    --overwrite             Overwrite the existing file
    --regex-patterns FILE   Regular expression patterns [default: ~/.medtext/resources/patterns/regex_patterns.yml]
    --ngrex-patterns FILE   Nregex-based expression patterns [default: ~/.medtext/resources/patterns/ngrex_patterns.yml]
    --sort-anns             Sort annotations by its location
    --model FILE            Pretrained model file [default: ~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint.zip]
    --model-dir DIR         [default: ~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint]
"""
import os.path
from pathlib import Path
from zipfile import ZipFile

import bioc
import gdown

from medtext_commons.download_utils import request_medtext, MEDTEXT_RESOURCES_GITHUB
from medtext_commons.core import BioCPipeline


import docopt
from medtext_commons.cmd_utils import process_options, process_file
from medtext_neg.models.prompt.neg_prompt import BioCNegPrompt
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
MODEL_URL = 'https://drive.google.com/uc?id=1e6VooVTKjMWLCedGMONVKButOBtWBbVH'


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['negbio']:
        regex_actor = NegRegexPatterns()
        regex_actor.load_yml2(os.path.expanduser(argv['--regex-patterns']))
        ngrex_actor = NegGrexPatterns()
        ngrex_actor.load_yml2(os.path.expanduser(argv['--ngrex-patterns']))

        neg_actor = BioCNeg(regex_actor=regex_actor, ngrex_actor=ngrex_actor)
        cleanup_actor = NegCleanUp(argv['--sort-anns'])
        pipeline = BioCPipeline()
        pipeline.processors = [neg_actor, cleanup_actor]

        process_file(argv['-i'], argv['-o'], pipeline, bioc.PASSAGE)
    elif argv['prompt']:
        model_dir = Path(argv['--model-dir']).expanduser()
        neg_actor = BioCNegPrompt(pretrained_model_dir=model_dir)
        cleanup_actor = NegCleanUp()
        pipeline = BioCPipeline()
        pipeline.processors = [neg_actor, cleanup_actor]
        process_file(argv['-i'], argv['-o'], pipeline, bioc.PASSAGE)
    elif argv['download']:
        if argv['negbio']:
            request_medtext(os.path.expanduser(argv['--regex-patterns']),
                            src=MEDTEXT_RESOURCES_GITHUB + '/patterns/regex_patterns.yml')
            request_medtext(os.path.expanduser(argv['--ngrex-patterns']),
                            src=MEDTEXT_RESOURCES_GITHUB + '/patterns/ngrex_patterns.yml')
        elif argv['download']:
            model_path = Path(argv['--model']).expanduser()
            if not model_path.parent.exists():
                model_path.parent.mkdir(parents=True)
            if not model_path.exists():
                gdown.download(MODEL_URL, str(model_path), quiet=False)
            print('Model downloaded: %s' % model_path)
            model_dir = Path(argv['--model-dir']).expanduser()
            if not model_dir.exists():
                with ZipFile(model_path, 'r') as zObject:
                    zObject.extractall(model_dir.parent)
            print('Model extracted: %s' % model_dir)
        else:
            raise KeyError
    else:
        raise KeyError


if __name__ == '__main__':
    main()