import pytest
from sentinel.domain.base import BaseIngestor, CSVIngestor

def test_cannot_instantiate_abc():
    with pytest.raises(TypeError) as e:
        BaseIngestor()

def test_instantiate_csvingestor():
    CSVIngestor(1)