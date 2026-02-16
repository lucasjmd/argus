from pydantic import BaseModel, condecimal
from decimal import Decimal

# constrained schema for balance-related columns

pydantic_keyword_dict = {
    'step':None,
    'type': None,
    'amount': None,
    'nameOrig': None,
    'oldbalanceOrg': None,
    'newbalanceOrig': None,
    'nameDest': None,
    'oldbalanceDest': None,
    'newbalanceDest': None,
    'isFraud': None,
    'isFlaggedFraud':None,
}

balance_schema = condecimal(
        strict=False,
        ge=0,
        decimal_places=2,
        allow_inf_nan=False,
    )

class Transaction(BaseModel):
    step: int
    type: str
    amount: condecimal(
        strict=False,
        gt=0,
        decimal_places=2,
        allow_inf_nan=False,
    )
    nameOrig: str
    oldbalanceOrg: balance_schema
    newbalanceOrig: balance_schema
    nameDest: str
    oldbalanceDest: balance_schema
    newbalanceDest: balance_schema
    isFraud: int
    isFlaggedFraud: int





