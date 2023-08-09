import pytest

from medtext_neg.models import ngrex


def test_compile():
    p = '@'
    with pytest.raises(TypeError):
        ngrex.compile(p)
