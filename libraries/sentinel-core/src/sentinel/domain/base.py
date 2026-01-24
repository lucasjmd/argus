from abc import ABC, abstractmethod
from typing import Iterator
from os import getcwd
from sys import path
import csv

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
        def get_transcations

    @abstractmethod
    def __exit(self):
        pass


class CSVIngestor(BaseIngestor):

    def __init__(self, csv_file):
        self.csv_file = csv_file

    def __enter__(self):
        print("Connecting to CSV file...")
        self.file_obj = open(f'{PAYSIM_DIR}/{self.csv_file}', 'r')
        self.reader_obj = reader(file_obj)

        def get_transactions(self,reader_obj):
            for _ in reader_obj:
                print(_)

    def __exit__(self):
        print("Closing down connection to CSV file...")






