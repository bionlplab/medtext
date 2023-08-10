import docopt
from medtext_ner.cmd import ner as cli


def test_download():
    cmd = 'download --spacy-model NAME'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['spacy'] is False
    assert argv['regex'] is False
    assert argv['--spacy-model'] == 'NAME'

    cmd = 'download'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--spacy-model'] == 'en_core_web_sm'


def test_spacy():
    cmd = 'spacy --overwrite --spacy-model NAME --radlex FILE -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['spacy'] is True
    assert argv['--spacy-model'] == 'NAME'
    assert argv['--radlex'] == 'FILE'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'spacy -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--spacy-model'] == 'en_core_web_sm'
    assert argv['--radlex'] == '.medtext/resources/Radlex4.1.xlsx'


def test_regex():
    cmd = 'regex --overwrite --phrases FILE -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['regex'] is True
    assert argv['--phrases'] == 'FILE'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True
