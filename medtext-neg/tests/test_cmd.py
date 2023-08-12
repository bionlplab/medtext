import docopt
from medtext_neg.cmd import neg as cli


def test_download():
    cmd = 'download --regex-patterns FILE --ngrex-patterns FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['download'] is True
    assert argv['neg'] is False
    assert argv['--regex-patterns'] == 'FILE'
    assert argv['--ngrex-patterns'] == 'FILE'

    cmd = 'download'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--regex-patterns'] == '~/.medtext/resources/patterns/regex_patterns.yml'
    assert argv['--ngrex-patterns'] == '~/.medtext/resources/patterns/ngrex_patterns.yml'


def test_neg():
    cmd = 'neg --regex-patterns FILE --ngrex-patterns FILE --overwrite --sort-anns -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['neg'] is True
    assert argv['download'] is False
    assert argv['--regex-patterns'] == 'FILE'
    assert argv['--ngrex-patterns'] == 'FILE'
    assert argv['-i'] == 'FILE'
    assert argv['-o'] == 'FILE'
    assert argv['--overwrite'] is True
    assert argv['--sort-anns'] is True

    cmd = 'neg -i FILE -o FILE'
    argv = docopt.docopt(cli.__doc__, argv=cmd.split())
    assert argv['--overwrite'] is False
    assert argv['--sort-anns'] is False
    assert argv['--regex-patterns'] == '~/.medtext/resources/patterns/regex_patterns.yml'
    assert argv['--ngrex-patterns'] == '~/.medtext/resources/patterns/ngrex_patterns.yml'
