import mysql.connector
import os

from core.domain.validation_models import Transaction


class MySQLTransactions:
    """
    Adapter responsible for writing validated transaction to MySQL db for persistent storage.
    """

    def __init__(self):
        self.config = {
            'user': 'root',
            'password': os.getenv('MYSQL_ROOT_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'host': os.getenv('MYSQL_HOST')
        }

    def save_batch(self, transactions: list[Transaction]):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        query = """
                    INSERT INTO transactions (
                        step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, 
                        nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

        # Maps objects to raw database tuples
        values = [
            (
                tx.step, tx.type, float(tx.amount), tx.nameOrig, float(tx.oldbalanceOrg),
                float(tx.newbalanceOrig), tx.nameDest, float(tx.oldbalanceDest),
                float(tx.newbalanceDest), tx.isFraud, tx.isFlaggedFraud
            )
            for tx in transactions
        ]

        cursor.executemany(query, values)
        conn.commit()
        cursor.close()
        conn.close()



    def get_sample_transactions() -> dict:

        # connection =

        df = pd.read_sql('SELECT * FROM transactions LIMIT 100', con = connection)

        json_output = df.to_dict(orient='records', data_format='iso')

        return json_output

    def get_transactions_above_amount(value: float) -> dict:

        df = pd.read_sql(f'SELECT * FROM transactions WHERE amount >= {value} LIMIT 1000')

        json_output = df.to_dict(orient='records', data_format='iso')

        return json_output

    def get_transactions_orig_account(account_id: str) -> dict:


        df = pd.read_sql(f"SELECT * FROM transactions WHERE nameOrig = '{account_id}' LIMIT 1000")

        json_output = df.to_dict(orient='records', data_format='iso')

        return json_output

    def get_transactions_dest_account(account_id: str) -> dict:
        df = pd.read_sql(f"SELECT * FROM transactions WHERE nameDest = '{account_id}' LIMIT 1000")

        json_output = df.to_dict(orient='records', data_format='iso')

        return json_output

#TODO: Add get for fraudulent tx