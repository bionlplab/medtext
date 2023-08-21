import docopt
import pytest

from medtext_deid.cmd import deid as cli


def test_download():
    cmd = 'download'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['bert'] is False
    assert argv['philter'] is False


def test_deid():
    cmd = 'philter --overwrite --repl Y -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is False
    assert argv['philter'] is True
    assert argv['bert'] is False
    assert argv['--repl'] == 'Y'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True

    cmd = 'philter -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--repl'] == 'X'
    assert argv['--overwrite'] is False

    cmd = 'bert --overwrite --collection --repl Y -i FILE -o FILE'
    print(cmd.split())
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is False
    assert argv['philter'] is False
    assert argv['bert'] is True
    assert argv['--repl'] == 'Y'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True
    assert argv['--collection'] is True

    cmd = 'bert --overwrite --document --repl Y -i FILE -o FILE'
    print(cmd.split())
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--document'] is True

    cmd = 'bert --overwrite --passage --repl Y -i FILE -o FILE'
    print(cmd.split())
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--passage'] is True

    cmd = 'bert --overwrite --repl Y -i FILE -o FILE'
    print(cmd.split())
    with pytest.raises(SystemExit):
        docopt.docopt(cli.__doc__, argv=cmd.split())