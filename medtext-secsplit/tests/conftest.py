from pathlib import Path

import bioc
import pytest


@pytest.fixture(scope="module")
def resource_dir():
    return Path(__file__).parent / '../../medtext-resources'


@pytest.fixture
def collection():
    text = """findings: pa and lat cxr at 7:34 p.m.. heart and mediastinum are
    stable. lungs are unchanged. air- filled cystic changes. no
    pneumothorax. osseous structures unchanged scoliosis
    impression: stable chest.
    dictating 
    """
    doc = bioc.BioCDocument.of_text(text)
    return bioc.BioCCollection.of_documents(doc)


@pytest.fixture
def cxr_section_titles(resource_dir):
    with open(resource_dir / 'cxr_section_titles.txt') as fp:
        section_titles = [line.strip() for line in fp]
    return section_titles


@pytest.fixture
def medspacy_section_titles(resource_dir):
    with open(resource_dir / 'medspacy_section_titles.txt') as fp:
        section_titles = [line.strip() for line in fp]
    return section_titles
