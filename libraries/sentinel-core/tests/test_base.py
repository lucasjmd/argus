import pytest
from sentinel.domain.base import BaseIngestor, CSVIngestor, stream_simulator, StreamIngestor
from pathlib import Path

def test_cannot_instantiate_abc():
    with pytest.raises(TypeError) as e:
        BaseIngestor()

def test_instantiate_csvingestor():
    CSVIngestor(1)

def test_stream_sim_type_raise():
    with pytest.raises(TypeError) as e:
        generator_obj = stream_simulator('test.xlsx')
        next(generator_obj)

def test_streamingestor_type_raise():
    with pytest.raises(TypeError):
        stream = StreamIngestor('test.xlsx')
        next(stream)

def test_stream_sim_data_read(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text('1, PAYMENT, 9839.64, C1231006815, 170136.0, 160296.36, M1979787155, 0.0, 0.0, 0, 0')

    gen_obj = stream_simulator(str(test_filestring))

    row_data = next(gen_obj)
    assert row_data == ['1, PAYMENT, 9839.64, C1231006815, 170136.0, 160296.36, M1979787155, 0.0, 0.0, 0, 0']

