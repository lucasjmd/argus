import csv
import itertools
import time

from collections.abc import Generator
from core.domain.base import BaseIngestor

class BatchIngestor(BaseIngestor):
    """
    Concrete ingestor engine class for ingesting 'batch' transaction data coming from a CSV.

    This concrete version of the BaseIngestor abstract base class specifies
    how batch or static data has to be ingested. It can be used as a context
    manager and offers a graceful file exit. The data is presented to the caller
    via a generator object that can be iterated through.

    Args:
        None
    Attributes:
        None

    """

    def __init__(self, data_source: str, throttle: bool = True):
        self.data_source = data_source
        self.throttle = throttle
        self.file_handle = None
        self.reader = None

    def __enter__(self):
        """
        Allows transaction data to be accessed via a context manager. 
        Sets the parameters to be passed to the terminal/MySQL shell.
        """
        print('Connecting to data source...')
        try:
            self.file_handle = open(self.data_source, mode='r', encoding='utf-8')
        except FileNotFoundError:
            print('Could not data source file.')
            raise

        self.reader = csv.DictReader(self.file_handle)
        return self

    def get_transactions(self):
        """
        Generator that yields each row of the transactions table from a mysql db.
        It defines no .send method or finishing return statement.


        Yields:
            A generator object that can iterate through the rows of
            the batch/static data.
        """
        for row in self.reader:
            if self.throttle:
                time.sleep(0.1)

            yield row

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file_handle:
            print('Closing connection to CSV source.')
            self.file_handle.close()

        if exc_type and exc_type is not StopIteration:
            print(f'Reading file interrupted due to error: {exc_value}')
            return False


if __name__ == '__main__':
    csv_path = 'paysim_data/paysim_dataset.csv'
    with BatchIngestor(data_source=csv_path, throttle=True) as batch:
        for tx in batch.get_transactions():
            print(tx)

