from pydantic import ValidationError
from core.adapters.ingestors import BatchIngestor
from core.domain.validation_models import Transaction
from core.adapters.writer import MySQLTransactions

class FraudDetectionPipeline:

    def __init__(self, data_source: str):
        self.data_source = data_source
        self.writer = MySQLTransactions()

    def run_pipeline(self):
        with BatchIngestor(data_source = self.data_source, throttle=False) as ingestor:
            for raw_row in ingestor.get_transactions():
                try:
                    validated_tx = Transaction(**raw_row)
                    self.writer.save(validated_tx)
                except ValidationError as e:
                    print(f'Skipping invalid transaction: {e}')
