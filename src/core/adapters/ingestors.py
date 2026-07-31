import csv
import time

from core.domain.base import BaseIngestor

class BatchIngestor(BaseIngestor):
    """
    Concrete ingestor engine class for ingesting 'batch' transaction data coming from a CSV.
    Used as a context manager to safely open and stream CSV records row by row without loading
    the entire file into memory

    Attributes:
        data_source (str): File path to the target CSV file
        throttle (bool): If True: adds a 0.1s pause between yielded rows
        file_handle: The open file stream
        reader: Reader object mapping CSV rows to dicts

    """

    def __init__(self, data_source: str, throttle: bool = True):
        """
        Initializes the CSV batch ingestor configuration

        :param data_source: File path to the CSV
        :param throttle: Whether to delay row iteration or not
        """
        self.data_source = data_source
        self.throttle = throttle
        self.file_handle = None
        self.reader = None

    def __enter__(self):
        """
        Opens the CSV file source and initializes the reader object

        :return: The BatchIngestor context instance
        :raises FileNotFoundError: If the CSV file path does not exist
        """
        print('Connecting to data source...')
        try:
            self.file_handle = open(self.data_source, mode='r', encoding='utf-8')
        except FileNotFoundError:
            print('Could not data source file.')
            raise

        self.reader = csv.DictReader(self.file_handle)
        return self

    def get_transactions(self):
        """
        Generates transaction dictionaries from the opened CSV source

        Yields:
            dict: A dictionary representing a single CSV row, (keys correspond to CSV column names)
        """
        for row in self.reader:
            if self.throttle:
                time.sleep(0.1)

            yield row

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Ensure the CSV file source is safely closed upon exiting"""
        if self.file_handle:
            print('Closing connection to CSV source.')
            self.file_handle.close()

        if exc_type and exc_type is not StopIteration:
            print(f'Reading file interrupted due to error: {exc_value}')
            return False


if __name__ == '__main__':
    csv_path = 'paysim_data/paysim_dataset.csv'
    with BatchIngestor(data_source=csv_path, throttle=True) as batch:
        for tx in batch.get_transactions():
            print(tx)

