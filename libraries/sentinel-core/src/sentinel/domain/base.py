from abc import ABC, abstractmethod
from typing import Iterator
from os import getcwd
from sys import path
import csv
import time

PAYSIM_DIR = path[1]

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
    def __exit__(self):
        pass


class CSVIngestor(BaseIngestor):

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def __enter__(self):
        print("Connecting to CSV file...")
        self.file_obj = open(f'{PAYSIM_DIR}/{self.csv_file}', 'r')
        self.reader_obj = csv.reader(self.file_obj)
        return self.reader_obj

    # def get_transactions(self):
    #     for _ in self.reader_obj:
    #         return _

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is StopIteration:
            print('Reached the end of the database.')
            return True
        else:
            return False

        self.reader_obj.close()

        print("Closing down connection to CSV file...")


# csvingestor_object = CSVIngestor('paysim_dataset.csv')

# with csvingestor_object as transaction:
#     print(transaction)

start = time.time()
with CSVIngestor('paysim_dataset.csv') as dataset:
    for transaction in dataset:
       print(transaction)
end = time.time()

length = end - start
print(f'Iterating through the CSV file took {length} seconds.')







