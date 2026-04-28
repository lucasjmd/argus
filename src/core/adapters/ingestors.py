import csv
import itertools
import sys
import time
import mysql.connector

from collections.abc import Generator
from pathlib import Path

from src.core.adapters.stream_simulator import stream_simulator
from src.core.domain.base import BaseIngestor

stream_simulator_dir = Path(__file__).resolve().parents[3] / 'tests'
sys.path.append(str(stream_simulator_dir))

class CSVIngestor(BaseIngestor):
    """
    Concrete ingestor engine class for ingesting 'batch'  transaction data
    coming from a .csv file.

    This concrete version of the BaseIngestor abstract base class specifies
    how batch or static data has to be ingested. It can be used as a context
    manager and offers a graceful file exit. The data is presented to the caller
    via a generator object that can be iterated through.

    Args:
        data_source (str): The csv file representing the batch or static data.
j
    Attributes:
        None

    """

    def __init__(self):
        pass

    def __enter__(self):
        self.config = {
            'user': 'root',
            'password': 'secret',
            'host': 'mysql-db',
            'database': 'paysim'
            }

        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()
        
        return self

    def get_transactions(self):
        """
        Generator that yields each row of the csv.
        It defines no .send method or finishing return statement.

        Yields:
            List[str]: A generator object that can iterate through the rows of
            the batch/static data.
        """
        self.cursor.execute("SELECT * FROM transactions")

        for row in self.cursor:
            yield row

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is StopIteration:
            print('Reached the end of the batch.')
            self.conn.close()
            return True

        self.conn.close()
        print("Encountered an error in reading the batch.")
        return False

class StreamIngestor(BaseIngestor):
    """
    Concrete ingestor engine class for ingesting stream transaction data.

    This concrete version of the BaseIngestor abstract base class specifies how
    stream data has to be ingested. It can be used as a context manager.
    The data is presented to the caller via an infinite generator object that
    can be iterated through.

    Args:
        data_source (str): The connection representing the stream of data.

    Attributes:
        None

    """
    def __init__(self, data_source: str, throttle: bool = True):
        self.data_source    = data_source
        self.throttle       = throttle

    def __enter__(self):
        print("Connecting to stream...")
        # This is until we connect to a real stream
        self.stream_obj = stream_simulator(f'{self.data_source}')

        #Checking if stream has any data.
        try:
            first_value = next(self.stream_obj)
            itertools.chain(first_value, self.stream_obj)
        except StopIteration:
                     print('Stream is empty.')

        return self

    def get_transactions(self) -> Generator[list[str], None, None]:
        """
        Generator that yields each row of a stream of data.
        It defines no .send method or finishing return statement.

        Yields:
            List[str]: A generator object that can iterate through the rows of
            the stream data.
        """
        for row in self.stream_obj:
            if self.throttle:
                time.sleep(0.2)
            yield row

    #TODO: Add a graceful file close down.
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is StopIteration:
            print('The stream has been interrupted.')
            self.stream_obj.close()
            return True

        print("Encountered an error in reading the batch.")
        self.stream_obj.close()
        return False



if __name__ == '__main__':
    with CSVIngestor() as data:
        for transaction in data.get_transactions():
            print(transaction)

    # with StreamIngestor('paysim_dataset.csv', True) as data:
    #     for tx in data.get_transactions():
    #         print(tx)
