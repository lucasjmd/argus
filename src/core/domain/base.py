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






