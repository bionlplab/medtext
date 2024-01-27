from medtext_secsplit.models.section_split_regex import BioCSectionSplitterRegex, combine_patterns


def test_section_split_regex(collection, cxr_section_titles):
    pattern = combine_patterns(cxr_section_titles)
    splitter = BioCSectionSplitterRegex(pattern)
    splitter.process_collection(collection)
    document = collection.documents[0]
    assert len(document.passages) == 4
    assert len(document.annotations) == 2
    assert document.annotations[0].text == 'findings:'
    assert document.annotations[1].text == 'impression:'


def test_section_split_regex2(collection, medspacy_section_titles):
    pattern = combine_patterns(medspacy_section_titles)
    splitter = BioCSectionSplitterRegex(pattern)
    splitter.process_collection(collection)
    document = collection.documents[0]
    assert len(document.passages) == 4
    assert len(document.annotations) == 2
    assert document.annotations[0].text == 'findings:'
    assert document.annotations[1].text == 'impression:'
