from abc import ABC, abstractmethod
from typing import Iterator, Generator
from os import getcwd
from sys import path
import csv
import time
from pathlib import Path

PAYSIM_DIR = '/home/lucas/github/argus/data'

class BaseIngestor(ABC):
    """
    Abstract base class for ingesting transaction data in various forms.

    This is the base class for various database connection subclasses.
    It is meant as a contract that defines the form concrete classes (the specific source ingestors)
    will have to follow. It is also set up to allow it to be used as a custom context manager.

    Args:
        None

    Attributes:
        None

    """

    @abstractmethod
    def __enter__(self):
        pass

    @abstractmethod
    def get_transactions(self):
        pass

    @abstractmethod
    def __exit__(self):
        pass


class CSVIngestor(BaseIngestor):
    """
    Concrete ingestor engine class for ingesting 'batch'  transaction data coming from a .csv file.

    This concrete version of the BaseIngestor abstract base class specifies how batch or static data has to be
    ingested. It can be used as a context manager and offers a graceful file exit. The data is presented to the caller
    via a generator object that can be iterated through.

    Args:
        data_source (str): The csv file representing the batch or static data.

    Attributes:
        None

    """

    def __init__(self, data_source: str):
        self.data_source = data_source

        base_dir = Path(PAYSIM_DIR)
        filestring = Path(data_source)
        self.full_path = base_dir / filestring

    def __enter__(self):
        print("Connecting to batch...")
        self.data_obj = open(f'{self.full_path}', 'r')
        return self

    def get_transactions(self) -> Generator[list[str], None, None]:
        """
        Generator that yields each row of the csv.
        It defines no .send method or finishing return statement.

        Yields:
            List[str]: A generator object that can iterate through the rows of the batch/static data.
        """
        self.reader_obj = csv.reader(self.data_obj)
        for row in self.reader_obj:
            yield row

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is StopIteration:
            print('Reached the end of the batch.')
            self.data_obj.close()
            return True
        else:
            self.data_obj.close()
            print("Encountered an error in reading the batch.")
            return False


class StreamIngestor(BaseIngestor):
    """
    Concrete ingestor engine class for ingesting stream transaction data.

    This concrete version of the BaseIngestor abstract base class specifies how stream data has to be
    ingested. It can be used as a context manager. The data is presented to the caller via an infinite generator
    object that can be iterated through.

    Args:
        data_source (str): The connection representing the stream of data.

    Attributes:
        None

    """
    def __init__(self, data_source: str):
        self.data_source = data_source

    def __enter__(self):
        print("Connecting to stream...")
        self.gen_obj = stream_simulator(f'{self.data_source}')
        return self

    def get_transactions(self) -> Generator[list[str], None, None]:
        """
        Generator that yields each row of a stream of data.
        It defines no .send method or finishing return statement.

        Yields:
            List[str]: A generator object that can iterate through the rows of the stream data.
        """
        for row in self.gen_obj:
            yield row

    #TODO: Add a graceful file close down.
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is StopIteration:
            print('The stream has been interrupted.')
            return True

        else:
            print("Encountered an error in reading the batch.")
            return False


def stream_simulator(data: str) -> Generator[list[str], None, None]:
    """
    Simulates an infinite 'stream' of the data from the csv file by looping through it continuously.
    It yields a generator object and defines no .send method or finishing return statement.

    Args:
        str: The name of the csv file.
    Yields:
        List[str]: A generator object that can iterate continuously through the csv rows.

    """

    base_dir = Path(PAYSIM_DIR)
    filestring = Path(data)
    full_path = base_dir / filestring

    if not data.endswith('.csv'):
        raise TypeError

    else:
        while True:
            data_obj = open(f'{full_path}', 'r')
            reader_obj = csv.reader(data_obj)

            for row in reader_obj:
                yield row

            data_obj.close()



if __name__ == '__main__':
    with CSVIngestor('paysim_dataset.csv') as data:
        for transaction in data.get_transactions():
            print(transaction)

    # with StreamIngestor('paysim_dataset.csv') as data:
    #     for tx in data.get_transactions():
    #         print(tx)

