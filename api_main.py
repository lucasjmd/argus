from fastapi import FastAPI, HTTPException
from src.core.adapters.databases import MySQLTransactions
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()
db = MySQLTransactions()

@app.get('/')
def root():
    return {'Hello': 'World!'}

@app.get('/transactions')
def get_txs_json(page: int=1, limit: int=50) -> list:

    return db.get_transactions(page, limit)

@app.get('/transactions/amount/{value}')
def get_tx_gte_amount_json(value: float) -> list:

    return db.get_transactions_above_amount(value)

@app.get('/transactions/orig/{account_id}')
def get_tx_orig_account_json(account_id: str) -> list:

    return db.get_transactions_orig_account(account_id)

@app.get('/transactions/dest/{account_id}')
def get_tx_dest_account_json(account_id: str) -> list:
    return db.get_transactions_dest_account(account_id)

@app.get('/transactions/summary/{account_id}')
def get_sum_account_json(account_id: str) -> dict:
    txs = db.get_transactions_orig_account(account_id)

    if not txs:
        raise HTTPException(status_code=404, detail='Account not found or has not history.')

    total_count = len(txs)
    total_transfer = sum(tx['amount'] for tx in txs)
    avg_value = total_transfer / total_count if total_count > 0 else 0

    return {
        'account_id': account_id,
        'total_transaction_count': total_count,
        'metrics': {
            'total_transfer': round(total_transfer, 2),
            'avg_tx_value': round(avg_value, 2)
        },
        'recent_transactions': txs[:100]
    }

#TODO: Add get route for fraudulent tx