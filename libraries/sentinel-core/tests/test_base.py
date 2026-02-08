import pytest
from sentinel.domain.base import BaseIngestor, CSVIngestor, stream_simulator, StreamIngestor
from pathlib import Path
import psutil

row_content = '1,PAYMENT,9839.64,C1231006815,170136.0,160296.36,M1979787155,0.0,0.0,0,0'

## UNIT TESTS

# Correct instantiation

def test_instantiate_csvingestor():
    CSVIngestor('abc')

def test_instant_csvingestor_wrongtype():
    with pytest.raises(TypeError) as e:
        CSVIngestor(1)

def test_instant_streamsim():
    stream_simulator('abc.csv')

# Incorrect argument type

def test_stream_sim_data_type_raise():
    with pytest.raises(TypeError) as e:
        generator_obj = stream_simulator('test.xlsx')
        next(generator_obj)

def test_streamingestor_type_raise():
    with pytest.raises(TypeError):
        stream = StreamIngestor('test.xlsx')
        next(stream)

def test_cannot_instantiate_abc():
    with pytest.raises(TypeError) as e:
        BaseIngestor()

def test_empty_data(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text('')

    batch_obj = CSVIngestor(str(test_filestring))

    with CSVIngestor(str(test_filestring)) as data:
        for transaction in data.get_transactions():
            print(transaction)

# correct closure of files

def test_csv_ingestor_close(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text(row_content)
    test_filestring.write_text(row_content)
    test_filestring.write_text(row_content)

    batch_obj = CSVIngestor(str(test_filestring))

    with batch_obj as data:
        for row in data.get_transactions():
            pass

    assert data.file_obj.closed




## INTEGRATION TESTS

def test_stream_sim_data_read(tmp_path):

    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text(row_content)

    gen_obj = stream_simulator(str(test_filestring))

    row_data = next(gen_obj)
    assert row_data == ['1', 'PAYMENT', '9839.64', 'C1231006815', '170136.0', '160296.36', 'M1979787155', '0.0', \
                        '0.0', '0', '0']

