import pytest
from sentinel.domain.validation_models import Transaction, pydantic_keyword_dict
from sentinel.domain.base import CSVIngestor, StreamIngestor
import itertools
from pathlib import Path
from decimal import Decimal


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
