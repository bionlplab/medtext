import medspacy
from medtext_secsplit.models.section_split_medspacy import BioCSectionSplitterMedSpacy


def test_section_split_medspacy(collection):
    nlp = medspacy.load()
    nlp.add_pipe("medspacy_sectionizer")
    splitter = BioCSectionSplitterMedSpacy(nlp)
    splitter.process_collection(collection)
    document = collection.documents[0]
    assert len(document.passages) == 4
    assert len(document.annotations) == 2
    assert document.annotations[0].text == 'findings:'
    assert document.annotations[1].text == 'impression:'

