from pydantic import BaseModel, condecimal
from decimal import Decimal

# constrained schema for balance-related columns
balance_schema = condecimal(
        strict=True,
        ge=0,
        decimal_places=2,
        allow_inf_nan=False,
    )

class Transaction(BaseModel):
    step: int
    type: str
    amount: condecimal(
        strict=True,
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




