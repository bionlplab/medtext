import docopt
from medtext_secsplit.cmd import split_section as cli


def test_download():
    cmd = 'download --section-titles FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['medspacy'] is False
    assert argv['regex'] is False
    assert argv['--section-titles'] == 'FILE'

    cmd = 'download'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--section-titles'] == '~/.medtext/resources/section_titles.txt'


def test_medspacy():
    cmd = 'medspacy --overwrite -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['medspacy'] is True
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'medspacy -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False


def test_regex():
    cmd = 'regex --overwrite --section-titles FILE -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['regex'] is True
    assert argv['--section-titles'] == 'FILE'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'regex -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--section-titles'] == '~/.medtext/resources/section_titles.txt'
    assert argv['--overwrite'] is False
