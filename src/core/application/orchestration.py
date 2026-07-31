import itertools
from pydantic import ValidationError

from core.adapters.ingestors import BatchIngestor
from core.domain.validation_models import Transaction
from core.adapters.databases import MySQLTransactions

class TransactionValidationPipeline:
    """
    Orchestrates the ingestion, validation, and database storage of batch (CSV) transaction data

    Attributes:
        data_source (str): file path to the raw dataset
        batch_size (int): Maximum number of records to process and flush per database write
        writer: Database adapter for bulk writing transactions
    """

    def __init__(self, data_source: str, batch_size: int = 5000):
        """
        Initializes the pipeline config and instantiates database writer

        :param data_source: Path to the raw CSV transaction file
        :param batch_size: Number of transactions per database flush
        """
        self.data_source = data_source
        self.batch_size = batch_size
        self.writer = MySQLTransactions()

    def run_pipeline(self):
        """
        Executes loop: reads CSV rows, validates schema compliance, and flushes valid records to db in chunks.
        """
        with BatchIngestor(data_source = self.data_source, throttle=False) as ingestor:

            raw_gen_obj = ingestor.get_transactions()

            for raw_chunk in itertools.batched(raw_gen_obj, self.batch_size):
                validated_batch = []

                for raw_row in raw_chunk:
                    try:
                        validated_tx = Transaction(**raw_row)
                        validated_batch.append(validated_tx)
                    except ValidationError as e:
                        print(f'Skipping invalid transaction: {e}')

                if validated_batch:
                    self.writer.save_batch(validated_batch)
                    print(f'Flushed batch: +{len(validated_batch)} rows written.')


if __name__ == '__main__':
    pipeline = FraudDetectionPipeline(data_source='paysim_data/paysim_dataset.csv')
    pipeline.run_pipeline()