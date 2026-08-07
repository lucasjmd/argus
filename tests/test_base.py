import itertools

import pytest

from core.adapters.ingestors import BatchIngestor
from core.domain.base import BaseIngestor

HEADER_SAMPLE = (
    'step,type,amount,nameOrig,oldbalanceOrg,newbalanceOrig,nameDest,oldbalanceDest,newbalanceDest,\
isFraud,isFlaggedFraud'
)
ROW_SAMPLE_1 = '1,PAYMENT,9839.64,C1231006815,170136.0,160296.36,M1979787155,0.0,0.0,0,0'


@pytest.fixture
def csv_file_create(tmp_path):
    """
    Generates temporary CSV files with given content.
    """

    def _create_csv(content: str) -> str:
        file_path = tmp_path / 'test_tx_data.csv'
        file_path.write_text(content, encoding='utf-8')
        return file_path

    return _create_csv


## UNIT TESTS


class TestBatchLogic:
    """
    Test CSV batch ingestion logic.
    """

    def test_instantiate_csvingestor(self):
        """
        Ensures BatchIngestor initialises with a valid filepath
        """
        ingestor = BatchIngestor('dummy_path.csv')
        assert ingestor.data_source == 'dummy_path.csv'

    def test_instant_csvingestor_wrongtype(self):
        """
        Ensures passing a non-string arg raises error
        """
        with pytest.raises((TypeError, AttributeError)), BatchIngestor(1.5, throttle=False) as data:
            list(data.get_transactions())

    def test_empty_batch_data(self, csv_file_create):
        """
        Ensures CSV with only header row yields zero transactions.
        """
        csv_path = csv_file_create(HEADER_SAMPLE + '\n')

        with BatchIngestor(csv_path, throttle=False) as data:
            results = list(data.get_transactions())

        assert len(results) == 0

    def test_csv_ingestor_close(self, csv_file_create):
        """
        Assert that underlying csv file is closed upon exiting
        """
        csv_path = csv_file_create(f'{HEADER_SAMPLE}\n{ROW_SAMPLE_1}')

        with BatchIngestor(csv_path, throttle=False) as data:
            for row in data.get_transactions():
                pass

        assert data.file_handle.closed

    def test_batch_ingestor_headers(self, csv_file_create):
        """
        Checks that rows are correctly matched with header keys in dict
        """
        csv_path = csv_file_create(f'{HEADER_SAMPLE}\n{ROW_SAMPLE_1}')

        with BatchIngestor(csv_path, throttle=False) as data:
            results = list(itertools.islice(data.get_transactions(), 2))

        assert len(results) == 1
        assert results[0]['type'] == 'PAYMENT'
        assert results[0]['nameOrig'] == 'C1231006815'


class TestABC:
    """
    Checks interface of abstract base class
    """

    def test_cannot_instantiate_abc(self):
        """
        Tests if BaseIngestor cannot be instantiated directly (without concrete implementation)
        """
        with pytest.raises(TypeError):
            BaseIngestor()
