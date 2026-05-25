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

    def save(self, tx: Transaction):
        conn = mysql.connector.connect(**self.config)
        cursor = conn.cursor()

        query = """
                    INSERT INTO transactions (step, type, amount, nameOrig, oldbalanceOrg, newbalanceOrig, nameDest, oldbalanceDest, newbalanceDest, isFraud, isFlaggedFraud)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
        values = (
            tx.step, tx.type, float(tx.amount), tx.nameOrig, float(tx.oldbalanceOrg),
            float(tx.newbalanceOrig), tx.nameDest, float(tx.oldbalanceDest),
            float(tx.newbalanceDest), tx.isFraud, tx.isFlaggedFraud
        )

        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()