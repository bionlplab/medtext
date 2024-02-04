"""
Usage:
    medtext-neg-prompt neg [--model-dir DIR --overwrite] -i FILE -o FILE
    medtext-neg-prompt download [--model FILE --model-dir DIR]

Options:
    -i FILE                 Inpput file
    -o FILE                 Output file
    --overwrite             Overwrite the existing file
    --model FILE            Pretrained model file [default: ~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint.zip]
    --model-dir DIR         [default: ~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint]
"""
import os.path
from pathlib import Path

import bioc
import gdown
from zipfile import ZipFile
from medtext_commons.core import BioCPipeline

import docopt
from medtext_commons.cmd_utils import process_options, process_file
from medtext_neg.models.neg_cleanup import NegCleanUp
from medtext_neg.models.prompt.neg_prompt import BioCNegPrompt

# MODEL_URL = 'https://drive.google.com/uc?id=17xFCEPwdtoHZv8UMFjr7Vl_k8N2Dq1wt'  # 3 class
MODEL_URL = 'https://drive.google.com/uc?id=1e6VooVTKjMWLCedGMONVKButOBtWBbVH'  # 6 class


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    if argv['neg']:
        model_dir = Path(argv['--model-dir']).expanduser()
        neg_actor = BioCNegPrompt(pretrained_model_dir=model_dir)
        cleanup_actor = NegCleanUp()
        pipeline = BioCPipeline()
        pipeline.processors = [neg_actor, cleanup_actor]
        process_file(argv['-i'], argv['-o'], pipeline, bioc.PASSAGE)
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


if __name__ == '__main__':
    main()
