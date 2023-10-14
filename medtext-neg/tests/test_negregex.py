from typing import Tuple

import bioc
import pytest

from medtext_neg.models.rules.neg import NegRegexPatterns
from medtext_neg.models.constants import UNCERTAINTY, NEGATION

# negation = Resource_Dir / 'patterns/regex_negation.yml'
# uncertainty_pre_neg = Resource_Dir / 'patterns/regex_uncertainty_pre_negation.yml'
# uncertainty_post_neg = Resource_Dir / 'patterns/regex_uncertainty_post_negation.yml'
# double_neg = Resource_Dir / 'patterns/regex_double_negation.yml'


@pytest.fixture
def negregex(resource_dir):
    regex_patterns = resource_dir / 'patterns/regex_patterns.yml'
    negregex = NegRegexPatterns()
    negregex.load_yml2(regex_patterns)
    return negregex


def _get(text, concept_start, concept_end) -> Tuple[bioc.BioCPassage, bioc.BioCAnnotation]:
    passage = bioc.BioCPassage.of_text(text, 0)
    ann = bioc.BioCAnnotation()
    ann.id = 0
    ann.text = text[concept_start:concept_end]
    ann.add_location(bioc.BioCLocation(concept_start, concept_end))
    return passage, ann


def test_uncertainty_pre_neg(negregex):
    passage, ann = _get('No evidence to rule out effusion.', 24, 32)
    assertion = negregex.assert_(passage, ann)
    m = assertion.assert_uncertainty_pre_neg()
    assert m
    assert ann.infons[UNCERTAINTY]
    assert 'regex_uncertainty_pre_neg_pattern_id' in ann.infons


def test_uncertainty_post_neg(negregex):
    passage, ann = _get('Effusion is possible.', 0, 8)
    assertion = negregex.assert_(passage, ann)
    m = assertion.assert_uncertainty_post_neg()
    assert m
    assert ann.infons[UNCERTAINTY]
    assert 'regex_uncertainty_post_neg_pattern_id' in ann.infons


def test_neg(negregex):
    passage, ann = _get('No effusion is seen', 3, 11)
    assertion = negregex.assert_(passage, ann)
    m = assertion.assert_neg()
    assert m
    assert ann.infons[NEGATION]
    assert 'regex_neg_pattern_id' in ann.infons


def test_double_neg(negregex):
    passage, ann = _get('Cannot exclude effusion', 15, 23)
    assertion = negregex.assert_(passage, ann)
    m = assertion.assert_double_neg()
    assert m
    assert ann.infons[UNCERTAINTY]
    assert 'regex_double_neg_pattern_id' in ann.infons


# if __name__ == '__main__':
#     test_uncertainty_pre_neg()
#     test_uncertainty_post_neg()
#     test_neg()
#     test_double_neg()
