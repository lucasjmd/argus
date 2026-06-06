import mysql.connector
import os
import pandas as pd


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



    def get_sample_transactions(self) -> list:

        connection = mysql.connector.connect(**self.config)

        df = pd.read_sql('SELECT * FROM transactions LIMIT 100', con = connection)

        connection.close()

        json_output = df.to_dict(orient='records')

        return json_output

    def get_transactions_above_amount(self, value: float) -> list:

        connection = mysql.connector.connect(**self.config)

        query = 'SELECT * FROM transactions WHERE amount >= %s LIMIT 1000'

        df = pd.read_sql(query, con = connection, params = [value])

        connection.close()

        json_output = df.to_dict(orient='records')

        return json_output

    def get_transactions_orig_account(self, account_id: str) -> list:

        connection = mysql.connector.connect(**self.config)
        query = 'SELECT * FROM transactions WHERE nameOrig = %s LIMIT 1000'
        df = pd.read_sql(query, con = connection, params = [account_id])
        connection.close()
        json_output = df.to_dict(orient='records')

        return json_output

    def get_transactions_dest_account(self, account_id: str) -> list:

        connection = mysql.connector.connect(**self.config)
        query = 'SELECT * FROM transactions WHERE nameDest = %s LIMIT 1000'
        df = pd.read_sql(query, con = connection, params=[account_id])
        connection.close()

        json_output = df.to_dict(orient='records')

        return json_output

#TODO: Add get for fraudulent tx