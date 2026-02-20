from abc import ABC, abstractmethod
from typing import Iterator, Generator
from os import getcwd
from sys import path
import csv
from time import sleep
import time
from pathlib import Path
import psutil
import sys
import itertools

stream_simulator_dir = Path(__file__).resolve().parents[3] / 'tests'
sys.path.append(str(stream_simulator_dir))

from stream_simulator import stream_simulator

PAYSIM_DIR = '/home/lucas/github/argus/data'

base_dir = Path(PAYSIM_DIR)
filestring = Path('paysim_dataset.csv')
full_path = base_dir / filestring

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
        self.file_obj = open(f'{self.full_path}', 'r')
        return self

    def get_transactions(self) -> Generator[list[str], None, None]:
        """
        Generator that yields each row of the csv.
        It defines no .send method or finishing return statement.

        Yields:
            List[str]: A generator object that can iterate through the rows of the batch/static data.
        """
        self.batch_obj = csv.reader(self.file_obj)

        # Skip header
        next(self.batch_obj, None)

        for row in self.batch_obj:
            time.sleep(0.2)
            yield row

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is StopIteration:
            print('Reached the end of the batch.')
            self.file_obj.close()
            return True
        else:
            self.file_obj.close()
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
            stream_obj = itertools.chain(first_value, self.stream_obj)
        except StopIteration:
            print('Stream is empty.')

        return self

    def get_transactions(self) -> Generator[list[str], None, None]:
        """
        Generator that yields each row of a stream of data.
        It defines no .send method or finishing return statement.

        Yields:
            List[str]: A generator object that can iterate through the rows of the stream data.
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

        else:
            print("Encountered an error in reading the batch.")
            self.stream_obj.close()
            return False



if __name__ == '__main__':
    with CSVIngestor('paysim_dataset.csv') as data:
        for transaction in data.get_transactions():
            print(transaction)

    # with StreamIngestor('paysim_dataset.csv', True) as data:
    #     for tx in data.get_transactions():
    #         print(tx)





