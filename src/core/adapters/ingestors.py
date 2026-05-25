import csv
import itertools
import sys
import time

from collections.abc import Generator
from pathlib import Path

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
    csv_path = 'paysim_data/paysim_dataset.csv'
    with BatchIngestor(data_source=csv_path, throttle=True) as batch:
        for tx in batch.get_transactions():
            print(tx)

    # with StreamIngestor('paysim_dataset.csv', True) as data:
    #     for tx in data.get_transactions():
    #         print(tx)
