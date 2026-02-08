import pytest
from sentinel.domain.base import BaseIngestor, CSVIngestor, stream_simulator, StreamIngestor
from pathlib import Path
import psutil
import itertools

row_sample_1 = '1,PAYMENT,9839.64,C1231006815,170136.0,160296.36,M1979787155,0.0,0.0,0,0'
row_sample_2 = '2,TRANSFER,1234.56,C840083671,1234567.1,89101112.13,M408069119,1.0,0.2,3,4'


## UNIT TESTS

#TODO: Use classes to group similar tests

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

def test_stream_sim_no_source():
    with pytest.raises(ValueError):
        stream = stream_simulator('')
        next(stream)

def test_nonexistant_file_stream_sim():
    with pytest.raises(FileNotFoundError):
        stream = stream_simulator('non_data.csv')
        next(stream)


# Empty data
#TODO: empty data stream test

def test_empty_stream_data(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text('')

    stream = stream_simulator(str(test_filestring))
    next(stream)

def test_empty_batch_data(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text('')

    batch_obj = CSVIngestor(str(test_filestring))

    with CSVIngestor(str(test_filestring)) as data:
        for transaction in data.get_transactions():
            print(transaction)

def test_empty_stream_data(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text('')

    stream = stream_simulator(str(test_filestring))

    with pytest.raises(ValueError):
        results = list(itertools.islice(stream, 1))


# correct closure of files

def test_csv_ingestor_close(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text(row_sample_1)
    test_filestring.write_text(row_sample_1)
    test_filestring.write_text(row_sample_1)

    batch_obj = CSVIngestor(str(test_filestring))

    with batch_obj as data:
        for row in data.get_transactions():
            pass

    assert data.file_obj.closed

# correct loop rows stream sim

def test_stream_sim_loop(tmp_path):
    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text(row_sample_2)
    test_filestring.write_text(row_sample_2)

    stream = stream_simulator(str(test_filestring))
    results = list(itertools.islice(stream, 4))

    assert len(results) == 4
    assert results[0] == results[2]
    assert results[1] == results[3]

# def test_stream_sim_headers(tmp_path):
#
# def test_batch_ingestor_no_headers(tmp_path):

## INTEGRATION TESTS

def test_stream_sim_data_read(tmp_path):

    unit_test_data_dir = tmp_path / 'data'
    unit_test_data_dir.mkdir()
    test_filestring = unit_test_data_dir / 'test_tx_data.csv'
    test_filestring.write_text(row_sample_1)

    gen_obj = stream_simulator(str(test_filestring))

    row_data = next(gen_obj)
    assert row_data == ['1', 'PAYMENT', '9839.64', 'C1231006815', '170136.0', '160296.36', 'M1979787155', '0.0', \
                        '0.0', '0', '0']

    #TODO: batch data read test



