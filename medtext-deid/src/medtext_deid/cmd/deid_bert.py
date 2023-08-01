"""
Usage:
    deid [options] -i FILE -o FILE

Options:
    --overwrite
    -o FILE
    -i FILE
    --repl CHAR                 PHI replacement char [default: X]
    --bert-deid-model DIR       [default: ~/.radtext/bert_deid_model]
"""
import os
import subprocess

import bioc
import docopt

from medtext_base.cmd.utils import process_options, process_file
from medtext_deid.models.deid_bert import BioCDeidBert


def main():
    argv = docopt.docopt(__doc__)
    process_options(argv)

    model_path = os.path.expanduser(argv['--bert-deid-model'])
    # download model
    print('Downloading the model: %s' % model_path)
    my_env = os.environ.copy()
    my_env["PATH"] = my_env['PATH'] + ':' + model_path
    subprocess.check_call(['bert_deid', '--model_dir=%s' % model_path, 'download'])

    processor = BioCDeidBert(repl=argv['--repl'], model_path=model_path)
    process_file(argv['-i'], argv['-o'], processor, bioc.DOCUMENT)


if __name__ == '__main__':
    main()
