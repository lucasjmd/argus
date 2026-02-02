import pytest
from sentinel.domain.base import BaseIngestor, CSVIngestor, stream_simulator

def test_cannot_instantiate_abc():
    with pytest.raises(TypeError) as e:
        BaseIngestor()

def test_instantiate_csvingestor():
    CSVIngestor(1)

def test_stream_sim_type_raise():
    with pytest.raises(TypeError) as e:
        generator_obj = stream_simulator('test.xlsx')
        next(generator_obj)