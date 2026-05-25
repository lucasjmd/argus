import itertools
from pydantic import ValidationError

from core.adapters.ingestors import BatchIngestor
from core.domain.validation_models import Transaction
from core.adapters.writer import MySQLTransactions

class FraudDetectionPipeline:

    def __init__(self, data_source: str, batch_size: int = 5000):
        self.data_source = data_source
        self.batch_size = batch_size
        self.writer = MySQLTransactions()

    def run_pipeline(self):
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
