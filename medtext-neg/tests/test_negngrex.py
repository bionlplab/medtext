from typing import Tuple

import bioc
import pytest

from medtext_neg.models.rules.neg import NegGrexPatterns
from medtext_neg.models.constants import NEGATION, UNCERTAINTY
from medtext_parse.models.tree2dep import BioCPtb2DepConverter

# negation = Resource_Dir / 'patterns/ngrex_negation.yml'
# uncertainty_pre_neg = Resource_Dir / 'patterns/ngrex_uncertainty_pre_negation.yml'
# uncertainty_post_neg = Resource_Dir / 'patterns/ngrex_uncertainty_post_negation.yml'
# double_neg = Resource_Dir / 'patterns/ngrex_double_negation.yml'


converter = BioCPtb2DepConverter()


@pytest.fixture
def negregex(resource_dir):
    ngrex_patterns = resource_dir / 'patterns/ngrex_patterns.yml'
    negregex = NegGrexPatterns()
    negregex.load_yml2(ngrex_patterns)
    return negregex


def _get(text, tree, concept_start, concept_end) -> Tuple[bioc.BioCPassage, bioc.BioCAnnotation]:
    sentence = bioc.BioCSentence.of_text(text, 0)
    sentence.infons['parse_tree'] = tree
    converter.process_sentence(sentence, '0')

    ann = bioc.BioCAnnotation()
    ann.id = 0
    ann.text = text[concept_start:concept_end]
    ann.add_location(bioc.BioCLocation(concept_start, concept_end))

    passage = bioc.BioCPassage.of_sentences(sentence)

    return passage, ann


def test_uncertainty_pre_neg(negregex):
    passage, ann = _get('No new effusion.', '(ROOT (NP (DT No) (JJ new) (NN effusion) (. .)))', 7, 15)
    assertion = negregex.assert_(passage, ann, '0')
    m = assertion.assert_uncertainty_pre_neg()
    assert m
    assert ann.infons[UNCERTAINTY]
    assert 'ngrex_uncertainty_pre_neg_pattern_id' in ann.infons


def test_uncertainty_post_neg(negregex):
    passage, ann = _get('Possible effusion.', '(ROOT (NP (JJ Possible) (NN effusion) (. .)))', 9, 17)
    assertion = negregex.assert_(passage, ann, '0')
    m = assertion.assert_uncertainty_post_neg()
    assert m
    assert ann.infons[UNCERTAINTY]
    assert 'ngrex_uncertainty_post_neg_pattern_id' in ann.infons


def test_neg(negregex):
    tree = """"
        (ROOT
          (S
            (NP
              (NP (NNP Effusion))
              (PP (IN from)
                (NP (DT the) (JJ right) (NN arm))))
            (VP (VBZ has)
              (VP (VBN been)
                (VP (VBN removed))))
            (. .)))
    """
    passage, ann = _get('Effusion from the right arm has been removed.', tree, 0, 8)
    assertion = negregex.assert_(passage, ann, '0')
    m = assertion.assert_neg()
    assert m
    assert ann.infons[NEGATION]
    assert 'ngrex_neg_pattern_id' in ann.infons


# def test_double_neg():
#     tree = """"
#     (ROOT
#       (S
#         (VP (MD Can) (RB not)
#           (VP (VB exclude)
#             (NP (NN effusion))))
#         (. .)))
#     """
#     graph, ann = _get('Cannot exclude effusion.', tree, 15, 23)
#     negregex.setup(graph, ann)
#     m = negregex.match_double_neg()
#     assert m
#     assert ann.infons['uncertainty']
#     assert 'ngrex_double_neg_pattern_id' in ann.infons


# if __name__ == '__main__':
#     test_neg()
