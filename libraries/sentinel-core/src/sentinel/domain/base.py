from abc import ABC, abstractmethod
from typing import Iterator

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
    def __exit(self):
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def get_transactions(self) -> Iterator:
        """
        This abstract method allows a source of transaction to be read.

        Args:
            None

        Returns:
            An iterator object consisting of transactions.
        """
        pass

class CSVIngestor(BaseIngestor):






