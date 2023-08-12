import bioc

from medtext_deid.models.deid_robust_deid import BioCRobustDeid

model = BioCRobustDeid()

TRUE_ENTITIES = [
    [(40, 50), 'DATE', '10/12/1982'],
    [(67, 77), 'DATE', '10/22/1982'],
    [(98, 110), 'PATIENT', 'Jack Reacher'],
    [(112, 114), 'AGE', '54'],
    [(132, 141), 'DATE', '1/21/1928'],
]


TEXT = 'Physician Discharge Summary Admit date: 10/12/1982 Discharge date: 10/22/1982 Patient ' \
       'Information Jack Reacher, 54 y.o. male (DOB = 1/21/1928)'

DEID = 'Physician Discharge Summary Admit date: XXXXXXXXXX Discharge date: XXXXXXXXXX Patient ' \
       'Information XXXXXXXXXXXX, XX y.o. male (DOB = XXXXXXXXX)'

def test_deid():
    entities = model.deidentify_text(TEXT)
    assert len(entities) == 5
    for pred_entity, true_entity in zip(entities, TRUE_ENTITIES):
        assert pred_entity[0] == true_entity[0]
        assert pred_entity[1] == true_entity[1]


def test_sentence():
    sen = bioc.BioCSentence.of_text(TEXT, 100)
    sen = model.process_sentence(sen)
    assert len(sen.annotations) == 5
    for pred_ann, true_entity in zip(sen.annotations, TRUE_ENTITIES):
        assert pred_ann.infons['source_concept'] == true_entity[1]
        assert pred_ann.total_span.offset == true_entity[0][0] + sen.offset
        assert pred_ann.text == true_entity[2]
    assert sen.text == DEID


def test_passage():
    p = bioc.BioCPassage()
    p.offset = 0
    p.add_sentence(bioc.BioCSentence.of_text(TEXT, 0))
    p.add_sentence(bioc.BioCSentence.of_text(TEXT, 100))
    p.add_sentence(bioc.BioCSentence.of_text(TEXT, 150))
    p = model.process_passage(p)
    for sen in p.sentences:
        for pred_ann, true_entity in zip(sen.annotations, TRUE_ENTITIES):
            assert pred_ann.infons['source_concept'] == true_entity[1]
            assert pred_ann.total_span.offset == true_entity[0][0] + sen.offset
            assert pred_ann.text == true_entity[2]
        assert sen.text == DEID
