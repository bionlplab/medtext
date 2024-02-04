import docopt
from medtext_neg.cmd import assert_ as cli


def test_negbio_download():
    cmd = 'download negbio --regex-patterns FILE --ngrex-patterns FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['negbio'] is True
    assert argv['prompt'] is False
    assert argv['--regex-patterns'] == 'FILE'
    assert argv['--ngrex-patterns'] == 'FILE'

    cmd = 'download negbio'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--regex-patterns'] == '~/.medtext/resources/patterns/regex_patterns.yml'
    assert argv['--ngrex-patterns'] == '~/.medtext/resources/patterns/ngrex_patterns.yml'


def test_negbio():
    cmd = 'negbio --regex-patterns FILE --ngrex-patterns FILE --overwrite --sort-anns -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['negbio'] is True
    assert argv['download'] is False
    assert argv['prompt'] is False
    assert argv['--regex-patterns'] == 'FILE'
    assert argv['--ngrex-patterns'] == 'FILE'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True
    assert argv['--sort-anns'] is True

    cmd = 'negbio -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--sort-anns'] is False
    assert argv['--regex-patterns'] == '~/.medtext/resources/patterns/regex_patterns.yml'
    assert argv['--ngrex-patterns'] == '~/.medtext/resources/patterns/ngrex_patterns.yml'


def test_prompt_download():
    cmd = 'download prompt --model FILE --model-dir DIR'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['negbio'] is False
    assert argv['prompt'] is True
    assert argv['--model'] == 'FILE'
    assert argv['--model-dir'] == 'DIR'

    cmd = 'download prompt'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--model'] == '~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint.zip'
    assert argv['--model-dir'] == '~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint'


def test_prompt():
    cmd = 'prompt --model-dir DIR --overwrite -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['negbio'] is False
    assert argv['download'] is False
    assert argv['prompt'] is True
    assert argv['--model-dir'] == 'DIR'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'prompt -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--model-dir'] == '~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint'
