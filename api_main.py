from fastapi import FastAPI, HTTPException
from src.core.adapters.databases import MySQLTransactions

app = FastAPI()
db = MySQLTransactions()

@app.get('/')
def root():
    return {'Hello': 'World!'}

@app.get('/transactions')
def get_sample_tx_json() -> list:

    return db.get_sample_transactions()

@app.get('/transactions/amount/{value}')
def get_tx_gte_amount_json(value: float) -> list:

    return db.get_transactions_above_amount(value)

@app.get('/transactions/orig/{account_id}')
def get_tx_orig_account_json(account_id: str) -> list:

    return db.get_transactions_orig_account(account_id)

@app.get('/transactions/dest/{account_id}')
def get_tx_dest_account_json(account_id: str) -> list:
    return db.get_transactions_dest_account(account_id)

#TODO: Add get route for fraudulent tx