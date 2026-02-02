from abc import ABC, abstractmethod
from typing import Iterator
from os import getcwd
from sys import path
import csv
import time

PAYSIM_DIR = '/home/lucas/github/argus/data/'


class BaseIngestor(ABC):
    """
    Abstract base class for ingesting transaction data in various forms.

    This is the base class for various database connection subclasses.
    It is both set up as a context manager and an iterator, as well as having other additional
    methods.

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

    def __init__(self, data_source):
        self.data_source = data_source

    def __enter__(self):
        print("Connecting to batch...")
        self.data_obj = open(f'{PAYSIM_DIR}/{self.data_source}', 'r')
        self.reader_obj = csv.reader(self.data_obj)
        return self

    def get_transactions(self):
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

    def __init__(self, data_source):
        self.data_source = data_source

    def __enter__(self):
        print("Connecting to stream...")
        self.data_obj = open(f'{PAYSIM_DIR}/{self.data_source}', 'r')
        self.reader_obj = csv.reader(self.data_obj)
        return self

    def get_transactions(self):
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


def stream_simulator(data):
    while True:
        data_obj = open(f'{PAYSIM_DIR}/{data}', 'r')
        reader_obj = csv.reader(data_obj)

        for row in reader_obj:
            yield row



if __name__ == '__main__':
    # with CSVIngestor('paysim_dataset.csv') as data:
    #     for transaction in data.get_transactions():
    #         print(transaction)

    stream = stream_simulator('paysim_dataset.csv')

    for tx in stream:
        print(tx)

