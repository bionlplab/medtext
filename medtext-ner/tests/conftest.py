from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def resource_dir():
    return Path(__file__).parent / '../../medtext-resources/'

