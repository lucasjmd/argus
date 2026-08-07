from decimal import Decimal

import pytest
from pydantic import ValidationError

from core.domain.validation_models import Transaction

# Base dict of valid transaction data used as a template across tests
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


def test_incorrect_account():
    """
    Ensure that invalid orig and dest account formats are caught
    """
    bad_orig = VALID_TEST_TX.copy()
    bad_orig['nameOrig'] = 'X123456789'
    with pytest.raises(ValidationError):
        Transaction(**bad_orig)

    bad_dest = VALID_TEST_TX.copy()
    bad_dest['nameDest'] = 'X123456789'
    with pytest.raises(ValidationError):
        Transaction(**bad_dest)


def test_empty_string():
    """
    Ensure that an empty string in a required text field is caught
    """
    bad_data = VALID_TEST_TX.copy()
    bad_data['type'] = ''
    with pytest.raises(ValidationError):
        Transaction(**bad_data)


def test_missing_field():
    """
    Ensure that None for a required field is caught
    """
    bad_data = VALID_TEST_TX.copy()
    bad_data['oldbalanceOrg'] = None
    with pytest.raises(ValidationError):
        Transaction(**bad_data)


def test_incorrect_type():
    """
    Check that passing a incorrect type is caught
    """
    bad_data = VALID_TEST_TX.copy()
    bad_data['step'] = 'shouldBeInt'
    with pytest.raises(ValidationError):
        Transaction(**bad_data)


def test_simple_row_pass():
    """
    Ensure that a valid dict is correctly turned into a Transaction instance with expected types
    """
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
