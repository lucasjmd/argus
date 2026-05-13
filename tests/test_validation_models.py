import pytest
from pydantic import ValidationError
from core.domain.validation_models import Transaction, pydantic_keyword_dict
from core.adapters.ingestors import BatchIngestor, StreamIngestor
import csv
from pathlib import Path
from decimal import Decimal

# reference to data locally saved as csv to be able to test without having to start mysql docker container
# or messing with networks
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / 'paysim_data' / 'paysim_dataset.csv'

with open(DATA_PATH, mode='r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    first_row = next(reader)

    i = 0

    for key in pydantic_keyword_dict.keys():
        pydantic_keyword_dict[key] = first_row[i]
        i += 1

missing_keyword_dict = pydantic_keyword_dict.copy()
missing_keyword_dict['oldbalanceOrg'] = None

wrongtype_keyword_dict = pydantic_keyword_dict.copy()
wrongtype_keyword_dict['step'] = 'shouldBeInt'

emptystring_keyword_dict = pydantic_keyword_dict.copy()
emptystring_keyword_dict['type'] = ''

def test_incorrect_account():
    with pytest.raises(ValidationError):
        Transaction(nameOrig='X123456789')

    with pytest.raises(ValidationError):
        Transaction(nameDest='X123456789')

def test_empty_string():
    with pytest.raises(ValidationError):
        tx = Transaction(**emptystring_keyword_dict)

def test_missing_field():
    with pytest.raises(ValidationError):
        tx = Transaction(**missing_keyword_dict)

def test_incorrect_type():
    with pytest.raises(ValidationError):
        tx = Transaction(**wrongtype_keyword_dict)

def test_simple_row_pass():
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
