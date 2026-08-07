from abc import ABC, abstractmethod


class BaseIngestor(ABC):
    """
    Abstract base class for ingesting transaction data from various sources (e.g. csv, stream)

    Defines a contract for all ingestor implementations and enforces context manager usage
    """

    @abstractmethod
    def __enter__(self):
        """Opens connections required by the ingestor."""
        pass

    @abstractmethod
    def get_transactions(self):
        """
        Yields transaction records as dictionaries

        :return: A generator yielding transaction data dicts
        """
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Safely closes connections upon exit"""
        pass
