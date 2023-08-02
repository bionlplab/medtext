import bioc

from medtext_commons.base_utils import contains, intersect, is_passage_empty, strip_passage, is_ner


def test_contains():
    assert contains(lambda a: a == 1, [0, 1, 2])
    assert not contains(lambda a: a == 3, [0, 1, 2])
    assert not contains(lambda a: a == 3, [])
    assert not contains(None, [False, False, False])


def test_intersect():
    assert intersect((0, 1), (.5, .9))
    assert not intersect((0, 1), (-1, 0))
    assert intersect((0, 1), (-1, .1))
    assert not intersect((0, 1), (1, 2))
    assert intersect((0, 1), (.9, 2))
    assert intersect((.5, .9), (0, 1))


def test_is_passage_empty():
    p = bioc.BioCPassage()
    p.text = ''
    assert is_passage_empty(p)

    p.text = None
    assert is_passage_empty(p)


def test_strip_passage():
    p = bioc.BioCPassage()
    p.offset = 0
    p.text = 'xxx '
    p = strip_passage(p)
    assert p.offset == 0

    p.text = ' xxx'
    p = strip_passage(p)
    assert p.offset == 1


def test_is_ner():
    ann = bioc.BioCAnnotation()
    assert not is_ner(ann)

    ann.infons['nlp_system'] = 'ner'
    assert is_ner(ann)

