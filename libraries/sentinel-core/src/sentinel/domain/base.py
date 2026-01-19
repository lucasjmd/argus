from abc import ABC, abstractmethod
from typing import Iterator

class BaseIngestor(ABC):
    """
    Abstract base class for ingesting transaction data in various forms.

    This is the base class for various planned forms of data ingestion classes, e.g.: complete CSV's, Kafka streams,
    SQL databases, etc. It defines  abstract methods that requires concrete classes to specify further.

    Args:
        None

    Attributes:
        None
    """
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






