from pathlib import Path
from typing import Tuple

import bioc
import pytest

from medtext_neg.models.prompt.neg_prompt import BioCNegPrompt
from medtext_neg.models.rules.neg import NegRegexPatterns
from medtext_neg.models.constants import UNCERTAINTY, NEGATION

# negation = Resource_Dir / 'patterns/regex_negation.yml'
# uncertainty_pre_neg = Resource_Dir / 'patterns/regex_uncertainty_pre_negation.yml'
# uncertainty_post_neg = Resource_Dir / 'patterns/regex_uncertainty_post_negation.yml'
# double_neg = Resource_Dir / 'patterns/regex_double_negation.yml'


@pytest.fixture
def neg_actor():
    model_dir = Path.home() / '.medtext/resources/medtext_neg_prompt/models/negation_detection_model_checkpoint'
    neg_actor = BioCNegPrompt(pretrained_model_dir=model_dir)
    return neg_actor


def _get(text, concept_start, concept_end) -> Tuple[bioc.BioCPassage, bioc.BioCAnnotation]:
    passage = bioc.BioCPassage.of_text(text, 0)
    ann = bioc.BioCAnnotation()
    ann.id = 0
    ann.text = text[concept_start:concept_end]
    ann.add_location(bioc.BioCLocation(concept_start, concept_end))
    passage.add_annotation(ann)
    return passage, ann


def test_uncertainty(neg_actor):
    passage, ann = _get('Effusion is possible.', 0, 8)
    neg_actor.process_passage(passage)
    assert ann.infons[UNCERTAINTY]

    passage, ann = _get('Cannot exclude effusion', 15, 23)
    neg_actor.process_passage(passage)
    assert ann.infons[UNCERTAINTY]


def test_neg(neg_actor):
    passage, ann = _get('No evidence to rule out effusion.', 24, 32)
    neg_actor.process_passage(passage)
    print(passage)
    assert ann.infons[NEGATION], passage

    passage, ann = _get('No effusion is seen', 3, 11)
    neg_actor.process_passage(passage)
    assert ann.infons[NEGATION]

