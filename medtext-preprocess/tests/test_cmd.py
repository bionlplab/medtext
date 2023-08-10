import docopt
from medtext_preprocess.cmd import preprocess as cli


def test_download_spacy():
    cmd = 'download spacy --spacy-model NAME'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['spacy'] is True
    assert argv['stanza'] is False
    assert argv['--spacy-model'] == 'NAME'

    cmd = 'download spacy'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--spacy-model'] == 'en_core_web_sm'


def test_download_stanza():
    cmd = 'download stanza'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['stanza'] is True
    assert argv['spacy'] is False


def test_stanza():
    cmd = 'stanza -i FILE -o FILE --overwrite'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['stanza'] is True
    assert argv['spacy'] is False
    assert argv['download'] is False
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'stanza -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False


def test_spacy():
    cmd = 'spacy --overwrite --spacy-model NAME -i FILE -o FILE'
    try:
        argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    except Exception as e:
        print(e)
    assert argv['spacy'] is True
    assert argv['stanza'] is False
    assert argv['download'] is False
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True
    assert argv['--spacy-model'] == 'NAME'

    cmd = 'spacy -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--spacy-model'] == 'en_core_web_sm'
