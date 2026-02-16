import pytest
from sentinel.domain.validation_models import Transaction, pydantic_keyword_dict
from sentinel.domain.base import CSVIngestor, StreamIngestor
import itertools
from pathlib import Path
from decimal import Decimal


header_sample = 'step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest,\
 isFraud, isFlaggedFraud'
row_sample_1 = ['1','PAYMENT','9839.64','C1231006815','170136.0','160296.36','M1979787155','0.0','0.0','0,0']
row_sample_2 = ['2','TRANSFER','1234.56','C840083671','1234567.1','89101112.13','M408069119','1.0','0.2','3','4']

PAYSIM_DIR = '/home/lucas/github/argus/data'
base_dir = Path(PAYSIM_DIR)
filestring = Path('paysim_dataset.csv')
full_path = base_dir / filestring


def test_simple_row_pass():
    with CSVIngestor(full_path) as data:
        results = list(itertools.islice(data.get_transactions(), 1))

        i = 0
        for key in pydantic_keyword_dict.keys():
            pydantic_keyword_dict[key] = results[0][i]
            i += 1

    tx = Transaction(**pydantic_keyword_dict)


    assert isinstance(tx.step, int)
    assert isinstance(tx.type, str)
    assert isinstance(tx.amount, Decimal)
    assert isinstance(tx.nameOrig, str)
    assert isinstance(tx.oldbalanceOrg, Decimal)
    assert isinstance(tx.newbalanceOrig, Decimal)
    assert isinstance(tx.nameDest, str)
    assert isinstance(tx.oldbalanceDest, Decimal)
    assert isinstance(tx.newbalanceDest, Decimal)
    assert isinstance(tx.isFraud, int)
    assert isinstance(tx.isFlaggedFraud, int)
