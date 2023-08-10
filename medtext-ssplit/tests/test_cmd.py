import docopt
import pytest
from docopt import DocoptExit

from medtext_ssplit.cmd import ssplit as cli


def test_download():
    cmd = 'download'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['ssplit'] is False


def test_all():
    cmd = 'ssplit -i FILE -o FILE --newline --overwrite'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is False
    assert argv['ssplit'] is True
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True
    assert argv['--newline'] is True

    cmd = 'ssplit -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--newline'] is False


def test_exception():
    cmd = 'ssplit'
    with pytest.raises(DocoptExit):
        docopt.docopt(cli.__doc__, argv=cmd.split())

