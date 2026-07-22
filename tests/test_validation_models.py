import pytest
from pydantic import ValidationError
from core.domain.validation_models import Transaction, pydantic_keyword_dict
from core.adapters.ingestors import BatchIngestor, StreamIngestor
import csv
from pathlib import Path
from decimal import Decimal

# reference to data locally saved as csv to be able to test without having to start mysql docker container
# or messing with networks
VALID_TEST_TX = {
    'step': '1',
    'type': 'PAYMENT',
    'amount': '9839.64',
    'nameOrig': 'C1231006815',
    'oldbalanceOrg': '170136.0',
    'newbalanceOrig': '160296.36',
    'nameDest': 'M1979787155',
    'oldbalanceDest': '0.0',
    'newbalanceDest': '0.0',
    'isFraud': '0',
    'isFlaggedFraud': '0',
}

missing_keyword_dict = pydantic_keyword_dict.copy()
missing_keyword_dict['oldbalanceOrg'] = None

wrongtype_keyword_dict = pydantic_keyword_dict.copy()
wrongtype_keyword_dict['step'] = 'shouldBeInt'

emptystring_keyword_dict = pydantic_keyword_dict.copy()
emptystring_keyword_dict['type'] = ''

def test_incorrect_account():
    bad_orig = VALID_TEST_TX.copy()
    bad_orig['nameOrig'] = 'X123456789'
    with pytest.raises(ValidationError):
        Transaction(**bad_orig)

    bad_dest = VALID_TEST_TX.copy()
    bad_dest['nameDest'] = 'X123456789'
    with pytest.raises(ValidationError):
        Transaction(**bad_dest)

def test_empty_string():
    bad_data = VALID_TEST_TX.copy()
    bad_data['type'] = ''
    with pytest.raises(ValidationError):
        tx = Transaction(**bad_data)

def test_missing_field():
    bad_data = VALID_TEST_TX.copy()
    bad_data['oldbalanceOrg'] = None
    with pytest.raises(ValidationError):
        tx = Transaction(**bad_data)

def test_incorrect_type():
    bad_data = VALID_TEST_TX.copy()
    bad_data['step'] = 'shouldBeInt'
    with pytest.raises(ValidationError):
        tx = Transaction(**bad_data)

def test_simple_row_pass():
    tx = Transaction(**VALID_TEST_TX)

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
