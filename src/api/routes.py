from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from src.api.auth.authenticator import validate_user
from src.api.auth.jwt_token_engine import create_jwt
from src.api.auth.passwords import hash_user_password, validate_password_attempt
from src.core.adapters.databases import MySQLTransactions

# creating main web application
app = FastAPI()

# database connection instance for api routes
db = MySQLTransactions()


class RegisterSchema(BaseModel):
    """
    Pydantic schema defining structure expected when register endpoint is called
    """

    username: str
    password: str


@app.get('/')
def root():
    """
    Health check and root welcome point
    """
    return {'Hello': 'World!'}


@app.get('/transactions')
def get_txs_json(page: int = 1, limit: int = 50, user_id: str = Depends(validate_user)) -> list:
    """
    Fetches a paginated list of all transactions.
    Requires a token authentication (aka protected route)
    """
    return db.get_transactions(page, limit)


@app.get('/transactions/amount/{value}')
def get_tx_gte_amount_json(value: float, user_id: str = Depends(validate_user)) -> list:
    """
    Fetch transactions where the transferred amount is larger than or equal to target value
    """
    return db.get_transactions_above_amount(value)


@app.get('/transactions/orig/{account_id}')
def get_tx_orig_account_json(account_id: str, user_id: str = Depends(validate_user)) -> list:
    """
    Fetch outgoing transactions originating from a specified account Id
    """
    return db.get_transactions_orig_account(account_id)


@app.get('/transactions/dest/{account_id}')
def get_tx_dest_account_json(account_id: str, user_id: str = Depends(validate_user)) -> list:
    """
    Fetch incoming transactions destined for a specified account Id
    """
    return db.get_transactions_dest_account(account_id)


@app.get('/transactions/summary/{account_id}')
def get_sum_account_json(account_id: str, user_id: str = Depends(validate_user)) -> dict:
    """
    Calculates summary stats and returns recent history for a given originating account id
    """
    txs = db.get_transactions_orig_account(account_id)

    if not txs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Account not found or has not history.'
        )

    total_count = len(txs)
    total_transfer = sum(tx['amount'] for tx in txs)
    avg_value = total_transfer / total_count if total_count > 0 else 0

    return {
        'account_id': account_id,
        'total_transaction_count': total_count,
        'metrics': {
            'total_transfer': round(total_transfer, 2),
            'avg_tx_value': round(avg_value, 2),
        },
        'recent_transactions': txs[:100],  # up to 100 most recent transactions returned
    }


@app.post('/register', status_code=status.HTTP_201_CREATED)
def register_user(register_data: RegisterSchema):
    """
    Register a new user with a unique username and hashed password.
    """
    user_exists = db.get_user_by_username(register_data.username)
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Username already registred!'
        )

    hashed_password = hash_user_password(register_data.password)
    db.create_user(register_data.username, hashed_password)
    return {'message': 'User succesfully registered!'}


@app.post('/login')
def user_login(login_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate user credentials and issue a signed JWT bearer access token

    """
    hashed_password = db.get_user_by_username(login_data.username)

    if not hashed_password or not validate_password_attempt(login_data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password!'
        )

    access_token = create_jwt(data={'sub': login_data.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
