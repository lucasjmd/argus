from pydantic import BaseModel, condecimal
from decimal import Decimal

# constrained schema for balance-related columns

# Setting a dictionary that matches the columns of the data, for easy keyword argument passing to the Transaction class
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

# Pydantic schema for all balance-related columns
balance_schema = condecimal(
        strict=False,
        ge=0,
        decimal_places=2,
        allow_inf_nan=False,
    )

class Transaction(BaseModel):
    """
    A Pydantic class to check if the incoming rows of paysim transaction data conform to the expected types and values
    per column.
    """
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





