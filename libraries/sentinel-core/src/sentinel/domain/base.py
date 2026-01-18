from abc import ABC, abstractmethod

class BaseIngestor(ABC):
    """
    Abstract base class for ingesting transaction data in various forms.

    This is the base class for various planned forms of data ingestion classes, e.g.: complete CSV's, Kafka streams,
    SQL databases, etc. It defines  abstract methods that requires concrete classes to specify further.

    Args:
        None

    Returns:
    """
    @abstractmethod
    def read_file