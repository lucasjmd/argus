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



    def get_transactions(self, page, limit) -> list:

        offset = (page - 1) * limit

        connection = mysql.connector.connect(**self.config)

        query = """
            SELECT amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest
            FROM transactions
            LIMIT %s
            OFFSET %s
        """

        df = pd.read_sql(query, con = connection, params = [limit, offset])

        connection.close()

        json_output = df.to_dict(orient='records')

        return json_output

    def get_transactions_above_amount(self, value: float) -> list:

        connection = mysql.connector.connect(**self.config)

        query = 'SELECT * FROM transactions WHERE amount >= %s'

        df = pd.read_sql(query, con = connection, params = [value])

        connection.close()

        json_output = df.to_dict(orient='records')

        return json_output

    def get_transactions_orig_account(self, account_id: str) -> list:

        connection = mysql.connector.connect(**self.config)
        query = 'SELECT * FROM transactions WHERE nameOrig = %s'
        df = pd.read_sql(query, con = connection, params = [account_id])
        connection.close()
        json_output = df.to_dict(orient='records')

        return json_output

    def get_transactions_dest_account(self, account_id: str) -> list:

        connection = mysql.connector.connect(**self.config)
        query = 'SELECT * FROM transactions WHERE nameDest = %s'
        df = pd.read_sql(query, con = connection, params=[account_id])
        connection.close()

        json_output = df.to_dict(orient='records')

        return json_output

    def create_user(self, username, hashed_password):

        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        query = 'INSERT IGNORE INTO api_users (username, hashed_password) VALUES (%s, %s);'

        cursor.execute(query, (username, hashed_password))
        connection.commit()

        cursor.close()
        connection.close()

    def get_user_by_username(self, username):

        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()

        query = 'SELECT hashed_password FROM api_users WHERE username = %s'

        cursor.execute(query, (username,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row:
            hashed_password = row[0]
            return hashed_password

        else:
            return None


#TODO: Add get for fraudulent tx