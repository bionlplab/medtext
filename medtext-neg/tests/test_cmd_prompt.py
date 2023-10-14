import docopt
from medtext_neg.cmd import neg_prompt as cli


def test_download():
    cmd = 'download --model FILE --model-dir DIR'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['neg'] is False
    assert argv['--model'] == 'FILE'
    assert argv['--model-dir'] == 'DIR'

    cmd = 'download'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--model'] == '~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint.zip'
    assert argv['--model-dir'] == '~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint'


def test_neg():
    cmd = 'neg --model-dir DIR --overwrite -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['neg'] is True
    assert argv['download'] is False
    assert argv['--model-dir'] == 'DIR'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'neg -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--model-dir'] == '~/.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint'
