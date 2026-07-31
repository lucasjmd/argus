from typing import Literal
from pydantic import BaseModel, Field, condecimal

# constrained schema for balance-related columns
# Pydantic schema for all balance-related columns
balance_schema = condecimal(
        strict=False,
        ge=0,
        decimal_places=2,
        allow_inf_nan=False,
    )

class Transaction(BaseModel):
    """
    A Pydantic class to check if the incoming rows of paysim transaction data
    conform to the expected types and values per column.
    """
    step: int
    type: Literal['CASH_IN', 'CASH_OUT', 'DEBIT', 'PAYMENT', 'TRANSFER']
    amount: condecimal(
        strict=False,
        gt=0,
        decimal_places=2,
        allow_inf_nan=False,
    )
    nameOrig: str = Field(pattern=r'^C')
    oldbalanceOrg: balance_schema
    newbalanceOrig: balance_schema
    nameDest: str = Field(pattern=r'^[CM]')
    oldbalanceDest: balance_schema
    newbalanceDest: balance_schema
    isFraud: int
    isFlaggedFraud: int





