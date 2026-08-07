import os

import mysql.connector
import pandas as pd

from core.domain.validation_models import Transaction


class MySQLTransactions:
    """
    Adapter responsible for writing validated transactions, reading transactions for api endpoints
    and writing/reading api user credentials to MySQL db for persistent storage.
    """

    def __init__(self):
        """
        Initialises database connection credentials from env variables.
        """
        self.config = {
            'user': 'root',
            'password': os.getenv('MYSQL_ROOT_PASSWORD'),
            'database': os.getenv('MYSQL_DATABASE'),
            'host': os.getenv('MYSQL_HOST'),
        }

    def save_batch(self, transactions: list[Transaction]) -> None:
        """
        Bulk inserts a list of validated transactions into the db.
        :param transactions: List of validated Transaction objects
        """
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
                tx.step,
                tx.type,
                tx.amount,
                tx.nameOrig,
                float(tx.oldbalanceOrg),
                float(tx.newbalanceOrig),
                tx.nameDest,
                float(tx.oldbalanceDest),
                float(tx.newbalanceDest),
                tx.isFraud,
                tx.isFlaggedFraud,
            )
            for tx in transactions
        ]

        cursor.executemany(
            query, values
        )  # batch flushing to db, avoids individual network traffic per tx
        conn.commit()
        cursor.close()
        conn.close()

    def get_transactions(self, page: int = 1, limit: int = 50) -> list:
        """
        Retrieves paginated list of transaction records.

        :param page: Page number to fetch (1-indexed)
        :param limit: Maximum number of transactions per page
        :return: A list of transaction records represented as dictionaries
        """

        offset = (page - 1) * limit

        connection = mysql.connector.connect(**self.config)

        query = """
            SELECT amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest
            FROM transactions
            LIMIT %s
            OFFSET %s
        """

        df = pd.read_sql(query, con=connection, params=[limit, offset])

        connection.close()

        return df.to_dict(orient='records')

    def get_transactions_above_amount(self, value: float) -> list:
        """
        Fetches all transactions where the transfer amount is greater than or equal to a taret value.

        :param value: Minimum transaction amount
        :return: A list of transaction records as dicts
        """

        connection = mysql.connector.connect(**self.config)

        query = 'SELECT * FROM transactions WHERE amount >= %s'

        df = pd.read_sql(query, con=connection, params=[value])

        connection.close()

        return df.to_dict(orient='records')

    def get_transactions_orig_account(self, account_id: str) -> list:
        """
        Retrieves all transactions originating from a specific account id.

        :param account_id: Originating account identifier
        :return: A list of transaction records as dicts
        """

        connection = mysql.connector.connect(**self.config)
        query = 'SELECT * FROM transactions WHERE nameOrig = %s'
        df = pd.read_sql(query, con=connection, params=[account_id])
        connection.close()
        return df.to_dict(orient='records')

    def get_transactions_dest_account(self, account_id: str) -> list:
        """
        Retrieves all transactions sent to a specific target account Id

        :param account_id: Destination account identifier
        :return: List of transaction records as dictionaries
        """

        connection = mysql.connector.connect(**self.config)
        query = 'SELECT * FROM transactions WHERE nameDest = %s'
        df = pd.read_sql(query, con=connection, params=[account_id])
        connection.close()

        return df.to_dict(orient='records')

    def create_user(self, username: str, hashed_password: str) -> None:
        """
        Inserts a new api user and their hashed password into the db

        :param username: username of the user
        :param hashed_password: the hashed password string
        :return:
        """

        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()
        query = 'INSERT IGNORE INTO api_users (username, hashed_password) VALUES (%s, %s);'

        cursor.execute(query, (username, hashed_password))
        connection.commit()

        cursor.close()
        connection.close()

    def get_user_by_username(self, username: str) -> str:
        """
        Fetches the stored hashed password for a given username.

        :param username: The username to look for
        :return: The hashed password string
        """

        connection = mysql.connector.connect(**self.config)
        cursor = connection.cursor()

        query = 'SELECT hashed_password FROM api_users WHERE username = %s'

        cursor.execute(query, (username,))

        row = cursor.fetchone()

        cursor.close()
        connection.close()

        if row:
            return row[0]

        return None
