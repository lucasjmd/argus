from abc import ABC, abstractmethod


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






